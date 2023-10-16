from datetime import date, datetime, timedelta
from pathlib import Path
import tomllib

from .base import BaseTradingCalendar


class StockTradingCalendar(BaseTradingCalendar):

    def init_config(self):
        config_file_path = Path(__file__).parent / 'data' / 'stock.toml'
        self.config = tomllib.loads(config_file_path.read_text(encoding='utf-8'))

        # tips
        #   这里的日期为自然日，非交易结算日
        #   周末没有日盘与夜盘，程序逻辑排除
        self.start_date = self.config['start_date']
        self.end_date = self.config['end_date']

        # Special cases
        self.no_day_trading_dates = set(self.config['holiday_dates'])

    def has_night_trading(self, d: date):
        return False

    def get_trading_day(self, dt: datetime):
        dt_date = dt.date()
        if self.has_day_trading(dt_date):
            return dt_date
        else:
            return None
