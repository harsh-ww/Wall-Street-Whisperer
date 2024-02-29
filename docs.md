# API Routes
### Company Search
`GET /company?query=<SQUERY>`
**Description**: Used for entering a partial company name and getting a list of all matching tracked & untracked companies
**Status**: IMPLEMENTED
Example Response:
```
[{
name: "Amazon",
ticker: "AMZN",
exchange: "United Kingdom",
tracked: False
},.......]
```
### Company Details
`GET /company/<ticker>`
**Description**: Used for getting data about a company - returns info from the database if tracked - returns stock price from alphavantage
**Status**: PARTIALLY IMPLEMENTED - needs modification to just ticker. Does not currently return stock price
Example Response:
```
[{
name: "Amazon",
ticker: "AMZN",
exchange: "United Kingdom",
tracked: False,
score: ....,
stockPrice: ....
[AlphaVantage data if US]
},.......]
```

### Company News
`GET /articles/<ticker>?from_date=..`
**Description**: Used for getting news articles about a given company
**Status**: PARTIALLY IMPLEMENTED - currently works by company ID. Needs to use news 
Example Response: All data held on news articles

### Tracked Companies List
`GET /company/tracked`
Description: Gets a list of all tracked companies and their data
**Status**: Not implemented

### Tracking a company
`POST /track`
Description: tracks a company in the database
**Status**: Implemented (needs refactor)
Example request body: 
```
{
'ticker_code': 'AMZN.L',
'company_name': 'Amazon Inc',
'common_name': 'Amazon
}
```
Note: not sure why we are passing in company name when this can be obtained on the backend

