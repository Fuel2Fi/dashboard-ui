class ExitStrategy:
    def __init__(self, trailing_threshold_pct=5.0):
        """
        Initialize trailing stop parameters.
        """
        self.trailing_threshold_pct = trailing_threshold_pct
        self.high_price = None
        self.in_position = False

    def mark_entry(self, entry_price, date=None):
        """
        Call this when you enter a position.
        """
        self.in_position = True
        self.high_price = entry_price
        if date:
            print(f"[ENTRY] Entered position at {entry_price} on {date}")
        else:
            print(f"[ENTRY] Entered position at {entry_price}")

    def check_exit_signal(self, price, date):
        """
        Only checks exit if in position.
        Returns True if exit triggered, False otherwise.
        """
        if not self.in_position:
            print(f"[SKIP] No position active on {date}")
            return False

        # Update high price if new high
        if price > self.high_price:
            print(f"[UPDATE] New high price {price} on {date}")
            self.high_price = price
            return False

        # Calculate percentage drop
        drop_pct = ((self.high_price - price) / self.high_price) * 100

        if drop_pct >= self.trailing_threshold_pct:
            print(f"[EXIT] Trailing stop triggered: Price dropped {drop_pct:.2f}% from high {self.high_price} on {date}")
            # Reset after exit
            self.high_price = None
            self.in_position = False
            return True
        else:
            return False
