import pandas as pd
import pandas_ta as ta
from tvDatafeed import TvDatafeed, Interval

def main():
    """
    Main function to run the stock screener.
    """
    print("Starting the stock screener...")

    # 1. Data Acquisition
    tv = TvDatafeed()

    # Read NIFTY 50 symbols from file
    try:
        with open('nifty50.txt', 'r') as f:
            symbols = [line.strip() for line in f if line.strip()]
        print(f"Loaded {len(symbols)} symbols from nifty50.txt")
    except FileNotFoundError:
        print("Error: nifty50.txt not found. Please create it with one symbol per line.")
        return

    all_data = {}

    print("Fetching EOD data...")
    for symbol in symbols:
        try:
            # Fetch daily data for the last 100 bars to ensure enough data for MAs
            data = tv.get_hist(symbol=symbol.split(':')[-1], exchange=symbol.split(':')[0], interval=Interval.in_daily, n_bars=100)
            if data is not None and not data.empty:
                all_data[symbol] = data
                print(f"Successfully fetched data for {symbol}")
            else:
                print(f"No data returned for {symbol}")
        except Exception as e:
            print(f"Could not fetch data for {symbol}: {e}")

    if not all_data:
        print("No data was fetched. Exiting.")
        return

    print("Data acquisition complete.")

    # 2. Screening Criteria
    alerts_list = []

    print("\nApplying screening criteria...")
    for symbol, df in all_data.items():
        # Calculate indicators
        df.ta.sma(length=50, append=True)
        # When passing a series to 'close', pandas-ta names the column with the indicator and length, e.g., 'SMA_30'
        df.ta.sma(close=df['volume'], length=30, append=True)

        # Rename columns for clarity
        df.rename(columns={'SMA_50': 'sma_50', 'SMA_30': 'avg_vol_30'}, inplace=True)

        # Get the latest data point
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else latest

        # Apply screening conditions
        condition1 = latest['close'] > latest['sma_50']
        condition2 = latest['volume'] > 2 * latest['avg_vol_30']
        condition3 = latest['high'] >= previous['high']
        condition4 = latest['close'] > latest['high'] - (latest['high'] - latest['low']) * 0.1

        if all([condition1, condition2, condition3, condition4]):
            alerts_list.append(symbol)
            print(f"  [ALERT] {symbol} meets all criteria.")
        else:
            print(f"  {symbol} does not meet all criteria.")

    if not alerts_list:
        print("\nNo stocks met the screening criteria.")
    else:
        print(f"\nScreening complete. Found {len(alerts_list)} stock(s): {alerts_list}")

        # 3. Generate and Save Results
        results_df = pd.DataFrame(alerts_list, columns=['Symbol'])
        results_df.to_csv('scan_results.csv', index=False)
        print("\nResults saved to scan_results.csv")


if __name__ == "__main__":
    main()