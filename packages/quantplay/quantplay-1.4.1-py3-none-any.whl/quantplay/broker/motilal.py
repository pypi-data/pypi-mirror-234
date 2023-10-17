import copy
import hashlib
import requests
import json
import time
import pandas as pd

from quantplay.utils.constant import Constants, timeit, OrderType
from quantplay.config.qplay_config import QplayConfig
from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException
import numpy as np
import pyotp
import websocket
import _thread as thread
import threading
import binascii
from quantplay.utils.pickle_utils import PickleUtils
from quantplay.exception.exceptions import (
    QuantplayOrderPlacementException,
    retry_exception,
    RetryableException,
)
from retrying import retry
from quantplay.wrapper.aws.s3 import S3Utils


class Motilal(Broker):
    user_id = "motilal_user_id"
    api_key = "motilal_api_key"
    password = "motilal_password"
    auth_token = "motilal_auth_token"
    two_factor_authentication = "motilal_2FA"
    secret_key = "motilal_secret_key"

    headers = {
        "Accept": "application/json",
        "User-Agent": "MOSL/V.1.1.0",
        "SourceId": "WEB",
        "MacAddress": "00:50:56:BD:F4:0B",
        "ClientLocalIp": "192.168.165.165",
        "ClientPublicIp": "106.193.137.95",
        "osname": "Ubuntu",
        "osversion": "10.0.19041",
        "devicemodel": "AHV",
        "manufacturer": "DELL",
        "productname": "Your Product Name",
        "productversion": "Your Product Version",
        "installedappid": "AppID",
        "browsername": "Chrome",
        "browserversion": "105.0",
    }

    @timeit(MetricName="Motilal:__init__")
    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=2,
        retry_on_exception=retry_exception,
    )
    def __init__(
        self,
        is_uat=False,
        headers=None,
        load_instruments=True,
        user_id=None,
        password=None,
        api_key=None,
        two_fa=None,
        totp=None,
        order_updates=None,
    ):
        super(Motilal, self).__init__()
        self.order_updates = order_updates

        self.instrument_data_by_exchange = {}

        uat = ""
        if is_uat:
            uat = "uat"

        self.url = (
            "https://{}openapi.motilaloswal.com/rest/login/v3/authdirectapi".format(uat)
        )
        self.otp_url = (
            "https://{}openapi.motilaloswal.com/rest/login/v3/resendotp".format(uat)
        )
        self.verify_otp_url = (
            "https://{}openapi.motilaloswal.com/rest/login/v3/verifyotp".format(uat)
        )
        self.ltp_utl = (
            "https://{}openapi.motilaloswal.com/rest/report/v1/getltpdata".format(uat)
        )
        self.place_order_url = (
            "https://{}openapi.motilaloswal.com/rest/trans/v1/placeorder".format(uat)
        )
        self.get_profile_url = (
            "https://{}openapi.motilaloswal.com/rest/login/v1/getprofile".format(uat)
        )
        self.margin_summary_url = "https://{}openapi.motilaloswal.com/rest/report/v1/getreportmarginsummary".format(
            uat
        )
        self.modify_order_url = (
            "https://{}openapi.motilaloswal.com/rest/trans/v2/modifyorder".format(uat)
        )
        self.order_book_url = (
            "https://{}openapi.motilaloswal.com/rest/book/v1/getorderbook".format(uat)
        )
        self.cancel_order_url = (
            "https://{}openapi.motilaloswal.com/rest/trans/v1/cancelorder".format(uat)
        )
        self.positions_url = (
            "https://{}openapi.motilaloswal.com/rest/book/v1/getposition".format(uat)
        )
        self.order_details_url = "https://{}openapi.motilaloswal.com/rest/book/v2/getorderdetailbyuniqueorderid".format(
            uat
        )

        try:
            if headers:
                self.headers = headers
            else:
                self.generate_token(user_id, password, api_key, two_fa, totp)
            profile = self.profile()
            self.user_id = profile["user_id"]
        except binascii.Error as e:
            raise InvalidArgumentException("Invalid TOTP key provided")
        except InvalidArgumentException as e:
            raise
        except Exception as e:
            raise RetryableException(str(e))

        if load_instruments:
            self.load_instrument()

        self.order_type_sl = "STOPLOSS"
        self.nfo_exchange = "NSEFO"
        self.exchange_code_map = {"NFO": "NSEFO", "CDS": "NSECD", "BFO": "BSEFO"}

    def update_headers(self):
        Constants.logger.info("Updating headers")
        quantplay_config = QplayConfig.get_config()

        auth_token = quantplay_config["DEFAULT"][Motilal.auth_token]
        api_key = quantplay_config["DEFAULT"][Motilal.api_key]
        user_id = quantplay_config["DEFAULT"][Motilal.user_id]

        self.headers["vendorinfo"] = user_id
        self.headers["Authorization"] = auth_token
        self.headers["ApiKey"] = api_key

        self.user_id = user_id

    @timeit(MetricName="Motilal:load_file_by_url")
    def load_file_by_url(self, exchange):
        data_url = "https://openapi.motilaloswal.com/getscripmastercsv?name={}".format(
            exchange
        )
        df = pd.read_csv(data_url)
        self.instrument_data_by_exchange[exchange] = df

    @timeit(MetricName="Motilal:load_instrument")
    def load_instrument(self):
        try:
            self.symbol_data = PickleUtils.load_data("motilal_instruments")
            Constants.logger.info("[LOADING_INSTRUMENTS] loading data from cache")
        except Exception as e:
            self.instrument_data = S3Utils.read_csv(
                "quantplay-market-data",
                "symbol_data/motilal_instruments.csv",
                read_from_local=False,
            )
            self.initialize_symbol_data(save_as="motilal_instruments")

        self.initialize_broker_symbol_map()

    def get_symbol(self, symbol, exchange=None):
        if symbol not in self.quantplay_symbol_map:
            return symbol
        return self.quantplay_symbol_map[symbol]

    def get_order_type(self, order_type):
        if order_type == OrderType.sl:
            return "STOPLOSS"
        return order_type

    def get_exchange(self, exchange):
        if exchange in self.exchange_code_map:
            return self.exchange_code_map[exchange]

        return exchange

    def get_product(self, product):
        if product == "CNC":
            return "DELIVERY"
        elif product == "NRML":
            return "NORMAL"
        elif product == "DELIVERY":
            return "DELIVERY"
        return "NORMAL"

    def place_order_quantity(self, quantity, tradingsymbol, exchange):
        lot_size = self.get_lot_size(exchange, tradingsymbol)
        quantity_in_lots = int(quantity / lot_size)

        return quantity_in_lots

    def get_lot_size(self, exchange, tradingsymbol):
        tradingsymbol = self.get_symbol(tradingsymbol, exchange=exchange)
        if exchange == "NSEFO":
            exchange = "NFO"
        elif exchange == "BSEFO":
            exchange = "BFO"
        try:
            return int(
                self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["lot_size"]
            )
        except Exception as e:
            Constants.logger.error(
                "[GET_LOT_SIZE] unable to get lot size for {} {}".format(
                    exchange, tradingsymbol
                )
            )
            raise e

    def generate_token(self, user_id, password, api_key, two_fa, totp):
        current_totp = pyotp.TOTP(totp).now()
        Constants.logger.info("TOTP is {}".format(current_totp))
        # initializing string
        str = "{}{}".format(password, api_key)
        result = hashlib.sha256(str.encode())

        data = {
            "userid": user_id,
            "password": result.hexdigest(),
            "2FA": two_fa,
            "totp": current_totp,
        }

        self.headers["ApiKey"] = api_key
        self.headers["vendorinfo"] = user_id
        response = requests.post(self.url, headers=self.headers, data=json.dumps(data))

        resp_json = response.json()
        if "status" in resp_json and resp_json["status"] == "ERROR":
            raise InvalidArgumentException(resp_json["message"])
        Constants.logger.info("login response {}".format(resp_json))
        self.headers["Authorization"] = resp_json["AuthToken"]
        self.user_id = user_id

    def send_otp(self):
        response = requests.post(self.otp_url, headers=self.headers).json()
        Constants.logger.info(response)
        return response

    def verify_otp(self, otp):
        data = {"otp": otp}
        response = requests.post(
            self.verify_otp_url, headers=self.headers, data=json.dumps(data)
        ).json()
        Constants.logger.info(response)
        return response

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
    )
    def get_ltp(self, exchange=None, tradingsymbol=None):
        tradingsymbol = self.get_symbol(tradingsymbol)
        token = self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["token"]
        exchange = self.get_exchange(exchange)
        data = {
            "userid": self.user_id,
            "exchange": exchange,
            "scripcode": token,
        }

        Constants.logger.info("[GET_LTP_REQUEST] response {}".format(data))
        response = requests.post(
            self.ltp_utl, headers=self.headers, data=json.dumps(data)
        )
        Constants.logger.info("[GET_LTP_RESPONSE] response {}".format(response.json()))
        return response.json()["data"]["ltp"] / 100.0

    def get_orders(self, order_status=None, order_type=None):
        response = (requests.post(self.order_book_url, headers=self.headers)).json()
        if response["status"] == "ERROR":
            Constants.logger.info(
                "Error while fetching order book [{}]".format(response["message"])
            )
            raise Exception(response["message"])
        orders = response["data"]

        if order_status:
            orders = [a for a in orders if a["orderstatus"] == order_status]

        if order_type:
            orders = [a for a in orders if a["ordertype"] == order_type]

        return orders

    def get_positions(self):
        response = (requests.post(self.positions_url, headers=self.headers)).json()
        if response["status"] == "ERROR":
            Constants.logger.info(
                "Error while fetching order book [{}]".format(response["message"])
            )
            raise Exception(response["message"])

        positions = response["data"]

        return positions

    def modify_price(self, order_id, price, trigger_price=None, order_type=None):
        orders = self.orders()
        orders = orders[orders["order_id"] == order_id]

        if len(orders) != 1:
            Constants.logger.error(
                "[ORDER_NOT_FOUND] invalid modify request for {}".format(order_id)
            )
            return
        orders.loc[:, "last_modified_time"] = orders.last_modified_time.astype(str)
        order = orders.to_dict("records")[0]

        order["price"] = price
        if trigger_price != None:
            order["trigger_price"] = trigger_price

        if order["order_type"] == "SL":
            order["order_type"] = "STOPLOSS"

        print(order)
        self.modify_order(order)

    def modify_order(self, order):
        data = {
            "uniqueorderid": order["order_id"],
            "newordertype": order["order_type"].upper(),
            "neworderduration": order["order_duration"].upper(),
            "newquantityinlot": int(order["pending_quantity"] / order["lot_size"]),
            # "newdisclosedquantity": 0,
            "newprice": order["price"],
        }

        if "trigger_price" in order:
            data["newtriggerprice"] = order["trigger_price"]
        if "quantity_traded_today" in order:
            data["qtytradedtoday"] = order["quantity_traded_today"]
        if "last_modified_time" in order:
            data["lastmodifiedtime"] = order["last_modified_time"]

        if "exchange" in order and order["exchange"] == "MCX":
            data["newquantityinlot"] = int(order["totalqtyremaining"])

        try:
            Constants.logger.info("[MODIFYING_ORDER] order [{}]".format(data))
            response = requests.post(
                self.modify_order_url, headers=self.headers, data=json.dumps(data)
            ).json()
            Constants.logger.info("[MODIFY_ORDER_RESPONSE] {}".format(response))
        except Exception as e:
            exception_message = (
                "[ORDER_MODIFICATION_FAILED] for {} failed with exception {}".format(
                    order["uniqueorderid"], e
                )
            )
            Constants.logger.error("{}".format(exception_message))

    def cancel_order(self, unique_order_id):
        data = {"uniqueorderid": unique_order_id}

        try:
            Constants.logger.info("Cancelling order [{}]".format(unique_order_id))
            response = requests.post(
                self.cancel_order_url, headers=self.headers, data=json.dumps(data)
            ).json()
            Constants.logger.info("Cancel order response [{}]".format(response))
        except Exception as e:
            exception_message = (
                "[ORDER_CANCELLATION_FAILED] unique_order_id {} exception {}".format(
                    unique_order_id, e
                )
            )
            Constants.logger.error(exception_message)

    def get_profile(self):
        response = requests.post(
            self.get_profile_url,
            headers=self.headers,
            data=json.dumps({"Clientcode": self.headers["vendorinfo"]}),
        ).json()
        if response["status"] == "ERROR":
            raise Exception(response["message"])

        return response["data"]

    def margin_summary(self):
        response = requests.post(
            self.margin_summary_url,
            headers=self.headers,
            data=json.dumps({"Clientcode": self.headers["vendorinfo"]}),
        ).json()
        if response["status"] == "ERROR":
            raise Exception(response["message"])

        return response["data"]

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
        order_type = self.get_order_type(order_type)
        product = self.get_product(product)
        tradingsymbol = self.get_symbol(tradingsymbol)

        actual_exchange = copy.deepcopy(exchange)
        if actual_exchange == "NSEFO":
            actual_exchange = "NFO"
        elif actual_exchange == "BSEFO":
            actual_exchange = "BFO"
        token = self.symbol_data["{}:{}".format(actual_exchange, tradingsymbol)][
            "token"
        ]

        exchange = self.get_exchange(exchange)
        quantity = self.place_order_quantity(quantity, tradingsymbol, exchange)

        data = {
            "exchange": exchange,
            "symboltoken": token,
            "buyorsell": transaction_type,
            "ordertype": order_type,
            "producttype": product,
            "orderduration": "DAY",
            "price": price,
            "triggerprice": trigger_price,
            "quantityinlot": quantity,
            "disclosedquantity": 0,
            "amoorder": "N",
            "algoid": "",
            "tag": tag,
        }
        try:
            Constants.logger.info("[PLACING_ORDER] {}".format(json.dumps(data)))
            response = requests.post(
                self.place_order_url, headers=self.headers, data=json.dumps(data)
            ).json()
            Constants.logger.info(
                "[PLACE_ORDER_RESPONSE] {} input {}".format(response, json.dumps(data))
            )
            if response["status"] == "ERROR":
                raise QuantplayOrderPlacementException(response["message"])
            return response["uniqueorderid"]
        except QuantplayOrderPlacementException as e:
            raise e
        except Exception as e:
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)

    def on_message(self, ws, order):
        try:
            order = json.loads(order)
            print(order)

            order["placed_by"] = self.user_id
            order["tag"] = self.user_id
            order["order_id"] = order["orderid"]
            order["exchange_order_id"] = order["order_id"]
            order["transaction_type"] = order["transactiontype"]
            order["quantity"] = int(order["quantity"])
            order["order_type"] = order["ordertype"]

            if order["exchange"] == "NFO":
                order["tradingsymbol"] = self.symbol_map[order["tradingsymbol"]]

            if order["order_type"] == "STOPLOSS_LIMIT":
                order["order_type"] = "SL"

            if "triggerprice" in order and order["triggerprice"] != 0:
                order["trigger_price"] = float(order["triggerprice"])
            else:
                order["trigger_price"] = None

            if order["status"] == "trigger pending":
                order["status"] = "TRIGGER PENDING"
            elif order["status"] == "cancelled":
                order["status"] = "CANCELLED"
            elif order["status"] == "open":
                order["status"] = "OPEN"
            elif order["status"] == "complete":
                order["status"] = "COMPLETE"

            # self.order_updates.put(order)
            print("Final order {}".format(order))
        except Exception as e:
            Constants.logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))
        print(json.dumps(order))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        def run(*args):
            for i in range(300000):
                time.sleep(1)
                print(
                    {
                        "actiontype": "TradeSubscribe",
                        "clientid": self.headers["vendorinfo"],
                    }
                )
                ws.send(
                    json.dumps(
                        {
                            "actiontype": "TradeSubscribe",
                            "clientid": self.headers["vendorinfo"],
                        }
                    )
                )
            time.sleep(1)
            ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())

    def account_summary(self):
        response = {"margin_used": 0}

        margin_summary = self.margin_summary()
        for margin_particular in margin_summary:
            if margin_particular["srno"] == 103:
                response["margin_available"] = margin_particular["amount"]
            if margin_particular["srno"] in [301, 321, 340, 360]:
                response["margin_used"] += margin_particular["amount"]

        response["pnl"] = self.positions().pnl.sum()
        return response

    def profile(self):
        api_response = requests.post(
            self.get_profile_url,
            headers=self.headers,
            data=json.dumps({"Clientcode": self.headers["vendorinfo"]}),
        ).json()
        if api_response["status"] == "ERROR":
            raise Exception(api_response["message"])

        api_response = api_response["data"]
        response = {
            "user_id": api_response["clientcode"],
            "full_name": api_response["name"],
            "segments": api_response["exchanges"],
        }

        return response

    def positions(self):
        response = (requests.post(self.positions_url, headers=self.headers)).json()
        if response["status"] == "ERROR":
            Constants.logger.info(
                "Error while fetching order book [{}]".format(response["message"])
            )
            raise Exception(response["message"])

        positions = response["data"]

        if positions is None or len(positions) == 0:
            return pd.DataFrame(columns=self.positions_column_list)

        positions = pd.DataFrame(positions)
        positions.loc[:, "tradingsymbol"] = positions.symbol

        positions.loc[:, "ltp"] = positions.LTP
        positions.loc[:, "pnl"] = positions.sellamount - positions.buyamount
        positions.loc[:, "pnl"] += (
            positions.buyquantity - positions.sellquantity
        ) * positions.ltp
        positions.loc[:, "quantity"] = positions.buyquantity - positions.sellquantity
        positions.rename(
            columns={
                "productname": "product",
                "sellquantity": "sell_quantity",
                "buyquantity": "buy_quantity",
                "optiontype": "option_type",
            },
            inplace=True,
        )

        positions["exchange"] = positions["exchange"].replace(
            ["NSEFO", "BSEFO"], ["NFO", "BFO"]
        )

        positions = positions[positions.exchange != "BFO"]
        return positions[self.positions_column_list]

    def order_details(self, order_id):

        response = (
            requests.post(
                self.order_details_url,
                headers=self.headers,
                data=json.dumps({"uniqueorderid": order_id}),
            )
        ).json()

    def orders(self, tag=None):
        response = (requests.post(self.order_book_url, headers=self.headers)).json()
        if response["status"] == "ERROR":
            Constants.logger.info(
                "Error while fetching order book [{}]".format(response["message"])
            )
            raise Exception(response["message"])
        orders = response["data"]
        orders = pd.DataFrame(orders)

        positions = self.positions()
        if len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)

        orders.loc[:, "tradingsymbol"] = orders.symbol
        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.rename(
            columns={
                "clientid": "user_id",
                "LTP": "ltp",
                "buyorsell": "transaction_type",
                "averageprice": "average_price",
                "uniqueorderid": "order_id",
                "orderstatus": "status",
                "recordinserttime": "order_timestamp",
                "orderqty": "quantity",
                "triggerprice": "trigger_price",
                "totalqtytraded": "filled_quantity",
                "totalqtyremaining": "pending_quantity",
                "orderduration": "order_duration",
                "lastmodifiedtime": "last_modified_time",
                "qtytradedtoday": "quantity_traded_today",
                "lotsize": "lot_size",
                "ordertype": "order_type",
            },
            inplace=True,
        )
        orders.loc[:, "product"] = np.where(
            orders.producttype == "VALUEPLUS", "MIS", orders.producttype
        )
        orders.loc[:, "product"] = np.where(
            orders["product"] == "DELIVERY", "CNC", orders["product"]
        )
        orders.loc[:, "product"] = np.where(
            orders["product"] == "NORMAL", "NRML", orders["product"]
        )

        orders = orders[orders.last_modified_time != "0"]
        orders.loc[:, "update_timestamp"] = pd.to_datetime(orders.last_modified_time)

        column_list = list(
            set(
                self.orders_column_list
                + [
                    "order_duration",
                    "last_modified_time",
                    "quantity_traded_today",
                    "lot_size",
                ]
            )
        )

        existing_columns = list(orders.columns)
        columns_to_keep = list(set(column_list).intersection(set(existing_columns)))
        orders = orders[columns_to_keep]
        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "SELL", -orders.pnl, orders.pnl
        )

        orders.loc[:, "status"] = np.where(
            ((orders.status == "Confirm") & (orders.trigger_price > 0)),
            "TRIGGER PENDING",
            orders.status,
        )
        orders.loc[:, "status"] = np.where(
            ((orders.status == "Confirm") & (orders.trigger_price == 0)),
            "OPEN",
            orders.status,
        )
        if tag:
            orders = orders[orders.tag == tag]

        orders.status = orders.status.replace(
            ["Traded", "Error", "Cancel", "Rejected"],
            ["COMPLETE", "REJECTED", "CANCELLED", "REJECTED"],
        )
        orders.order_type = np.where(
            orders.order_type == "Stop Loss", "SL", orders.order_type.str.upper()
        )
        orders.exchange = orders.exchange.replace(["NSEFO", "NSECD"], ["NFO", "CDS"])
        orders.loc[:, "order_timestamp"] = pd.to_datetime(orders.order_timestamp)
        #
        return orders
