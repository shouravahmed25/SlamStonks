from pymongo import MongoClient, DESCENDING

# sudo systemctl start mongod
server_link = 'mongodb://localhost:27017/'
database_name = 'SlamStonks'


def get_analysis():
    my_client = MongoClient(server_link)
    my_db = my_client[database_name]
    col_top10s = my_db['Top10s']
    my_client.server_info()
    top10s = col_top10s.find_one(sort=[('_id', DESCENDING)])
    my_client.close()
    return top10s["Top10"] if top10s else None


def get_chart_analysis():
    my_client = MongoClient(server_link)
    my_db = my_client[database_name]
    col_google_trends = my_db['GoogleTrends']
    my_client.server_info()
    google_trends = col_google_trends.find_one(sort=[('_id', DESCENDING)])
    my_client.close()

    google_trends = google_trends['GoogleTrends']
    tickers = list(google_trends.keys())
    legend = 'Monthly Data'
    the_date = list(google_trends[tickers[0]].keys())
    the_date.reverse()

    return {'legend': legend, 'the_date': the_date, 'tickers': tickers, 'nested_dictionaries': google_trends}


def get_ticker_data(ticker):
    my_client = MongoClient(server_link)
    my_db = my_client[database_name]
    col_stocks = my_db['Stocks']
    my_client.server_info()
    stocks = col_stocks.find_one({"_id": ticker})
    my_client.close()
    return StockInfo(stocks["Data"]) if stocks else None


class StockInfo:

    def __init__(self, info):
        self.symbol = info['Symbol']
        self.name = info['overview']['Name']
        self.market_cap = info['overview']['MarketCapitalization']
        self.fiftytwo_week_high = info['overview']['52WeekHigh']
        self.fiftytwo_week_low = info['overview']['52WeekLow']
        # self.daily = info['daily']

        if info['intraday']:
            intraday = info['intraday']
            self.Dates = []
            self.Values = []
            volumes = []

            intraday_values = []
            for value in intraday.values():
                intraday_values.append(value)
            intraday = intraday_values

            for d in range(len(intraday)):
                if intraday[d]['last']:
                    self.Dates.append(intraday[d]['date'])
                    self.Values.append(intraday[d]['last'])
                    volumes.append(intraday[d]['volume'])

            self.Dates.reverse()
            self.Values.reverse()

            self.avg_vol = sum(volumes) // len(volumes)
            self.avg_price = sum(self.Values) / len(self.Values)
            self.avg_price = round(self.avg_price, 3)

        self.social = info['social']
        self.social_dates = self.social.keys()
        self.social_values = self.social.values()
