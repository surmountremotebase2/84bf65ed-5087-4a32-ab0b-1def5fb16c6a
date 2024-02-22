from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets we're interested in
        self.tickers = ["SPY", "SH"]  # SPY for long positions, SH for shorting SPY

    @property
    def interval(self):
        # Use daily data for the RSI computation
        return "1day"
    
    @property
    def assets(self):
        # Our trading strategy focuses on SPY and its inverse SH
        return self.tickers

    def run(self, data):
        # Initialize the allocation dict
        allocation_dict = {"SPY": 0, "SH": 0}
        # Utilize data to fetch RSI values for SPY
        rsi_values = RSI("SPY", data["ohlcv"], length=14)  # Compute 14-day RSI for SPY
        
        if not rsi_values:
            # If RSI values are unavailable, log an error and exit the strategy
            log("RSI values could not be computed.")
            return TargetAllocation(allocation_dict)
        
        latest_rsi = rsi_values[-1]  # Obtain the most recent RSI value
        
        # Determine allocation based on RSI
        if latest_rsi > 70:
            # RSI above 70 indicates an overbought scenario, opt for SH (short SPY)
            allocation_dict["SH"] = 1.0  # Allocate 100% to SH
        elif latest_rsi < 30:
            # RSI below 30 indicates an oversold scenario, invest in SPY
            allocation_dict["SPY"] = 1.0  # Allocate 100% to SPY

        # Log the allocation decision
        log(f"RSI: {latest_rsi}, Allocation: {allocation_dict}")

        return TargetAllocation(allocation_dict)