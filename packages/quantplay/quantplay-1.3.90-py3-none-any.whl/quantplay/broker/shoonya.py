from quantplay.broker.finvasia_utils.shoonya import ShoonyaApiPy
from quantplay.utils.constant import Constants, OrderType
from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException
import pyotp

from quantplay.utils.pickle_utils import PickleUtils

import pandas as pd
import numpy as np
from retrying import retry
import time
import json
import traceback
import copy

logger = Constants.logger


class FinvAsia(Broker):
    def __init__(
        self,
        order_updates=None,
        api_secret=None,
        imei=None,
        password=None,
        totp_key=None,
        user_id=None,
        vendor_code=None,
        user_token=None,
        load_instruments=True,
    ):
        super(FinvAsia, self).__init__()
        self.order_updates = order_updates

        self.api = ShoonyaApiPy()
        if user_token:
            self.api.set_session(
                userid=user_id, password=password, usertoken=user_token
            )
            response = {
                "susertoken": user_token,
                "actid": user_id,
                "email": None,
                "uname": None,
            }
        else:
            totp = pyotp.TOTP(totp_key).now()
            response = self.api.login(
                userid=user_id,
                password=password,
                twoFA=totp,
                vendor_code=vendor_code,
                api_secret=api_secret,
                imei=imei,
            )
            if response is None:
                raise InvalidArgumentException(f"Invalid API credentials")
        print(
            "finvasia login successful email {} account_id {}".format(
                response["email"], response["actid"]
            )
        )

        self.set_attributes(response)

        if load_instruments:
            self.load_instrument()

        self.order_type_sl = "SL-LMT"
        self.trigger_pending_status = "TRIGGER_PENDING"

    def set_attributes(self, response):
        self.email = response["email"]
        self.user_id = response["actid"]
        self.full_name = response["uname"]
        self.user_token = response["susertoken"]

    def load_instrument(self):
        try:
            self.symbol_data = PickleUtils.load_data("shoonya_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception as e:
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from server")
            instrument_file_EQ = self.get_df_from_zip(
                "https://api.shoonya.com/NSE_symbols.txt.zip"
            )
            instrument_file_FO = self.get_df_from_zip(
                "https://api.shoonya.com/NFO_symbols.txt.zip"
            )
            instrument_file_MCX = self.get_df_from_zip(
                "https://api.shoonya.com/MCX_symbols.txt.zip"
            )

            self.instrument_data = pd.concat(
                [instrument_file_MCX, instrument_file_FO, instrument_file_EQ]
            )
            self.instrument_data.loc[
                :, "instrument_symbol"
            ] = self.instrument_data.Symbol
            self.instrument_data.loc[
                :, "instrument_expiry"
            ] = self.instrument_data.Expiry
            self.instrument_data.loc[
                :, "strike_price"
            ] = self.instrument_data.StrikePrice
            self.instrument_data.loc[:, "exchange"] = self.instrument_data.Exchange
            self.instrument_data.loc[:, "option_type"] = self.instrument_data.OptionType
            self.instrument_data.loc[:, "instrument"] = self.instrument_data.Instrument
            self.instrument_data.loc[:, "lot_size"] = self.instrument_data.LotSize

            self.initialize_expiry_fields()
            self.add_quantplay_opt_tradingsymbol()
            self.add_quantplay_fut_tradingsymbol()

            self.instrument_data.loc[
                :, "broker_symbol"
            ] = self.instrument_data.TradingSymbol
            self.instrument_data = self.instrument_data[
                [
                    "Token",
                    "broker_symbol",
                    "strike_price",
                    "exchange",
                    "option_type",
                    "instrument",
                    "tradingsymbol",
                    "expiry",
                    "lot_size",
                ]
            ]

            self.initialize_symbol_data(save_as="shoonya_instruments")

        self.initialize_broker_symbol_map()

    def get_symbol(self, symbol, exchange=None):
        if symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    def get_transaction_type(self, transaction_type):
        if transaction_type == "BUY":
            return "B"
        elif transaction_type == "SELL":
            return "S"

        raise InvalidArgumentException(
            "transaction type {} not supported for trading".format(transaction_type)
        )

    def get_order_type(self, order_type):
        if order_type == OrderType.market:
            return "MKT"
        elif order_type == OrderType.sl:
            return "SL-LMT"
        elif order_type == OrderType.slm:
            return "SL-MKT"
        elif order_type == OrderType.limit:
            return "LMT"

        return order_type

    def get_product(self, product):
        if product == "NRML":
            return "M"
        elif product == "CNC":
            return "C"
        elif product == "MIS":
            return "I"
        elif product in ["M", "C", "I"]:
            return product

        raise InvalidArgumentException(
            "Product {} not supported for trading".format(product)
        )

    def event_handler_order_update(self, order):
        try:
            order["placed_by"] = order["actid"]
            order["tag"] = order["actid"]
            order["order_id"] = order["norenordno"]
            order["exchange_order_id"] = order["exchordid"]
            order["exchange"] = order["exch"]

            # TODO translate symbol
            # -EQ should be removed
            # F&O symbol translation
            order["tradingsymbol"] = order["tsym"]

            if order["exchange"] == "NSE":
                order["tradingsymbol"] = order["tradingsymbol"].replace("-EQ", "")
            elif order["exchange"] in ["NFO", "MCX"]:
                order["tradingsymbol"] = self.broker_symbol_map[order["tradingsymbol"]]

            order["order_type"] = order["prctyp"]
            if order["order_type"] == "LMT":
                order["order_type"] = "LIMIT"
            elif order["order_type"] == "MKT":
                order["order_type"] = "MARKET"
            elif order["order_type"] == "SL-LMT":
                order["order_type"] = "SL"

            if order["pcode"] == "M":
                order["product"] = "NRML"
            elif order["pcode"] == "C":
                order["product"] = "CNC"
            elif order["pcode"] == "I":
                order["product"] = "MIS"

            if order["trantype"] == "S":
                order["transaction_type"] = "SELL"
            elif order["trantype"] == "B":
                order["transaction_type"] = "BUY"
            else:
                logger.error(
                    "[UNKNOW_VALUE] finvasia transaction type {} not supported".format(
                        order["trantype"]
                    )
                )

            order["quantity"] = int(order["qty"])

            if "trgprc" in order:
                order["trigger_price"] = float(order["trgprc"])
            else:
                order["trigger_price"] = None

            order["price"] = float(order["prc"])

            if order["status"] == "TRIGGER_PENDING":
                order["status"] = "TRIGGER PENDING"
            elif order["status"] == "CANCELED":
                order["status"] = "CANCELLED"

            print(f"order feed {order}")
            self.order_updates.put(order)
        except Exception as e:
            logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))

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
        trigger_price=None,
    ):
        try:
            if trigger_price == 0:
                trigger_price = None

            transaction_type = self.get_transaction_type(transaction_type)
            order_type = self.get_order_type(order_type)
            product = self.get_product(product)
            tradingsymbol = self.get_symbol(tradingsymbol)

            data = {
                "product_type": product,
                "buy_or_sell": transaction_type,
                "exchange": exchange,
                "tradingsymbol": tradingsymbol,
                "quantity": quantity,
                "price_type": order_type,
                "price": price,
                "trigger_price": trigger_price,
                "remarks": tag,
            }
            Constants.logger.info("[PLACING_ORDER] {}".format(json.dumps(data)))
            response = self.api.place_order(
                buy_or_sell=transaction_type,
                product_type=product,
                exchange=exchange,
                tradingsymbol=tradingsymbol,
                quantity=quantity,
                discloseqty=0,
                price_type=order_type,
                price=price,
                trigger_price=trigger_price,
                retention="DAY",
                remarks=tag,
            )
            Constants.logger.info(
                "[PLACE_ORDER_RESPONSE] {} input {}".format(response, json.dumps(data))
            )
            if "norenordno" in response:
                return response["norenordno"]
            else:
                raise Exception(response)
        except Exception as e:
            print(traceback.print_exc())
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)

    def get_orders(self):
        return self.api.get_order_book()

    def get_ltp(self, exchange, tradingsymbol):
        tradingsymbol = self.get_symbol(tradingsymbol)
        token = self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["Token"]
        return float(self.api.get_quotes(exchange, str(token))["lp"])

    def live_data(self, exchange, tradingsymbol):
        tradingsymbol = self.get_symbol(tradingsymbol)
        token = self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["Token"]
        data = self.api.get_quotes(exchange, str(token))
        return {
            "ltp": float(data["lp"]),
            "upper_circuit": float(data["uc"]),
            "lower_circuit": float(data["lc"]),
        }

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def modify_order(self, data):
        data["order_type"] = self.get_order_type(data["order_type"])

        if "trigger_price" not in data:
            data["trigger_price"] = None
        if "order_id" in data:
            data["norenordno"] = data["order_id"]
        if "exchange" in data:
            data["exch"] = data["exchange"]
        if "tradingsymbol" in data:
            data["tsym"] = data["tradingsymbol"]
        if "order_type" in data:
            data["prctyp"] = data["order_type"]
        if "quantity" in data:
            data["qty"] = data["quantity"]
        if "price" in data:
            data["prc"] = data["price"]
        try:
            logger.info(
                "Modifying order [{}] new price [{}]".format(
                    data["norenordno"], data["prc"]
                )
            )
            response = self.api.modify_order(
                orderno=data["norenordno"],
                exchange=data["exch"],
                tradingsymbol=data["tsym"],
                newprice_type=data["prctyp"],
                newquantity=data["qty"],
                newprice=data["prc"],
                newtrigger_price=data["trigger_price"],
            )
            logger.info(
                "[MODIFY_ORDER_RESPONSE] order id [{}] response [{}]".format(
                    data["norenordno"], response
                )
            )
            return response
        except Exception as e:
            exception_message = (
                "OrderModificationFailed for {} failed with exception {}".format(
                    data["norenordno"], e
                )
            )
            Constants.logger.error("{}".format(exception_message))

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        data = {}
        order_history = self.api.single_order_history(order_id)
        order_details = order_history[0]
        data["norenordno"] = order_id
        data["prc"] = price
        data["prctyp"] = order_details["prctyp"]
        data["exch"] = order_details["exch"]
        data["qty"] = order_details["qty"]
        data["tsym"] = order_details["tsym"]
        data["order_type"] = order_type
        if trigger_price != None and trigger_price > 0:
            data["newtrigger_price"] = trigger_price
        else:
            data["newtrigger_price"] = None

        self.modify_order(data)

    def cancel_order(self, order_id):
        self.api.cancel_order(order_id)

    def stream_order_data(self):
        self.api.start_websocket(order_update_callback=self.event_handler_order_update)

    def profile(self):

        response = {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
        }

        return response

    def positions(self):
        positions = self.api.get_positions()

        if positions is None or len(positions) == 0:
            return pd.DataFrame(columns=self.positions_column_list)

        positions = pd.DataFrame(positions)

        positions.loc[:, "tradingsymbol"] = positions.tsym
        positions.loc[:, "ltp"] = positions.lp.astype(float)
        positions.loc[:, "pnl"] = positions.rpnl.astype(
            float
        ) + positions.urmtom.astype(float)

        if "dname" not in positions.columns:
            positions.loc[:, "dname"] = None

        positions.loc[:, "dname"] = positions.dname.str.strip()
        positions.loc[:, "dname"] = positions.dname.str.strip()
        positions.loc[:, "option_type"] = np.where(
            "PE" == positions.dname.str[-2:], "PE", np.nan
        )
        positions.loc[:, "option_type"] = np.where(
            "CE" == positions.dname.str[-2:], "CE", positions.option_type
        )
        positions.loc[:, "option_type"] = np.where(
            positions.exch != "NFO", None, positions.option_type
        )

        positions.rename(
            columns={
                "prd": "product",
                "opensellqty": "sell_quantity",
                "openbuyqty": "buy_quantity",
                "exch": "exchange",
            },
            inplace=True,
        )

        positions.loc[:, "buy_quantity"] = positions.buy_quantity.astype(int)
        positions.loc[:, "sell_quantity"] = positions.sell_quantity.astype(int)
        positions.loc[:, "quantity"] = positions.buy_quantity - positions.sell_quantity

        positions["product"] = positions["product"].replace(
            ["I", "C", "M"], ["MIS", "CNC", "NRML"]
        )

        return positions[self.positions_column_list]

    def add_transaction_charges(self, orders):
        return super(FinvAsia, self).add_transaction_charges(
            orders, cm_charges=0, fo_charges=0
        )

    def orders(self, tag=None, status=None):
        orders = pd.DataFrame(self.api.get_order_book())
        positions = self.positions()
        if len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)

        orders.loc[:, "tradingsymbol"] = orders.tsym
        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.rename(
            columns={
                "norenordno": "order_id",
                "uid": "user_id",
                "exch": "exchange",
                "remarks": "tag",
                "avgprc": "average_price",
                "prd": "product",
                "trantype": "transaction_type",
                "qty": "quantity",
                "trgprc": "trigger_price",
                "prc": "price",
                "fillshares": "filled_quantity",
                "rorgqty": "pending_quantity",
                "norentm": "order_timestamp",
            },
            inplace=True,
        )

        existing_columns = list(orders.columns)
        columns_to_keep = list(
            set(self.orders_column_list).intersection(set(existing_columns))
        )
        orders = orders[columns_to_keep]

        if "filled_quantity" not in orders.columns:
            orders.loc[:, "filled_quantity"] = 0
        if "average_price" not in orders.columns:
            orders.loc[:, "average_price"] = 0
        orders.loc[:, "filled_quantity"] = orders.filled_quantity.astype(float)
        orders.loc[:, "average_price"] = orders.average_price.astype(float)
        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "S", -orders.pnl, orders.pnl
        )
        orders.loc[:, "order_timestamp"] = pd.to_datetime(
            orders.order_timestamp, format="%H:%M:%S %d-%m-%Y"
        )

        orders = self.filter_orders(orders, status=status, tag=tag)

        orders.transaction_type = orders.transaction_type.replace(
            ["S", "B"], ["SELL", "BUY"]
        )

        orders.status = orders.status.replace(
            ["TRIGGER_PENDING", "CANCELED"], ["TRIGGER PENDING", "CANCELLED"]
        )

        orders["product"] = orders["product"].replace(
            ["I", "C", "M"], ["MIS", "CNC", "NRML"]
        )

        return orders

    def account_summary(self):
        margins = self.api.get_limits()

        pnl = 0
        positions = self.positions()
        if len(positions) > 0:
            pnl = positions.pnl.sum()

        if "marginused" not in margins:
            margins["marginused"] = 0
        if "payin" not in margins:
            margins["payin"] = 0
        margin_available = (
            float(margins["cash"])
            + float(margins["payin"])
            - float(margins["marginused"])
        )
        response = {
            "margin_used": float(margins["marginused"]),
            "total_balance": float(margins["cash"]),
            "margin_available": margin_available,
            "pnl": pnl,
        }
        return response
