import numpy as np
import plotly.graph_objects as go
import pandas as pd
from quantplay.reporting.visuals import VisualReport
from quantplay.services.market import Market
import matplotlib.pyplot as plt
import inspect
import typing
from quantplay.reporting.strategy_report import StrategyReport

market = Market()


class TradeLens:

    @staticmethod
    def plot(dataset, interval, symbol):
        symbol = "BANKNIFTY2111432100PE"
        df = pd.read_csv(f"~/.quantplay/{dataset}/{interval}/{symbol}.csv")

        fig = go.Figure(data=go.Ohlc(x=df['date'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']))
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.show()

    @staticmethod
    def generate_report(trades, columns=None):
        response = StrategyReport.generate_report(trades)
        result = pd.DataFrame(response)

        if columns:
            result = result[columns]
        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):  # more options can be specified also
            print(result)
    @staticmethod
    def max_drawdowns(trades):
        trades = trades.sort_values("order_timestamp")
        temp_df = trades[['order_timestamp', 'profit']]
        
        temp_df.loc[:,'order_timestamp'] = pd.to_datetime(temp_df['order_timestamp'])
        temp_df.loc[:, "date_only"] = trades.order_timestamp.dt.date
        temp_df = temp_df.groupby(["date_only"])["profit"].sum().reset_index()
        temp_df = temp_df.sort_values("date_only")
        

        for j in range(0, 5):
            temp_df.loc[:, 'balance'] = temp_df.profit.cumsum()
            temp_df.loc[:, 'running_max_balance'] = np.maximum.accumulate(
                temp_df.balance)
            temp_df.loc[:, 'drawdowns'] = temp_df.running_max_balance - \
                temp_df.balance

            max_drawdown = np.max(temp_df.drawdowns)
            end_index = None
            for i in range(0, len(temp_df)):
                end_index = len(temp_df) - 1 - i
                if temp_df.iloc[end_index]['drawdowns'] != max_drawdown:
                    continue

                start_index = end_index
                while temp_df.iloc[start_index - 1]['running_max_balance'] == temp_df.iloc[start_index][
                        'running_max_balance']:
                    start_index = start_index - 1

                print("Max drawdown {} from {} till {} amount {}".format(j,
                                                                         temp_df.iloc[start_index]['date_only'],
                                                                         temp_df.iloc[end_index]['date_only'],
                                                                         max_drawdown))

                temp_df = temp_df.drop(temp_df.index[start_index:end_index+1])
                break

    @staticmethod
    def analyse(trades, disable_metrics=[]):
        trades.loc[:, 'date'] = pd.to_datetime(trades.date)
        exchanges = list(trades.exchange.unique())
        trades.loc[:, 'segment'] = np.where(
            "PE" == trades.tradingsymbol.str[-2:], "PE", "CE")

        trades.loc[:, 'hour'] = trades.date.dt.hour
        trades.loc[:, "day_of_week"] = trades.date.dt.day_name()

        if "hour" not in disable_metrics:
            print(trades.groupby('hour').profit.mean())

        if "day_of_week" not in disable_metrics:
            print(trades.groupby('day_of_week').profit.mean())

        if "hour:day_of_week" not in disable_metrics:
            print(trades.groupby(['hour', 'day_of_week']).profit.mean())

        if len(exchanges) == 1 and exchanges[0] == "NFO":
            if "segment" not in disable_metrics:
                print(trades.groupby('segment').profit.mean())
            if "segment:day_of_week" not in disable_metrics:
                print(trades.groupby(['segment', 'day_of_week']).profit.mean())
            if "hour:segment" not in disable_metrics:
                print(trades.groupby(['hour', 'segment']).profit.mean())

        trades.loc[:, 'trade_return'] = trades.profit / trades.exposure
        trades.loc[:, 'time'] = trades.order_timestamp.dt.time.astype(str)

        if "time" not in disable_metrics:
            print("Trade return by time")
            print(trades.groupby('time').trade_return.mean())

        trades.loc[:, 'trade_return'] = trades.close_price / \
            trades.entry_price - 1
        print("Mean return of trades")
        print(trades.trade_return.mean())

        trades.loc[:, 'week_number'] = (
            trades.order_timestamp.dt.day / 7).astype(int)
        if "week_number" not in disable_metrics:
            print("profit by week number")
            print(trades.groupby('week_number').profit.mean())

    @staticmethod
    def show_report(trades):
        trades.loc[:, 'order_timestamp'] = pd.to_datetime(
            trades.order_timestamp)
        VisualReport.display_profit_report(trades)
        VisualReport.display_balance_report(trades, 'tt')

    @staticmethod
    def load_tradingsymbol(trades):
        security_types = list(trades.security_type.unique())
        symbols_by_security_type = {}
        for security_type in security_types:
            symbols_by_security_type[security_type] = list(
                trades[trades.security_type ==
                       security_type].tradingsymbol.unique()
            )

        market_data = market.data(
            interval="minute",
            symbols_by_security_type=symbols_by_security_type
        )

        return market_data

    @staticmethod
    def plot_pnl(trade_data, check_date, plot_graph=False):
        testing = trade_data[trade_data.date_only == check_date]
        all_dates = testing.date.unique()
        all_symbols = testing.symbol.unique()
        for symbol in all_symbols:
            dates = testing[testing.symbol == symbol].date.unique()
            dates_to_add = list(set(all_dates) - set(dates))
            t_df = [{'date': date_value,
                     'symbol': symbol} for date_value in dates_to_add]
            t_df = pd.DataFrame(t_df)
            testing = pd.concat([testing, t_df])
        testing = testing.sort_values(["symbol", "date"])
        testing.loc[:, 'date_only'] = pd.to_datetime(testing.date.dt.date)
        testing.loc[:, 'pnl'] = testing.groupby(
            ['symbol', 'date_only']).pnl.ffill()

        testing = testing.groupby('date').pnl.sum().reset_index()

        if plot_graph:
            plt.plot(testing.date, testing.pnl)
            plt.show(block=True)
        return {
            "minimum_pnl": int(testing.pnl.min()),
            "maximum_pnl": int(testing.pnl.max())
        }

    @staticmethod
    def analyze_pnl(trades, start_date, end_date):
        trades = trades[trades.date_only.astype(str) >= start_date]
        trades = trades[trades.date_only.astype(str) <= end_date]

        data = TradeLens.load_tradingsymbol(trades)

        trades.loc[:, "date_only"] = pd.to_datetime(trades.date.dt.date)
        data.loc[:, 'date_only'] = pd.to_datetime(data.date.dt.date)

        trade_data = pd.merge(data,
                              trades[['symbol', 'date_only', 'order_timestamp', 'closing_timestamp', 'entry_price',
                                      'transaction_type', 'close_price', 'quantity']],
                              how="left",
                              left_on=['symbol', 'date_only'],
                              right_on=['symbol', 'date_only'])

        trade_data = trade_data[trade_data.date >= trade_data.order_timestamp]
        trade_data = trade_data[trade_data.date < trade_data.closing_timestamp]
        trade_data.loc[:, 'close'] = np.where(
            ((trade_data.transaction_type == "SELL") & (trade_data.close > trade_data.close_price) & (
                trade_data.date >= trade_data.closing_timestamp)),
            trade_data.close_price, trade_data.close)
        trade_data.loc[:, 'close'] = np.where(
            ((trade_data.transaction_type == "BUY") & (trade_data.close < trade_data.close_price) & (
                trade_data.date >= trade_data.closing_timestamp)),
            trade_data.close_price, trade_data.close)
        trade_data.loc[:, 'pnl'] = np.where(trade_data.transaction_type == "SELL",
                                            trade_data.entry_price - trade_data.close,
                                            trade_data.close - trade_data.entry_price)
        trade_data.loc[:, 'pnl'] = trade_data.pnl * trade_data.quantity

        check_dates = trade_data.date_only.unique()
        trade_analysis = []
        for check_date in check_dates:
            date_only = str(check_date).split("T")[0]
            response = TradeLens.plot_pnl(trade_data, date_only)
            trade_analysis.append({
                "date_only": date_only,
                "backtesting_pnl": trades[trades.date_only.astype(str) == date_only].profit.sum(),
                "minimum_pnl": response["minimum_pnl"]
            })

        return pd.DataFrame(trade_analysis)

    @staticmethod
    def validate_alpha(day_candles, alpha_name, num_buckets=10):
        """Validate alphas by bucketing them into 10 buckets and checking the returns

        Args:
            day_candles (DataFrame): Dataframe containing day candles
            alpha (string): name of the alpha
            num_buckets (int, optional): No of brackets required. Defaults to 10.
        """
        try:
            alpha_bucket_name = "{}_bucket".format(alpha_name)

            day_candles.loc[:, 'liquidity'] = day_candles.volume*day_candles.close
            

            day_candles.loc[:, 'liquidity_20'] = day_candles.groupby('symbol')['liquidity'].transform(
            lambda x: x.rolling(20).mean())
            
            day_candles.loc[:, "liquidity_rank"] = day_candles.groupby("date")[
                "liquidity_20"
            ].rank(ascending=False)

            day_candles.loc[:, "is_top500"] = np.where(
                (day_candles["liquidity_rank"] <= 500), True, False
            )

            day_candles.loc[:, "intraday_return"] = (
                day_candles.close / day_candles.open - 1
            )
            day_candles.loc[
                :, "next_day_intraday_return"
            ] = day_candles.intraday_return.shift(-1)

            day_candles.loc[:, alpha_bucket_name] = 1 + 10 * day_candles.groupby(
                ["is_top500", "date"]
            )[alpha_name].rank(method="first", pct=True)

            day_candles.loc[:, alpha_bucket_name] = np.where(
                day_candles["is_top500"] == False,
                np.nan,
                day_candles[alpha_bucket_name],
            )

            day_candles.loc[:, alpha_bucket_name] = (
                day_candles[alpha_bucket_name]
                .replace([np.inf, -np.inf, np.nan], 0)
                .astype(int)
                .replace([0], np.nan)
                .replace([num_buckets + 1], num_buckets)
            )

            # plotting
            t_df = (
                day_candles.groupby(alpha_bucket_name)
                .next_day_intraday_return.mean()
                .reset_index()
            )

            plt.clf()
            plt.title(f"{alpha_name} intraday return analysis")
            plt.bar(t_df[alpha_bucket_name],
                    t_df.next_day_intraday_return)
            plt.show()

        except Exception as e:
            print(e)
