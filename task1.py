import yfinance as yf
import pandas as pd

class AlgoTrader:
    def __init__(self, symbol, start_date, end_date, capital=5000):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.capital = capital

        print(f"Initial Capital: ${self.capital:.2f}")

        self.data = None
        self.position = 0
        self.buy_price = 0
        self.shares = 0
        self.total_profit = 0

    def fetch_data(self):
        self.data = yf.download(
            self.symbol,
            start=self.start_date,
            end=self.end_date
        )

    def clean_data(self):
        self.data = self.data[~self.data.index.duplicated()]
        if hasattr(self.data.columns, 'nlevels') and self.data.columns.nlevels > 1:
             self.data.columns = self.data.columns.get_level_values(0)
        self.data.ffill(inplace=True)

    def add_indicators(self):
        self.data["MA50"] = self.data["Close"].rolling(window=50).mean()
        self.data["MA200"] = self.data["Close"].rolling(window=200).mean()

    def run_strategy(self):
        for i in range(1, len(self.data)):
            prev_row = self.data.iloc[i - 1]
            curr_row = self.data.iloc[i]

            # golden cross - BUY
            if (
                prev_row["MA50"] < prev_row["MA200"]
                and curr_row["MA50"] > curr_row["MA200"]
                and self.position == 0
            ):
                self.buy_price = curr_row["Close"]
                self.shares = int(self.capital // self.buy_price)
                self.position = 1
                print(f"BUY {self.shares} shares at ${self.buy_price:.2f}")

            # death cross - SELL
            elif (
                prev_row["MA50"] > prev_row["MA200"]
                and curr_row["MA50"] < curr_row["MA200"]
                and self.position == 1
            ):
                sell_price = curr_row["Close"]
                profit = (sell_price - self.buy_price) * self.shares
                self.total_profit += profit
                self.position = 0
                print(f"SELL at ${sell_price:.2f} | Profit: ${profit:.2f}")

        # force close on last day
        if self.position == 1:
            final_price = self.data.iloc[-1]["Close"]
            profit = (final_price - self.buy_price) * self.shares
            self.total_profit += profit
            print(f"FORCE SELL at ${final_price:.2f} | Profit: ${profit:.2f}")

    def evaluate(self):
        print("\n--- Strategy Evaluation ---")

        print(f"Total Profit/Loss: ${self.total_profit:.2f}")
        print(f"Final Portfolio Value: ${self.capital + self.total_profit:.2f}")


trader = AlgoTrader("AAPL", "2018-01-01", "2023-12-31", 5000)

trader.fetch_data()
trader.clean_data()
trader.add_indicators()
trader.run_strategy()
trader.evaluate()
