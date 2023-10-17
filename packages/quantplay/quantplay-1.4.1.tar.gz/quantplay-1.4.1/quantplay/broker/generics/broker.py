import math
import random
import time
from collections import defaultdict
import threading
from threading import Lock

import numpy as np
import pandas as pd
import io
import os
import zipfile
import requests
import platform

from quantplay.exception.exceptions import QuantplayOrderPlacementException
from quantplay.utils.constant import Constants
from quantplay.utils.exchange import Market as MarketConstants
from quantplay.utils.number_utils import NumberUtils
from quantplay.utils.pickle_utils import PickleUtils
from quantplay.utils.constant import Order, StrategyType, ExchangeName, timeit
import traceback, copy
from datetime import datetime, timedelta

logger = Constants.logger


class Broker:
    def __init__(self):
        self.instrument_data = None
        self.instrument_id_to_symbol_map = dict()
        self.instrument_id_to_exchange_map = dict()
        self.instrument_id_to_security_type_map = dict()
        self.exchange_symbol_to_instrument_id_map = defaultdict(dict)
        self.order_type_sl = "SL"
        self.nfo_exchange = "NFO"

        self.orders_column_list = [
            "order_id",
            "user_id",
            "tradingsymbol",
            "tag",
            "average_price",
            "transaction_type",
            "status",
            "ltp",
            "exchange",
            "product",
            "quantity",
            "filled_quantity",
            "pending_quantity",
            "order_timestamp",
            "trigger_price",
            "price",
            "token",
            "update_timestamp",
            "order_type",
            "variety",
        ]
        self.positions_column_list = [
            "tradingsymbol",
            "quantity",
            "ltp",
            "pnl",
            "buy_quantity",
            "sell_quantity",
            "exchange",
            "product",
            "option_type",
        ]
        self.trigger_pending_status = "TRIGGER PENDING"
        self.lock = Lock()

    def initialize_symbol_data(self, save_as=None):
        instruments = self.instrument_data
        instruments = instruments.to_dict("records")
        self.symbol_data = {}
        for instrument in instruments:
            exchange = instrument["exchange"]
            tradingsymbol = instrument["broker_symbol"]

            instrument_data = copy.deepcopy(instrument)
            self.symbol_data["{}:{}".format(exchange, tradingsymbol)] = instrument_data

        PickleUtils.save_data(self.symbol_data, save_as)

    @timeit(MetricName="Broker:initialize_broker_symbol_map")
    def initialize_broker_symbol_map(self):
        self.broker_symbol_map = {}
        for a in self.symbol_data:
            self.broker_symbol_map[
                self.symbol_data[a]["broker_symbol"]
            ] = self.symbol_data[a]["tradingsymbol"]
        platform_version = platform.python_version().split(".")
        if (
            len(platform_version) >= 2
            and platform_version[0] == "3"
            and platform_version[1] == "8"
        ):
            self.quantplay_symbol_map = {}
            for k in self.broker_symbol_map:
                v = self.broker_symbol_map[k]
                self.quantplay_symbol_map[v] = k
        else:
            self.quantplay_symbol_map = {
                v: k for k, v in self.broker_symbol_map.items()
            }

    def round_to_tick(self, number):
        return round(number * 20) / 20

    def get_user_id(self):
        return self.user_id

    def populate_instruments(self, instruments):
        """Fetches instruments for all exchanges from the broker
        and stores them in the member attributes.
        """
        Constants.logger.info("populating instruments")
        for instrument in instruments:
            exchange, symbol, instrument_id = (
                instrument.exchange,
                instrument.symbol,
                instrument.instrument_id,
            )
            self.instrument_id_to_symbol_map[instrument_id] = symbol
            self.instrument_id_to_exchange_map[instrument_id] = exchange
            self.instrument_id_to_security_type_map[
                instrument_id
            ] = instrument.security_type()
            self.exchange_symbol_to_instrument_id_map[exchange][symbol] = instrument_id

    def add_quantplay_fut_tradingsymbol(self):
        seg_condition = [
            (
                (self.instrument_data["instrument"].str.contains("FUT"))
                & (self.instrument_data.instrument != "OPTFUT")
            )
        ]

        tradingsymbol = [
            self.instrument_data.tradingsymbol
            + self.instrument_data.expiry_year
            + self.instrument_data.month
            + "FUT"
        ]

        self.instrument_data.loc[:, "tradingsymbol"] = np.select(
            seg_condition, tradingsymbol, default=self.instrument_data.tradingsymbol
        )

    def add_quantplay_opt_tradingsymbol(self):
        seg_condition = self.instrument_data["strike_price"] > 0
        weekly_option_condition = (
            self.instrument_data.expiry.dt.month
            == self.instrument_data.next_expiry.dt.month
        ) & (self.instrument_data.exchange == "NFO")
        month_option_condition = (
            self.instrument_data.expiry.dt.month
            != self.instrument_data.next_expiry.dt.month
        ) | (self.instrument_data.exchange == "MCX")

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.expiry_year,
            self.instrument_data.tradingsymbol,
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & weekly_option_condition,
            self.instrument_data.tradingsymbol
            + self.instrument_data.week_option_prefix,
            self.instrument_data.tradingsymbol,
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & month_option_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.month,
            self.instrument_data.tradingsymbol,
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol
            + self.instrument_data.strike_price.astype(float)
            .astype(str)
            .str.split(".")
            .str[0],
            self.instrument_data.tradingsymbol,
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.option_type,
            self.instrument_data.tradingsymbol,
        )

    def get_df_from_zip(self, url):
        response = requests.get(url, timeout=10)
        z = zipfile.ZipFile(io.BytesIO(response.content))

        directory = "/tmp/"
        z.extractall(path=directory)
        file_name = url.split(".txt")[0].split("/")[-1]
        os.system("cp /tmp/{}.txt /tmp/{}.csv".format(file_name, file_name))
        time.sleep(2)
        return pd.read_csv("/tmp/{}.csv".format(file_name))

    def initialize_expiry_fields(self):
        self.instrument_data.loc[
            :, "tradingsymbol"
        ] = self.instrument_data.instrument_symbol
        self.instrument_data.loc[:, "expiry"] = pd.to_datetime(
            self.instrument_data.instrument_expiry
        )

        self.instrument_data.loc[:, "expiry_year"] = (
            self.instrument_data["expiry"].dt.strftime("%y").astype(str)
        )
        self.instrument_data.loc[:, "month"] = (
            self.instrument_data["expiry"].dt.strftime("%b").str.upper()
        )

        self.instrument_data.loc[:, "month_number"] = (
            self.instrument_data["expiry"].dt.strftime("%m").astype(float).astype(str)
        )
        self.instrument_data.loc[:, "month_number"] = np.where(
            self.instrument_data.month_number == "nan",
            np.nan,
            self.instrument_data.month_number.str.split(".").str[0],
        )

        self.instrument_data.loc[:, "week_option_prefix"] = np.where(
            self.instrument_data.month_number.astype(float) >= 10,
            self.instrument_data.month.str[0]
            + self.instrument_data["expiry"].dt.strftime("%d").astype(str),
            self.instrument_data.month_number
            + self.instrument_data["expiry"].dt.strftime("%d").astype(str),
        )

        self.instrument_data.loc[
            :, "next_expiry"
        ] = self.instrument_data.expiry + pd.DateOffset(days=7)

    def execute_order_v2(self, order):
        start_time = datetime.now()
        tradingsymbol = order["tradingsymbol"]
        exchange = order["exchange"]
        trigger_price = order["trigger_price"]
        transaction_type = order["transaction_type"]
        if order["validity"] is not None and order["trigger_price"] is not None:
            while True:
                self.lock.acquire()
                try:
                    ltp = self.get_ltp(exchange, tradingsymbol)
                except Exception as e:
                    Constants.logger.error(
                        "[GET_LTP_FAILED] with exception {}".format(e)
                    )
                time.sleep(0.5)
                self.lock.release()
                if (transaction_type == "SELL" and trigger_price > ltp) or (
                    transaction_type == "BUY" and trigger_price < ltp
                ):
                    logger.info(
                        "[EXECUTING_ORDER] ltp {} crossed trigger price {} for {}".format(
                            ltp, trigger_price, order
                        )
                    )
                    self.execute_order(
                        tradingsymbol=order["tradingsymbol"],
                        exchange=order["exchange"],
                        quantity=order["quantity"],
                        product=order["product"],
                        tag=order["tag"],
                        stoploss=order["stoploss"],
                        transaction_type=order["transaction_type"],
                        order_type=order["order_type"],
                    )
                    return
                current_time = datetime.now()
                if (current_time - start_time).seconds > order["validity"]:
                    Constants.logger.info(
                        "[ORDER_VALIDITY_EXPIRED] order [{}]".format(order)
                    )
                    return

    def execute_order(
        self,
        tradingsymbol=None,
        exchange=None,
        quantity=None,
        order_type=None,
        transaction_type=None,
        stoploss=None,
        tag=None,
        product=None,
        price=None,
    ):
        upper_circuit = None
        trade_price = copy.deepcopy(price)
        if price is None:
            live_data = self.live_data(exchange=exchange, tradingsymbol=tradingsymbol)
            price = live_data["ltp"]
            upper_circuit = live_data["upper_circuit"]
            trade_price = copy.deepcopy(price)
        try:
            if stoploss != None:
                if transaction_type == "SELL":
                    sl_transaction_type = "BUY"
                    sl_trigger_price = self.round_to_tick(price * (1 + stoploss))

                    if exchange == "NFO":
                        price = sl_trigger_price * 1.05
                    elif exchange == "NSE":
                        price = sl_trigger_price * 1.01
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                elif transaction_type == "BUY":
                    sl_transaction_type = "SELL"
                    sl_trigger_price = self.round_to_tick(price * (1 - stoploss))

                    if exchange == self.nfo_exchange:
                        price = sl_trigger_price * 0.95
                    elif exchange == "NSE":
                        price = sl_trigger_price * 0.99
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                else:
                    raise Exception(
                        "Invalid transaction_type {}".format(transaction_type)
                    )

                if upper_circuit != None and sl_price > upper_circuit:
                    raise Exception(
                        f"[PRICE_BREACHED] {sl_price} is above upper circuit price [{upper_circuit}]"
                    )

                stoploss_order_id = self.place_order(
                    tradingsymbol=tradingsymbol,
                    exchange=exchange,
                    quantity=quantity,
                    order_type=self.order_type_sl,
                    transaction_type=sl_transaction_type,
                    tag=tag,
                    product=product,
                    price=sl_price,
                    trigger_price=sl_trigger_price,
                )

                if stoploss_order_id is None:
                    Constants.logger.error(
                        "[ORDER_REJECTED] tradingsymbol {}".format(tradingsymbol)
                    )
                    raise QuantplayOrderPlacementException(
                        "Order reject for {}".format(tradingsymbol)
                    )

            if order_type == "MARKET":
                trade_price = 0

            response = self.place_order(
                tradingsymbol=tradingsymbol,
                exchange=exchange,
                quantity=quantity,
                order_type=order_type,
                transaction_type=transaction_type,
                tag=tag,
                product=product,
                price=trade_price,
            )
            return response
        except Exception as e:
            raise e

    """
            Input  : quantplay symbol
            Output : broker symbol
        """

    def get_symbol(self, symbol, exchange=None):
        return symbol

    """
        Input  : quantplay exchange
        Output : broker exchange
    """

    def get_order_type(self, order_type):
        return order_type

    def get_exchange(self, exchange):
        return exchange

    def live_data(self, exchange, tradingsymbol):
        return {
            "ltp": self.get_ltp(exchange, tradingsymbol),
            "upper_circuit": None,
            "lower_circuit": None,
        }

    def place_order_quantity(self, quantity, tradingsymbol, exchange):
        lot_size = self.get_lot_size(exchange, tradingsymbol)
        quantity_in_lots = int(quantity / lot_size)

        return quantity_in_lots * lot_size

    def get_product(self, product):
        return product

    def get_lot_size(self, exchange, tradingsymbol):
        tradingsymbol = self.get_symbol(tradingsymbol, exchange=exchange)
        exchange = self.get_exchange(exchange)
        try:
            return int(
                self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["lot_size"]
            )
        except Exception as e:
            logger.error(
                "[GET_LOT_SIZE] unable to get lot size for {} {}".format(
                    exchange, tradingsymbol
                )
            )
            raise e

    def filter_orders(self, orders, tag=None, status=None):
        if tag:
            orders = orders[orders.tag == tag]

        if status:
            orders = orders[orders.status == status]

        return orders

    def option_symbol(self, underlying_symbol, expiry_date, strike_price, type):
        option_symbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[
            underlying_symbol
        ]
        option_symbol += expiry_date.strftime("%y")

        month_number = str(int(expiry_date.strftime("%m")))
        monthly_option_prefix = expiry_date.strftime("%b").upper()

        if int(month_number) >= 10:
            week_option_prefix = monthly_option_prefix[0]
        else:
            week_option_prefix = month_number
        week_option_prefix += expiry_date.strftime("%d")

        next_expiry = expiry_date + timedelta(days=7)

        if next_expiry.month != expiry_date.month:
            option_symbol += monthly_option_prefix
        else:
            option_symbol += week_option_prefix

        option_symbol += str(int(strike_price))
        option_symbol += type

        return option_symbol

    def exit_all_trigger_orders(
        self,
        tag="ALL",
        symbol_contains=None,
        order_timestamp=None,
        modify_sleep_time=10,
    ):
        stoploss_orders = self.orders()
        stoploss_orders = stoploss_orders[stoploss_orders.status == "TRIGGER PENDING"]

        if len(stoploss_orders) == 0:
            Constants.logger.info("All stoploss orders have been already closed")
            return

        if tag != "ALL":
            stoploss_orders = stoploss_orders[stoploss_orders.tag == tag]

        if symbol_contains is not None:
            symbol_contains = self.get_symbol(symbol_contains)
            stoploss_orders = stoploss_orders[
                stoploss_orders["tradingsymbol"].str.contains(symbol_contains)
            ]

        if order_timestamp is not None:
            stoploss_orders.loc[
                :, "order_timestamp"
            ] = stoploss_orders.order_timestamp.apply(lambda x: x.replace(second=0))
            stoploss_orders = stoploss_orders[
                stoploss_orders.order_timestamp == order_timestamp
            ]

        if len(stoploss_orders) == 0:
            Constants.logger.info("All stoploss orders have been already closed")
            return

        orders_to_close = list(stoploss_orders.order_id.unique())

        stoploss_orders = stoploss_orders.to_dict("records")
        for stoploss_order in stoploss_orders:
            exchange = stoploss_order["exchange"]
            tradingsymbol = stoploss_order["tradingsymbol"]

            ltp = self.get_ltp(exchange, tradingsymbol)
            stoploss_order["order_type"] = "LIMIT"
            stoploss_order["price"] = self.round_to_tick(ltp)
            stoploss_order["trigger_price"] = None

            self.modify_order(stoploss_order)
            time.sleep(0.1)

        self.modify_orders_till_complete(orders_to_close, sleep_time=modify_sleep_time)
        Constants.logger.info("All order have been closed successfully")

    def square_off_all(self, dry_run=True, contains=None, sleep_time=0.1):
        positions = self.positions()
        if len(positions) == 0:
            print("Positions are already squared off")
            return []

        if contains:
            positions = positions[positions.tradingsymbol.str.contains(contains)]

        positions.loc[:, "net_quantity"] = (
            positions.buy_quantity - positions.sell_quantity
        )
        positions = positions[positions.net_quantity != 0]
        if len(positions) == 0:
            print("Positions are already squared off")
            return []
        positions.loc[:, "transaction_type"] = np.where(
            positions.quantity < 0, "BUY", "SELL"
        )
        positions.loc[:, "lot_size"] = positions.apply(
            lambda x: self.get_lot_size(x.exchange, x.tradingsymbol), axis=1
        )
        positions.loc[:, "price"] = positions.apply(
            lambda x: self.get_ltp(x["exchange"], x["tradingsymbol"]), axis=1
        )

        positions = positions.to_dict("records")
        orders_to_close = []
        for position in positions:
            quantity = abs(position["net_quantity"])
            exchange = position["exchange"]
            tradingsymbol = position["tradingsymbol"]
            transaction_type = position["transaction_type"]

            quantity_in_lots = int(
                quantity / self.get_lot_size(exchange, tradingsymbol)
            )

            split_into = int(math.ceil(quantity_in_lots / 25))
            split_array = NumberUtils.split(abs(quantity_in_lots), abs(split_into))

            for q in split_array:
                orders_to_close.append(
                    {
                        "symbol": tradingsymbol,
                        "exchange": exchange,
                        "transaction_type": transaction_type,
                        "quantity_in_lots": q,
                        "product": position["product"],
                        "price": position["price"],
                    }
                )

        random.shuffle(orders_to_close)
        orders_to_close = sorted(orders_to_close, key=lambda d: d["transaction_type"])
        orders_placed = []
        for order in orders_to_close:
            quantity = int(
                order["quantity_in_lots"]
                * self.get_lot_size(order["exchange"], order["symbol"])
            )
            print(
                order["symbol"],
                order["exchange"],
                order["transaction_type"],
                quantity,
                order["product"],
                order["price"],
            )
            if dry_run == False:
                order_id = self.place_order(
                    tradingsymbol=order["symbol"],
                    exchange=order["exchange"],
                    quantity=quantity,
                    order_type="LIMIT",
                    transaction_type=order["transaction_type"],
                    tag="killall",
                    product=order["product"],
                    price=order["price"],
                )
                orders_placed.append(str(order_id))
                time.sleep(sleep_time)
        if dry_run == False:
            self.modify_orders_till_complete(orders_placed)

        return orders_to_close

    def convert_to_event(self, order):
        order = copy.deepcopy(order)
        order["placed_by"] = self.user_id
        order["tag"] = self.user_id

        order["exchange_order_id"] = order["order_id"]
        order["quantity"] = int(order["quantity"])
        order["tradingsymbol"] = self.get_quantplay_symbol(order["tradingsymbol"])

        order["order_timestamp"] = str(order["order_timestamp"])
        order["update_timestamp"] = str(order["update_timestamp"])

        if "trigger_price" in order and order["trigger_price"] != 0:
            order["trigger_price"] = float(order["trigger_price"])
        else:
            order["trigger_price"] = None
        Constants.logger.info(f"[ORDER_EVENT] {order}")
        if order["status"] == "COMPLETE":
            order["status"] = "OPEN"
            self.order_updates.put(copy.deepcopy(order))
            order["status"] = "COMPLETE"
            time.sleep(1)
        self.order_updates.put(order)

    def get_quantplay_symbol(self, symbol):
        return self.broker_symbol_map[symbol]

    def stream_order_updates(self):

        self.order_log = {}
        while 1:
            try:
                orders = self.orders()

                if len(orders) > 0:
                    delta_time = str(
                        datetime.now().replace(microsecond=0) - timedelta(seconds=120)
                    )
                    orders = orders[orders.update_timestamp >= delta_time]

                    orders = orders.to_dict("records")
                    for order in orders:
                        order_id = order["order_id"]
                        if order_id not in self.order_log:
                            self.convert_to_event(order)
                        else:
                            update_timestamp = str(order["update_timestamp"])
                            last_log_time = str(
                                self.order_log[order_id]["update_timestamp"]
                            )

                            if update_timestamp != last_log_time:
                                self.convert_to_event(order)
                        self.order_log[order_id] = copy.deepcopy(order)
                time.sleep(3)
            except Exception as e:
                print(traceback.print_exc())
                print(f"Unable to process order stream for {self.user_id}")
                time.sleep(5)

    def stream_order_data(self):
        th = threading.Thread(target=self.stream_order_updates, daemon=True)
        th.start()

    def square_off_by_tag(self, tag, dry_run=True, sleep_time=0.05):
        self.exit_all_trigger_orders(tag=tag)
        orders = self.orders(tag=tag)

        if len(orders) == 0:
            logger.info(
                f"All positions with tag {tag} are already squared-off for {self.profile()}"
            )
        orders.loc[:, "exit_quantity"] = np.where(
            orders.transaction_type == "BUY",
            -orders.filled_quantity,
            orders.filled_quantity,
        )
        exit_orders = (
            orders.groupby("tradingsymbol")
            .agg({"exit_quantity": "sum", "exchange": "first", "product": "first"})
            .reset_index()
        )

        orders_to_close = []
        exit_orders = exit_orders[exit_orders.exit_quantity != 0]
        positions = exit_orders.to_dict("records")
        for position in positions:
            exchange = position["exchange"]
            tradingsymbol = position["tradingsymbol"]
            quantity = position["exit_quantity"]

            transaction_type = "SELL"
            if quantity == 0:
                continue
            elif quantity > 0:
                transaction_type = "BUY"

            quantity = abs(quantity)
            quantity_in_lots = int(
                quantity / self.get_lot_size(exchange, tradingsymbol)
            )

            split_into = int(math.ceil(quantity_in_lots / 25))
            split_array = NumberUtils.split(abs(quantity_in_lots), abs(split_into))

            for q in split_array:
                orders_to_close.append(
                    {
                        "tradingsymbol": tradingsymbol,
                        "exchange": exchange,
                        "transaction_type": transaction_type,
                        "quantity_in_lots": q,
                        "product": position["product"],
                    }
                )

        random.shuffle(orders_to_close)
        orders_to_close = sorted(orders_to_close, key=lambda d: d["transaction_type"])
        for order in orders_to_close:
            tradingsymbol = order["tradingsymbol"]
            exchange = order["exchange"]
            transaction_type = order["transaction_type"]
            product = order["product"]
            quantity = order["quantity_in_lots"] * self.get_lot_size(
                exchange, tradingsymbol
            )
            quantity = self.place_order_quantity(quantity, tradingsymbol, exchange)

            print(tradingsymbol, exchange, transaction_type, quantity)
            if dry_run == False:
                self.place_order(
                    tradingsymbol=tradingsymbol,
                    exchange=exchange,
                    quantity=quantity,
                    order_type="MARKET",
                    transaction_type=transaction_type,
                    tag=tag,
                    product=product,
                    price=0,
                )
                time.sleep(sleep_time)

        return orders_to_close

    def add_ltp(self, orders):
        orders.loc[:, "exchange_symbol"] = orders.exchange + ":" + orders.tradingsymbol

        all_symbols = list(orders.exchange_symbol.unique())
        symbol_ltp = {}
        for exchange_symbol in all_symbols:
            ltp = self.get_ltp(
                exchange_symbol.split(":")[0], exchange_symbol.split(":")[1]
            )
            symbol_ltp[exchange_symbol] = ltp
        orders.loc[:, "ltp"] = orders["exchange_symbol"].map(symbol_ltp)

    def risk_analysis(self):
        positions = self.positions()
        positions.loc[:, "net_quantity"] = (
            positions.buy_quantity - positions.sell_quantity
        )
        positions.loc[:, "premium"] = positions.net_quantity * positions.ltp

        bank_nifty = positions[positions.tradingsymbol.str.contains("BANKNIFTY")]
        t_df = bank_nifty.groupby("option_type").premium.sum().reset_index()
        t_df.loc[:, "segment"] = t_df.option_type
        t_df = t_df[["segment", "premium"]]
        response = {"banknifty_premium": t_df}

        fin_nifty = positions[positions.tradingsymbol.str.contains("FINNIFTY")]
        t_df = fin_nifty.groupby("option_type").premium.sum().reset_index()
        t_df.loc[:, "segment"] = t_df.option_type
        t_df = t_df[["segment", "premium"]]
        response["finnifty_premium"] = t_df

        return response

    def add_transaction_charges(self, orders, cm_charges=0.0003, fo_charges=20):
        orders.loc[:, "sell_value"] = np.where(
            orders.transaction_type == "SELL", orders.average_price * orders.quantity, 0
        )
        orders.loc[:, "buy_value"] = np.where(
            orders.transaction_type == "BUY", orders.average_price * orders.quantity, 0
        )

        orders.loc[:, "product"] = np.where(
            orders.exchange == ExchangeName.nse, "MIS", "NRML"
        )
        orders.loc[:, "security_type"] = np.where(
            orders.exchange == ExchangeName.nse, "EQ", "OPT"
        )

        charges_condition = [
            (orders["product"] == "MIS") & (orders["exchange"] == ExchangeName.nse),
            (orders["product"] == "CNC") & (orders["exchange"] == ExchangeName.nse),
            (orders["exchange"] == ExchangeName.nfo)
            & (orders["security_type"] == "FUT"),
            (orders["exchange"] == ExchangeName.nfo)
            & (orders["security_type"] == "OPT"),
        ]

        brokerage_charges_choices = [
            cm_charges * orders.quantity * orders.average_price,
            0,
            fo_charges,
            fo_charges,
        ]

        orders.loc[:, Order.brokerage_charges] = np.select(
            charges_condition, brokerage_charges_choices, default=0
        )

        stt_charges_choices = [
            0.00025 * (orders.sell_value),
            0.001 * (orders.quantity * orders.average_price),
            0.000125 * (orders.sell_value),
            0.000625 * (orders.sell_value),
        ]

        orders.loc[:, Order.stt_charges] = np.select(
            charges_condition, stt_charges_choices, default=0
        )

        exchange_charges_choices = [
            0.0000325 * (orders.quantity * orders.average_price),
            0.0000325 * (orders.quantity * orders.average_price),
            0.000019 * (orders.quantity * orders.average_price),
            0.00053 * (orders.quantity * orders.average_price),
        ]

        orders.loc[:, Order.exchange_transaction_charges] = np.select(
            charges_condition, exchange_charges_choices, default=0
        )

        stamp_charges_choices = [
            0.00003 * (orders.buy_value),
            0.00015 * (orders.buy_value),
            0.00002 * (orders.buy_value),
            0.00003 * (orders.buy_value),
        ]

        orders.loc[:, Order.stamp_charges] = np.select(
            charges_condition, stamp_charges_choices, default=0
        )

        orders.loc[:, Order.gst_charges] = 0.18 * (
            orders[Order.exchange_transaction_charges] + orders[Order.brokerage_charges]
        )

        orders.loc[:, Order.total_charges] = (
            orders[Order.stt_charges]
            + orders[Order.exchange_transaction_charges]
            + orders[Order.stamp_charges]
            + orders[Order.gst_charges]
            + orders[Order.brokerage_charges]
        )

        return orders

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        data = {}

        data["order_id"] = order_id
        data["price"] = price
        data["order_type"] = order_type
        data["variety"] = "regular"
        data["trigger_price"] = trigger_price

        self.modify_order(data)

    def modify_orders_till_complete(self, orders_placed, sleep_time=10):
        modification_count = {}
        while 1:
            time.sleep(sleep_time)
            orders = self.orders()

            orders = orders[orders.order_id.isin(orders_placed)]
            orders = orders[~orders.status.isin(["REJECTED", "CANCELLED", "COMPLETE"])]

            if len(orders) == 0:
                Constants.logger.info("ALL orders have been completed")
                break

            orders = orders.to_dict("records")
            for order in orders:
                order_id = order["order_id"]

                ltp = self.get_ltp(order["exchange"], order["tradingsymbol"])
                order["price"] = ltp
                order["order_type"] = "LIMIT"
                self.modify_order(order)

                if order_id not in modification_count:
                    modification_count[order_id] = 1
                else:
                    modification_count[order_id] += 1

                time.sleep(0.1)

                if modification_count[order_id] > 5:
                    order["order_type"] = "MARKET"
                    order["price"] = 0
                    Constants.logger.info("Placing MARKET order [{}]".format(order))
                    self.modify_order(order)
