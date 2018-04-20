# stock-screener
An interactive jupyter notebook to help you screen your stocks
# Pre-requisites: 
1. chromedriver.exe(included in this repository)
2. Running all the cells of the notebook first and then entering your values.

# PS: 
To actually use this notebook interactively, you need to run all cells first.(IPython Widgets!!!)
Enter the name of the exchange and the ticker next in the space provided and BOOM.

# Use this notebook as your stock screener
The name of the exchange and the ticker symbol of your stock is all you need. 
Enter these in the space provided and let the magic happen!

You'll see the current price first(along with the open price of the stock)
Next, you'll see the candlestick plot of the close prices beginning FY14

You can ask for Fundamentals too. That is just a click away.
Then we have the tech-indicators, I've included four of the most commonly used indicators
# Commodity Channel Index: 
Indicates the strength of movement of price of a ccommodity
# Relative Strength Index: 
Indicates the relative strenght between upward and downward movements
# Moving Average Convergence Divergence: 
Indicates the change in movement based on momentum
# Exponentially Weighted Moving Average: 
14 day moving average with the lag affect removed, that gives more weightage to recent values.

I've created my library that I've imported to separate the actual code from the main notebook.
# Primary Concepts Used:
1. Web Scraping using Beautiful Soup and Selenium
2. Data ingestion - from Quandl and Alphavantage
3. Data Wrangling - Pandas and Numpy
4. Tech-Indicators
5. Data Visualization - Matplotlib 
6. Ipyton Widgets

Next-up: Stock Price Prediction using Machine Learning models! Stay Tuned
