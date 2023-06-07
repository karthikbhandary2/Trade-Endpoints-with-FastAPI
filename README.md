# Trade-Endpoints-with-FastAPI

### This project is done as a part of the `SteelEye API Developer technical test`

I have used FastAPI and pydantic to solve the problem. Link to the problem: https://github.com/steeleye/recruitment-ext/wiki/API-Developer-Assessment

I have used the provided pydantic schema model that was present in the repo provided. Since it was ok to mock a database to my convinience I create 3 Trades and put them in a dictionary becuase it becomes easy to test(mock). 

I have created an endpoint which is the starting page where it shows the message `API Developer Assessment`

I have created an end point to get trades based on the `trade_id`. In this if trade_id is not present in the database it would raise an `HTTPException`

I have created an end point which has multiple functions. It takes in a search query and returns the result based on the search query. For example, If I give a query as `instrumentid='AMZN'` then it would search the database for the given istrumentid and return the results based on it. This end point take a query related to `trader`, `instrumentname`, `instrumentid`, `assetclass`

I have created 3 more end points which deals with `counterparty`, `price`, and `date`. The counterparty end point takes in a counterparty and checks the database for it and returns the data accordingly.
The price end point takes in a minprice and maxprice and returns the data with price between the given ranges. Finally for the date it does the same thing as the price but with dates.

To the run the code go to the directory the file is present in the `cmd` after the download and type: `uvicorn myapi:app --reload`

Please take a look at the code for furthur understanding.
