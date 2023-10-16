from datetime import time, datetime, timedelta
from pathlib import Path
import tomllib

from .base import BaseTradingCalendar


class FuturesTradingCalendar(BaseTradingCalendar):

    def init_config(self):
        config_file_path = Path(__file__).parent / 'data' / 'futures.toml'
        self.config = tomllib.loads(config_file_path.read_text(encoding='utf-8'))
        # tips
        #   这里的日期为自然日，非交易结算日
        #   周末没有日盘与夜盘，程序逻辑排除
        self.start_date = self.config['start_date']
        self.end_date = self.config['end_date']

        # Special cases
        self.no_day_trading_dates = set(self.config['holiday_dates'])
        self.no_night_trading_dates = set(self.config['holiday_dates']) | set(self.config['no_night_trading_dates'])

    def get_trading_day(self, dt: datetime):
        dt_date = dt.date()
        dt_time = dt.time()

        # 日盘
        if time(3, 0) <= dt_time < time(18, 0):
            if self.has_day_trading(dt_date):
                return dt_date
            else:
                return None

        # 夜盘，深夜
        elif dt_time >= time(18, 0):
            if self.has_night_trading(dt_date):
                return self.next_trading_day(dt_date)
            else:
                return None

        # 夜盘，凌晨
        elif dt_time < time(3, 0):
            d = dt_date - timedelta(days=1)
            if self.has_night_trading(d):
                return self.next_trading_day(d)
            else:
                return None



