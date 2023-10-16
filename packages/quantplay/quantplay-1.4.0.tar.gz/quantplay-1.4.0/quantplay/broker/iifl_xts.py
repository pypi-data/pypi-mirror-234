from quantplay.broker.xts import XTS
from quantplay.utils.constant import timeit


class IIFL(XTS):
    xts_interactive = "https://ttblaze.iifl.com"
    xts_market = "https://ttblaze.iifl.com/apimarketdata"

    @timeit(MetricName="Symphony:__init__")
    def __init__(self, api_secret=None, api_key=None, wrapper=None, ClientID=None):
        super().__init__(
            api_secret=api_secret,
            api_key=api_key,
            root_interactive=self.xts_interactive,
            root_market=self.xts_market,
            wrapper=wrapper,
            ClientID=ClientID,
        )
