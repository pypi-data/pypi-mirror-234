import pandas as pd

from quantplay.broker.generics.broker import Broker
from quantplay.utils.constant import Constants, timeit
from quantplay.broker.iifl_utils.IIFLapis.IIFLapis import IIFLClient


class IIFL(Broker):

    @timeit(MetricName="IIFL:__init__")
    def __init__(self,  client_code=None, passwd=None, dob=None, email_id=None, contact_number=None, jwt=None, appName=None, appSource=None, userKey=None, encrKey=None, ocpKey=None):
        super(IIFL, self).__init__()

        self.client_code = client_code
        self.passwd = passwd
        self.dob = dob

        self.email_id = email_id
        self.contact_number = contact_number

        self.appName = appName
        self.appSource = appSource
        self.userKey = userKey
        self.encrKey = encrKey
        self.ocpKey = ocpKey

        try:
            self.wrapper = IIFLClient(client_code=client_code, passwd=passwd, dob=dob, email_id=email_id, contact_number=contact_number,
                                      jwt=jwt, appName=appName, appSource=appSource, userKey=userKey, encrKey=encrKey, ocpKey=ocpKey)

            self.wrapper.client_login()
        except Exception as e:
            print("Error")
            raise e

    def account_summary(self):
        margin_api = self.wrapper.margin(self.client_code)

        response = {
            # TODO: Get PNL
            "pnl": 0,
            "margin_used": margin_api["EquityMargin"]["Mgn4Position"],
            "margin_available": margin_api["EquityMargin"]["GrossMargin"],
            "margin_pending_orders": margin_api["EquityMargin"]["Mgn4PendOrd"],
            "Ledger_balance": margin_api["EquityMargin"]["Lb"],

        }

    def profile(self):
        api_response = self.wrapper.profile(
            client_id=self.client_code)

        response = {
            "user_id": api_response["ClientCode"],
            "full_name": api_response["ClientName"],
            # "segments": api_response["ClientExchangeDetailsList"],
        }

        return response

    def positions(self):
        api_response = self.wrapper.net_positions(
            self.client_code)["NetPositionDetail"]

        return api_response

    def holdings(self):
        resp = self.wrapper.holdings(self.client_code)

        return resp

    def orders(self):
        self.wrapper.order_book(self.client_code)

    def get_exchange(self, exchange):
        exchange_code_map = {
            "NSE": "N",
            "BSE": "B",
            "MCX": "M",
        }

        if exchange not in exchange_code_map:
            raise KeyError(
                "INVALID_EXCHANGE: Exchange not in ['NSE','BSE','MCX']"
            )
        return exchange_code_map[exchange]

    def get_exchange_type(self, exch_type):
        exchange_type_code_map = {
            "CASH": "C",
            "DERIVATIVE": "D",
            "CURRENCY": "U"
        }

        # if exchange not in exchange_code_map:
        #     raise KeyError(
        #         "INVALID_EXCHANGE: Exchange not in ['NSE','BSE','MCX']"
        #     )
        # return exchange_code_map_code[exchange]

    def get_symbol(self, exchange, symbol):

        scrip_data = pd.read_csv(
            "http://content.indiainfoline.com/IIFLTT/Scripmaster.csv")
        scripcode = int(scrip_data.loc[scrip_data['Name'] ==
                        symbol].loc[scrip_data['Exch'] == exchange]['Scripcode'])

        return scripcode

    def get_ltp(self, exchange, symbol, exch_type="C"):
        scripcode = self.get_symbol(exchange, symbol)
        exchange_code = self.get_exchange(exchange)
        req_list = [
            {"Exch": exchange_code, "ExchType": exch_type, "ScripCode": scripcode}]
        count = len(req_list)
        response = self.wrapper.fetch_market_feed(
            req_list=req_list, count=count, client_id="client_code")

        ltp = response["Data"]["LastRate"]

        return ltp
