from quantplay.broker.xts import XTS
from quantplay.utils.constant import timeit


class Symphony(XTS):
    xts_interactive = "https://developers.symphonyfintech.in"
    xts_market = "https://developers.symphonyfintech.in"

    @timeit(MetricName="Symphony:__init__")
    def __init__(self, api_secret=None, api_key=None):
        super().__init__(
            api_secret=api_secret,
            api_key=api_key,
            root_interactive=self.xts_interactive,
            root_market=self.xts_market,
        )
