# EOD_SCANNER
eod stock scanner

Algorithm: End-of-Day (EOD) Stock Screener
This document outlines a high-level algorithm for an automated end-of-day stock screener for the Indian market (NSE), designed to run after market close and send email alerts.

Prerequisites
Before starting the process, you'll need the following components set up:

A programming language (Python is highly recommended for its powerful data analysis libraries).

A reliable source for EOD stock data ( tvDataFeed).
 

Step 1: Data Acquisition
The first and most critical step is to get the latest EOD data for all stocks you want to screen. This must be done after the market has officially closed (after 3:30 PM IST). A good practice is to schedule the script to run around 6:00 PM IST to ensure all data is final and updated.

Request EOD Data: Make an API call to a financial data provider to retrieve the EOD data for all relevant stocks (e.g., all stocks in the NIFTY 500, or a custom watchlist).

Handle Data Format: The data will likely be in a JSON or CSV format. Use a library like Pandas (if using Python) to parse this data into a structured format like a DataFrame, making it easy to work with.

Store Data Locally: Temporarily save the EOD data to a local file (e.g., eod_data.csv) for quick access in the next steps.

Step 2: Define Screening Criteria
This is where you specify the rules for which stocks you are looking for. The criteria can be based on technical indicators, price action, or volume. For example:

Moving Averages:

stock.close > stock.moving_average_50d (Closing price is above the 50-day Simple Moving Average)

Volume Analysis:

stock.volume > 2 * stock.average_volume_30d (Today's volume is more than double the 30-day average)

Price Action:

stock.high >= stock.previous_day.high (Today's high is greater than or equal to yesterday's high)

stock.close > stock.high - (stock.high - stock.low) * 0.1 (Closing price is in the top 10% of the daily range)

You can combine these criteria using logical AND or OR to create a powerful screening query.

Step 3: Scan the Data
Iterate through the list of stocks (from the DataFrame created in Step 1) and check each one against your defined screening criteria.

Initialize an empty list called alerts_list.

Loop through each stock in your EOD data.

Apply the criteria: For each stock, check if it meets all of the conditions you defined in Step 2.

Add to list: If a stock satisfies all the criteria, add its relevant details (e.g., symbol, closing price, volume, and the criteria it met) to the alerts_list.

Step 4: Generate the STOCK LIST CSV
Once the loop is complete, Created list with stock TICKER of the flagged stocks, and the reason for the alert.

Step 5: SAVE the CSV

Step 6: Automation & Scheduling
For this to be a true "screener," the entire process must be automated to run daily without manual intervention.

Schedule the script: Use a task scheduler (e.g., Cron on Linux, Task Scheduler on Windows) or a cloud function (e.g., AWS Lambda, Google Cloud Functions) to execute the script at a specific time every weekday evening (e.g., 6:00 PM IST).

Logging: Add logging to your script to record when it runs, if it encounters any errors, and which stocks were found. This is crucial for debugging and monitoring the process.
