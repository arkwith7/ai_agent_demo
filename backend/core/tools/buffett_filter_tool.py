from typing import List, Dict

class BuffettFilterTool:
    def __init__(self, min_roe: float = 15.0):
        self.min_roe = min_roe

    def filter_stocks(self, stocks: List[Dict]) -> List[Dict]:
        filtered_stocks = []
        for stock in stocks:
            if stock.get('roe', 0) >= self.min_roe:
                filtered_stocks.append(stock)
        return filtered_stocks

    def analyze(self, stocks: List[Dict]) -> List[Dict]:
        return self.filter_stocks(stocks)