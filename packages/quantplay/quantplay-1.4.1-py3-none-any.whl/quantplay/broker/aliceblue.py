import os
import traceback

import pandas as pd
from pya3 import Aliceblue as Alice
from pya3 import OrderType as AliceOrderType
from pya3 import ProductType
from pya3 import TransactionType
from retrying import retry
import numpy as np
import pickle, codecs
from retrying import retry

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.exception.exceptions import (
    QuantplayOrderPlacementException,
    RetryableException,
    retry_exception,
)
from quantplay.utils.constant import Constants, OrderType, OrderStatus, timeit
from quantplay.utils.pickle_utils import PickleUtils

logger = Constants.logger


class Aliceblue(Broker):
    @timeit(MetricName="Aliceblue:__init__")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=2,
        retry_on_exception=retry_exception,
    )
    def __init__(self, user_id=None, api_key=None, order_updates=None, client=None):
        super(Aliceblue, self).__init__()
        self.order_updates = order_updates

        try:
            if client:
                self.set_client(client)
            else:
                if user_id is None or api_key is None:
                    raise InvalidArgumentException(
                        "Mandatory fields [user_id/api_key] are missing"
                    )
                self.alice = Alice(
                    user_id=user_id,
                    api_key=api_key,
                )
                response = self.alice.get_session_id()
                if "sessionID" not in response or response["sessionID"] is None:
                    if "emsg" in response:
                        raise InvalidArgumentException(response["emsg"])
                    raise InvalidArgumentException(f"Invalid API Key {api_key}")
        except InvalidArgumentException as e:
            raise
        except Exception as e:
            raise RetryableException(str(e))
        self.user_id = self.alice.user_id
        self.load_instrument()

    def set_client(self, serialized_client):
        self.alice = pickle.loads(codecs.decode(serialized_client.encode(), "base64"))

    def set_attributes(self, response):
        self.email = response["email"]
        self.user_id = response["actid"]
        self.full_name = response["uname"]
        self.user_token = response["susertoken"]

    def get_quantplay_symbol(self, symbol):
        if "-EQ" in symbol:
            return symbol.replace("-EQ", "")
        return symbol

    def load_instrument(self):
        try:
            self.symbol_data = PickleUtils.load_data("aliceblue_instruments")
            Constants.logger.info(
                "[LOADING_INSTRUMENTS] loading aliceblue instruments data from cache"
            )
        except Exception as e:
            Constants.logger.info(
                "[LOADING_INSTRUMENTS] loading aliceblue instruments data from server"
            )

            all_exchanges = ["NFO", "NSE", "INDICES"]
            for exchange in all_exchanges:
                self.alice.get_contract_master(exchange)

            cwd = os.getcwd()
            self.instrument_data = pd.concat(
                (pd.read_csv(f"{cwd}/{exchange}.csv") for exchange in all_exchanges),
                ignore_index=True,
            )

            self.instrument_data = self.instrument_data[self.instrument_data.Token > 0]
            self.instrument_data.loc[:, "token"] = self.instrument_data.Token.astype(
                int
            )
            self.instrument_data.rename(
                columns={
                    "Strike Price": "strike_price",
                    "Expiry Date": "instrument_expiry",
                    "Symbol": "instrument_symbol",
                    "Exch": "exchange",
                    "Option Type": "option_type",
                    "Instrument Name": "instrument",
                    "Lot Size": "lot_size",
                },
                inplace=True,
            )

            self.initialize_expiry_fields()
            self.add_quantplay_opt_tradingsymbol()
            self.add_quantplay_fut_tradingsymbol()

            self.instrument_data.loc[:, "broker_symbol"] = self.instrument_data[
                "Trading Symbol"
            ]
            self.instrument_data = self.instrument_data[
                [
                    "token",
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

            self.initialize_symbol_data(save_as="aliceblue_instruments")

        self.initialize_broker_symbol_map()

    def get_transaction_type(self, transaction_type):
        if (
            transaction_type == "BUY"
            or transaction_type == TransactionType.Buy.value
            or transaction_type == "B"
        ):
            return TransactionType.Buy
        elif (
            transaction_type == "SELL"
            or transaction_type == TransactionType.Sell.value
            or transaction_type == "S"
        ):
            return TransactionType.Sell

        raise InvalidArgumentException(
            "transaction type {} not supported for trading".format(transaction_type)
        )

    def get_order_type(self, order_type):
        if order_type == OrderType.market or order_type == AliceOrderType.Market.value:
            return AliceOrderType.Market
        elif (
            order_type == OrderType.sl
            or order_type == AliceOrderType.StopLossLimit.value
        ):
            return AliceOrderType.StopLossLimit
        elif (
            order_type == OrderType.slm
            or order_type == AliceOrderType.StopLossMarket.value
        ):
            return AliceOrderType.StopLossMarket
        elif order_type == OrderType.limit or order_type == AliceOrderType.Limit.value:
            return AliceOrderType.Limit

        return order_type

    def get_product(self, product):
        if product == "NRML":
            return ProductType.Normal
        elif product == "CNC":
            return ProductType.Delivery
        elif product == "MIS":
            return ProductType.Intraday
        elif product in [
            ProductType.BracketOrder,
            ProductType.CoverOrder,
            ProductType.Delivery,
            ProductType.Normal,
            ProductType.Intraday,
        ]:
            return product

        raise InvalidArgumentException(
            "Product {} not supported for trading".format(product)
        )

    def get_symbol(self, symbol, exchange=None):
        if exchange == "NSE":
            if "-EQ" not in symbol:
                return f"{symbol}-EQ"
        return symbol

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
            if trigger_price != None:
                trigger_price = float(trigger_price)

            order_type = self.get_order_type(order_type)
            product = self.get_product(product)

            instrument = self.alice.get_instrument_by_symbol(exchange, tradingsymbol)

            response = self.alice.place_order(
                transaction_type=self.get_transaction_type(transaction_type),
                product_type=product,
                instrument=instrument,
                order_type=order_type,
                quantity=quantity,
                price=float(price),
                trigger_price=trigger_price,
                order_tag=tag,
            )
            Constants.logger.info(f"[PLACE_ORDER_RESPONSE] {response}")
            return response["NOrdNo"]
        except Exception as e:
            print(traceback.print_exc())
            exception_message = f"Order placement failed [{str(e)}]"
            raise QuantplayOrderPlacementException(exception_message)

    def get_ltp(self, exchange, tradingsymbol):
        inst = self.alice.get_instrument_by_symbol(exchange, tradingsymbol)
        info = self.alice.get_scrip_info(inst)
        return info["LTP"]

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def modify_order(self, data):
        try:
            order_id = data["order_id"]
            order_history = self.alice.get_order_history(order_id)
            exchange = order_history["Exchange"]
            token = int(order_history["token"])
            product_type = self.get_product(order_history["Pcode"])
            quantity = order_history["Qty"]

            order_type = order_history["Prctype"]
            if "order_type" in data:
                order_type = data["order_type"]
            order_type = self.get_order_type(order_type)

            transaction_type = order_history["Trantype"]
            if "transaction_type" in data:
                transaction_type = data["transaction_type"]
            transaction_type = self.get_transaction_type(transaction_type)

            trigger_price = None
            if "trigger_price" in data and data["trigger_price"] is not None:
                trigger_price = float(data["trigger_price"])

            response = self.alice.modify_order(
                instrument=self.alice.get_instrument_by_token(exchange, token),
                transaction_type=transaction_type,
                order_id=order_id,
                product_type=product_type,
                order_type=order_type,
                price=float(data["price"]),
                trigger_price=trigger_price,
                quantity=quantity,
            )
            logger.info("[MODIFY_ORDER_RESPONSE] [{order_id}]  response [{response}]")
            return response
        except Exception as e:
            print(traceback.print_exc())
            Constants.logger.error(
                f"[MODIFY_ORDER_FAILED] {data} with exception {str(e)}"
            )

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        data = {}

        data["order_id"] = order_id
        data["price"] = price
        data["order_type"] = order_type
        if trigger_price is not None and trigger_price > 0:
            data["trigger_price"] = trigger_price
        else:
            data["trigger_price"] = None

        self.modify_order(data)

    def cancel_order(self, order_id):
        return self.alice.cancel_order(order_id)

    def profile(self):
        profile = self.alice.get_profile()
        response = {
            "user_id": self.alice.user_id,
            "full_name": profile["accountName"],
            "email": profile["emailAddr"],
        }

        return response

    def positions(self):
        positions = self.alice.get_netwise_positions()

        if not isinstance(positions, list):
            return pd.DataFrame(columns=self.positions_column_list)

        positions = pd.DataFrame(positions)

        positions.loc[:, "tradingsymbol"] = positions.Tsym
        positions.loc[:, "ltp"] = positions.LTP.astype(float)
        positions.loc[:, "pnl"] = positions.realisedprofitloss.astype(
            float
        ) + positions.unrealisedprofitloss.astype(float)

        positions.loc[:, "option_type"] = positions.Opttype

        positions.rename(
            columns={
                "Pcode": "product",
                "netsellqty": "sell_quantity",
                "netbuyqty": "buy_quantity",
                "Exchange": "exchange",
            },
            inplace=True,
        )

        positions["buy_quantity"] = positions.buy_quantity.astype(int)
        positions["sell_quantity"] = positions.sell_quantity.astype(int)
        positions["quantity"] = positions.buy_quantity - positions.sell_quantity

        return positions[self.positions_column_list]

    def orders(self, tag=None, status=None):
        orders = self.alice.order_data()
        if not isinstance(orders, list) and orders["emsg"] == "No Data":
            return pd.DataFrame(columns=self.orders_column_list)
        positions = self.positions()
        if len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)

        orders = pd.DataFrame(orders)
        orders.loc[:, "tradingsymbol"] = orders.Trsym

        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.rename(
            columns={
                "Nstordno": "order_id",
                "accountId": "user_id",
                "Exchange": "exchange",
                "Avgprc": "average_price",
                "Pcode": "product",
                "Trantype": "transaction_type",
                "Qty": "quantity",
                "Trgprc": "trigger_price",
                "Prc": "price",
                "Fillshares": "filled_quantity",
                "rorgqty": "pending_quantity",
                "OrderedTime": "update_timestamp",
                "orderentrytime": "order_timestamp",
                "Prctype": "order_type",
                "Status": "status",
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
        orders["filled_quantity"] = orders.filled_quantity.astype(float)
        orders["average_price"] = orders.average_price.astype(float)
        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "S", -orders.pnl, orders.pnl
        )
        orders["order_timestamp"] = pd.to_datetime(orders.order_timestamp)
        orders["update_timestamp"] = pd.to_datetime(
            orders.update_timestamp, format="%d/%m/%Y %H:%M:%S"
        )

        orders.transaction_type = orders.transaction_type.replace(
            ["S", "B"], ["SELL", "BUY"]
        )

        orders.status = orders.status.replace(
            ["open", "trigger pending", "rejected", "cancelled", "complete"],
            [
                OrderStatus.open,
                OrderStatus.trigger_pending,
                OrderStatus.rejected,
                OrderStatus.cancelled,
                OrderStatus.complete,
            ],
        )

        orders.order_type = orders.order_type.replace(
            ["MKT", "L", "SL"], [OrderType.market, OrderType.limit, OrderType.sl]
        )

        orders = self.filter_orders(orders, status=status, tag=tag)

        return orders

    def account_summary(self):
        margins = self.alice.get_balance()
        margins = [a for a in margins if a["segment"] == "ALL"][0]

        response = {
            "margin_used": float(margins["debits"]),
            "total_balance": float(margins["credits"]),
            "margin_available": float(margins["net"]),
            "pnl": float(self.positions().pnl.sum()),
        }
        return response
