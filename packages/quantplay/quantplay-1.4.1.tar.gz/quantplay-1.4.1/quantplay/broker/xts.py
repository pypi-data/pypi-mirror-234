import traceback
import json

import pandas as pd
import numpy as np
import pickle
import codecs
from datetime import datetime

from quantplay.broker.generics.broker import Broker
from quantplay.utils.constant import Constants, timeit, OrderType
from quantplay.broker.xts_utils.Connect import XTSConnect
from quantplay.utils.pickle_utils import PickleUtils
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.broker.xts_utils.InteractiveSocketClient import OrderSocket_io

import requests
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class XTS(Broker):
    source = "WebAPI"

    @timeit(MetricName="XTS:__init__")
    def __init__(
        self,
        api_secret,
        api_key,
        root_interactive,
        root_market,
        order_updates=None,
        wrapper=None,
        ClientID=None,
    ):
        super(XTS, self).__init__()

        self.root_interactive = root_interactive
        self.order_updates = order_updates

        try:
            if wrapper:
                self.set_wrapper(wrapper)
                self.ClientID = ClientID
            else:
                self.wrapper = XTSConnect(
                    apiKey=api_key,
                    secretKey=api_secret,
                    source=self.source,
                    root_interactive=root_interactive,
                    root_market=root_market,
                )
                self.login()

        except Exception as e:
            print(traceback.print_exc())
            raise e

        self.initialize_symbol_data()

    def set_wrapper(self, serialized_wrapper):
        self.wrapper = pickle.loads(
            codecs.decode(serialized_wrapper.encode(), "base64")
        )

    def initialize_symbol_data(self):
        # TODO: Check for Futures
        try:
            self.symbol_data = PickleUtils.load_data("xts_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception as e:
            instruments = pd.read_csv(
                "https://quantplay-public-data.s3.ap-south-1.amazonaws.com/symbol_data/instruments.csv"
            )
            instruments = instruments.to_dict("records")
            self.symbol_data = {}

            for instrument in instruments:
                exchange = instrument["exchange"]
                tradingsymbol = instrument["tradingsymbol"]
                # NIFTY 08JUN2023 PE 17850 <- NIFTY2360817850PE
                # 2023-06-27 -> 08JUN2023
                # For FUTURES : EURINR23AUGFUT -> EURINR 23AUG2023 FUT

                ins_type = instrument["instrument_type"]
                name = instrument["name"]
                if ins_type in ["CE", "PE"]:
                    expiry = datetime.strftime(
                        datetime.strptime(str(instrument["expiry"]), "%Y-%m-%d"),
                        "%d%b%Y",
                    ).upper()
                    strike = str(instrument["strike"]).rstrip("0")
                    if strike[-1] == ".":
                        strike = strike[:-1]
                    instrument["broker_symbol"] = f"{name} {expiry} {ins_type} {strike}"
                elif ins_type == "FUT":
                    expiry = datetime.strftime(
                        datetime.strptime(str(instrument["expiry"]), "%Y-%m-%d"),
                        "%d%b%Y",
                    ).upper()
                    instrument["broker_symbol"] = f"{name} {expiry} FUT"
                else:
                    instrument["broker_symbol"] = tradingsymbol

                self.symbol_data["{}:{}".format(exchange, tradingsymbol)] = instrument

            PickleUtils.save_data(self.symbol_data, "xts_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from server")
        self.initialize_broker_symbol_map()

    def login(self):
        response_interact = self.wrapper.interactive_login()
        self.wrapper.marketdata_login()

        self.ClientID = response_interact["result"]["clientCodes"][0]

    def account_summary(self):
        # TODO: Edit For Dealers

        api_response = self.wrapper.get_balance(self.ClientID)

        if not api_response:
            return {
                "pnl": 0,
                "margin_used": 0,
                "margin_available": 0,
            }

            raise Exception(
                "[XTS_ERROR]: Balance API available for retail API users only, dealers can watch the same on dealer terminal"
            )

        api_response = api_response["result"]["BalanceList"][0]["limitObject"]

        response = {
            # TODO: Get PNL
            "pnl": 0,
            "margin_used": api_response["RMSSubLimits"]["marginUtilized"],
            "margin_available": api_response["RMSSubLimits"]["netMarginAvailable"],
        }

        return response

    def profile(self):
        api_response = self.wrapper.get_profile(self.ClientID)["result"]

        response = {
            "user_id": api_response["ClientId"],
            "full_name": api_response["ClientName"],
            "segments": api_response["ClientExchangeDetailsList"],
        }

        return response

    def orders(self, tag=None, order_type=None):
        api_response = self.wrapper.get_order_book(self.ClientID)

        if api_response["type"] == "error":
            raise Exception("[XTS_Error]: " + api_response["description"])

        api_response = api_response["result"]

        orders = pd.DataFrame(api_response)
        positions = self.positions()

        if len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)

        orders.loc[:, "tradingsymbol"] = orders.TradingSymbol
        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.rename(
            columns={
                "ClientID": "user_id",
                "AppOrderID": "order_id",
                "OrderStatus": "status",
                "ExchangeSegment": "exchange",
                "OrderPrice": "price",
                "OrderType": "order_type",
                "OrderSide": "transaction_type",
                "OrderAverageTradedPrice": "average_price",
                "OrderGeneratedDateTime": "order_timestamp",
                "OrderQuantity": "quantity",
                "CumulativeQuantity": "filled_quantity",
                "LeavesQuantity": "pending_quantity",
                "ProductType": "product",
                "OrderStopPrice": "trigger_price",
                "OrderUniqueIdentifier": "tag",
            },
            inplace=True,
        )

        orders.loc[:, "filled_quantity"] = orders.filled_quantity.astype(float)
        orders.loc[:, "average_price"] = np.where(
            orders.average_price == "", 0, orders.average_price
        )
        orders.loc[:, "average_price"] = orders.average_price.astype(float)
        orders.loc[:, "order_id"] = orders.order_id.astype(str)

        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "SELL", -orders.pnl, orders.pnl
        )
        orders.loc[:, "order_timestamp"] = pd.to_datetime(orders.order_timestamp)

        orders.loc[:, "exchange"] = orders.exchange.replace(
            ["NSECM", "NSEFO"], ["NSE", "NFO"]
        )
        orders.loc[:, "status"] = orders.status.replace(
            ["Rejected", "Cancelled", "Filled", "New"],
            ["REJECTED", "CANCELLED", "COMPLETE", "OPEN"],
        )
        orders.loc[:, "order_type"] = orders.order_type.replace(
            ["Limit", "StopLimit", "Market"], ["LIMIT", "TRIGGER PENDING", "MARKET"]
        )

        orders = orders[
            self.orders_column_list + ["price", "trigger_price", "order_type"]
        ]

        if tag:
            orders = orders[orders.tag == tag]

        if order_type:
            orders = orders[orders.order_type == order_type]

        return orders

    def positions(self):
        # TODO: get sell_value, buy_value
        api_response = self.wrapper.get_position_daywise(self.ClientID)

        if api_response["type"] == "error":
            raise Exception("[XTS_Error]: " + api_response["description"])

        api_response = api_response["result"]["positionList"]

        positions = pd.DataFrame(api_response)

        if len(positions) == 0:
            return pd.DataFrame(columns=self.positions_column_list)

        positions.rename(
            columns={
                "TradingSymbol": "tradingsymbol",
                "ExchangeSegment": "exchange",
                "OpenBuyQuantity": "buy_quantity",
                "OpenSellQuantity": "sell_quantity",
                "Quantity": "quantity",
                "SumOfTradedQuantityAndPriceBuy": "buy_value",
                "SumOfTradedQuantityAndPriceSell": "sell_value",
                "ProductType": "product",
            },
            inplace=True,
        )

        a = [
            "pnl",
            "option_type",
        ]

        positions.loc[:, "exchange"] = positions.exchange.replace(
            ["NSECM", "NSEFO"], ["NSE", "NFO"]
        )

        positions.loc[:, "exchange_symbol"] = (
            positions["exchange"] + ":" + positions["ExchangeInstrumentId"]
        )

        symbols = positions.exchange_symbol.unique().tolist()
        symbol_ltps = self.get_ltps(symbols)

        positions.loc[:, "ltp"] = positions.ExchangeInstrumentId.apply(
            lambda x: symbol_ltps[int(x)]
        )
        positions.loc[:, "pnl"] = positions.sell_value.astype(
            float
        ) - positions.buy_value.astype(float)
        positions.loc[:, "pnl"] += positions.quantity.astype(float) * positions.ltp
        positions.loc[:, "quantity"] = positions.quantity.astype(int)
        positions.loc[:, "buy_quantity"] = positions.buy_quantity.astype(int)
        positions.loc[:, "sell_quantity"] = positions.sell_quantity.astype(int)

        positions.loc[:, "option_type"] = None

        return positions[self.positions_column_list]

    def get_ltps(self, symbols):
        instruments = [
            {
                "exchangeSegment": int(self.get_exchange_code(x.split(":")[0])),
                "exchangeInstrumentID": int(x.split(":")[1]),
            }
            for x in symbols
        ]

        api_response = self.wrapper.get_quote(
            Instruments=instruments,
            xtsMessageCode=1512,
            publishFormat="JSON",
        )["result"]

        ltp_json = api_response["listQuotes"]

        ltp = [json.loads(x) for x in ltp_json]

        ltp = {x["ExchangeInstrumentID"]: x["LastTradedPrice"] for x in ltp}
        return ltp

    def get_exchange_code(self, exchange):
        exchange_code_map = {
            "NSE": 1,
            "NFO": 2,
            "NSECM": 1,
            "NSEFO": 2,
            "NSECD": 3,
            "BSECM": 11,
            "BSEFO": 12,
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                "INVALID_EXCHANGE: Exchange not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def get_exchange_name(self, exchange):
        exchange_code_map = {
            "NSE": "NSECM",
            "NFO": "NSEFO",
            "NSECD": "NSECD",
            "BSECM": "BSECM",
            "BSEFO": "BSEFO",
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                "INVALID_EXCHANGE: Exchange not in ['NSE', 'NFO', 'NSECD', 'BSECM', 'BSEFO']"
            )

        return exchange_code_map[exchange]

    def get_ltp(self, exchange=None, tradingsymbol=None):
        exchange_code = self.get_exchange_code(exchange)
        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"][
            "exchange_token"
        ]

        api_response = self.wrapper.get_quote(
            Instruments=[
                {
                    "exchangeSegment": exchange_code,
                    "exchangeInstrumentID": exchange_token,
                }
            ],
            xtsMessageCode=1512,
            publishFormat="JSON",
        )["result"]

        ltp_json = api_response["listQuotes"][0]

        ltp = json.loads(ltp_json)["LastTradedPrice"]

        return ltp

    def place_order(
        self,
        tradingsymbol=None,
        exchange=None,
        quantity=None,
        order_type=None,
        transaction_type=None,
        tag=None,
        product=None,
        price=None,
        trigger_price=0,
    ):
        exchange_name = self.get_exchange_name(exchange)

        exchange_token = self.symbol_data[f"{exchange}:{tradingsymbol}"][
            "exchange_token"
        ]

        api_response = self.wrapper.place_order(
            exchangeSegment=exchange_name,
            exchangeInstrumentID=exchange_token,
            orderType=order_type,
            disclosedQuantity=0,
            orderQuantity=quantity,
            limitPrice=price,
            timeInForce="DAY",
            stopPrice=trigger_price,
            orderSide=transaction_type,
            productType=product,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )
        Constants.logger.info(f"[XTS_PLACE_ORDER_RESPONSE] {api_response}")

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_PLACE_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def cancel_order(self, order_id):
        orders = self.orders()

        order_data = orders[orders.order_id == str(order_id)]
        if len(order_data) == 0:
            raise InvalidArgumentException(f"Order [{order_id}] not found")
        order_data = order_data.to_dict("records")[0]

        tag = order_data["tag"]

        api_response = self.wrapper.cancel_order(
            appOrderID=int(order_id),
            clientID=order_data["user_id"],
            orderUniqueIdentifier=tag,
        )

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_CANCEL_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def get_order_type(self, order_type):
        if order_type == OrderType.market:
            return "Market"
        elif order_type == OrderType.sl:
            return "StopLimit"
        elif order_type == OrderType.slm:
            return "StopMarket"
        elif order_type == OrderType.limit:
            return "Limit"

        return order_type

    def modify_order(
        self,
        order_id,
        price=None,
        trigger_price=None,
        order_type=None,
        transaction_type=None,
        tag=None,
        product=None,
    ):
        orders = self.orders()
        order_data = orders[orders.order_id == order_id]
        if len(order_data) == 0:
            raise InvalidArgumentException(f"Order [{order_id}] not found")
        order_data = order_data.to_dict("records")[0]

        price = price or order_data["price"]
        trigger_price = trigger_price or order_data["trigger_price"]
        order_type = order_type or order_data["order_type"]
        tag = tag or order_data["tag"]
        product = product or order_data["product"]

        quantity = order_data["quantity"]
        time_in_force = "DAY"
        disclosed_quantity = 0

        api_response = self.wrapper.modify_order(
            appOrderID=order_id,
            modifiedTimeInForce=time_in_force,
            modifiedDisclosedQuantity=disclosed_quantity,
            modifiedLimitPrice=price,
            modifiedOrderQuantity=quantity,
            modifiedOrderType=self.get_order_type(order_type),
            modifiedProductType=product,
            modifiedStopPrice=trigger_price,
            orderUniqueIdentifier=tag,
            clientID=self.ClientID,
        )

        if api_response["type"] == "error":
            Constants.logger.info(f"[XTS_MODIFY_ORDER_ERROR] {api_response}")

            raise Exception("[XTS_ERROR]: " + api_response["description"])

        return api_response["result"]["AppOrderID"]

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        return self.modify_order(
            order_id=str(order_id),
            price=price,
            trigger_price=trigger_price,
            order_type=order_type,
        )

    def stream_order_data(self):
        socket = OrderSocket_io(
            userID=self.ClientID,
            token=self.wrapper.token,
            root_url=self.root_interactive,
        )
        socket.setup_event_listners(on_order=self.order_event_handler)
        socket.connect()

    def order_event_handler(self, order):
        order = json.loads(order)
        new_ord = {}

        try:
            new_ord["placed_by"] = order["ClientID"]
            new_ord["tag"] = order["ClientID"]
            new_ord["order_id"] = order["AppOrderID"]
            new_ord["exchange_order_id"] = order["ExchangeOrderID"]
            new_ord["exchange"] = order["ExchangeSegment"]
            new_ord["tradingsymbol"] = order["TradingSymbol"]

            if new_ord["exchange"] == "NSEFO":
                new_ord["exchange"] = "NFO"
            elif new_ord["exchange"] == "NSECM":
                new_ord["exchange"] = "NSE"

            if new_ord["exchange"] in ["NFO", "MCX"]:
                new_ord["tradingsymbol"] = self.broker_symbol_map[
                    new_ord["tradingsymbol"]
                ]

            new_ord["order_type"] = order["OrderType"].upper()
            new_ord["product"] = order["ProductType"].upper()
            new_ord["transaction_type"] = order["OrderSide"].upper()
            new_ord["quantity"] = int(order["OrderQuantity"])

            if "OrderStopPrice" in order:
                new_ord["trigger_price"] = float(order["OrderStopPrice"])
            else:
                new_ord["trigger_price"] = None

            new_ord["price"] = float(order["OrderPrice"])
            new_ord["status"] = order["OrderStatus"].upper()

            if new_ord["status"] == "PENDINGNEW":
                new_ord["status"] = "TRIGGER PENDING"
            elif new_ord["status"] == "PENDINGCANCEL":
                new_ord["status"] = "PENDING"
            elif new_ord["status"] == "PENDINGREPLACE":
                new_ord["status"] = "TRIGGER PENDING"
            elif new_ord["status"] == "REPLACED":
                new_ord["status"] = "UPDATE"

            print(new_ord)
            self.order_updates.put(new_ord)

        except Exception as e:
            print(e)
            Constants.logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))
