class ExitStrategy:
    def __init__(self, trailing_stop_pct=1.5, trailing_take_profit_pct=2.0, time_exit_bars=10):
        self.trailing_stop_pct = trailing_stop_pct
        self.trailing_take_profit_pct = trailing_take_profit_pct
        self.time_exit_bars = time_exit_bars
        self.entry_price = None
        self.highest_price = None
        self.lowest_price = None
        self.entry_time = None

    def check_exit_conditions(self, current_price, current_time):
        exit_reason = None
        exit_price = None

        if self.entry_price is None:
            self.entry_price = current_price
            self.highest_price = current_price
            self.lowest_price = current_price
            self.entry_time = current_time
            return None

        # Update high/low watermark
        self.highest_price = max(self.highest_price, current_price)
        self.lowest_price = min(self.lowest_price, current_price)

        # Trailing stop loss for long position
        if current_price <= self.highest_price * (1 - self.trailing_stop_pct / 100):
            exit_reason = "trailing_stop"
            exit_price = current_price

        # Trailing take profit for long position
        elif current_price >= self.entry_price * (1 + self.trailing_take_profit_pct / 100):
            self.entry_price = current_price * (1 - self.trailing_take_profit_pct / 100)
            self.highest_price = current_price

        # Time-based exit
        if self.time_exit_bars and int(current_time[-2:]) >= self.time_exit_bars:
            exit_reason = "time_exit"
            exit_price = current_price

        if exit_reason:
            return {"exit_reason": exit_reason, "exit_price": exit_price}

        return None
