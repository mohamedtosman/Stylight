# Data Engineer Task

For this assignement you have to process one file and enrich it with data provided by an API, in order to provide high level aggregate info.

The goal is to see how you implement the missing parts of the API, and how you deal with file processing and data structures manipulation.


## Description

### API

There two endpoints that need to be implemented, one that searches for the user_status on a given date,
and another one that returns a city based on IP provided.


`/user_status/<user_id>?date=2017-10-10T10:00:00`
On this endpoint, please provide an implementation that searches the records and based on the date, returns the correct user status at that time.
In case there's no status available for a given date, simply return non-paying.
The valid statuses that should be provided are: paying, canceled or non-paying.

`/ip_city/10.0.0.0`
On this endpoint, please provide an implementation that searched the IP ranges provided, and based on the IP, returns the correct city.
In case IP range is not within any of the provided cities, **unknown** should be provided.

### File Processing

Here you need to read the file provided, `transactions.json`, and enrich it with the data provided by the API.
The output of the script should provide an aggregate containing the sum of `product_price`, grouped by user_status and city.

## Setup
There's a simple API which you'll need, to install it simply use pip.
To run the API, simply run the api.py file.

```
pip install -r requirements.txt
python api.py
```
**************************************************************************************************************************
## Updates
- Changed IP on which app runs on (0.0.0.0 -> 127.0.0.1)

- Changed how user_status() function populates the variable "date" so it goes with my implementation of get_status()

- Adding implementation for get_status() and get_city()

- Added TransactionsSearch class that contains three methods:
	- populateTransactionsArray(): Uses passed in file in class to populate an array of json objects that hold all transactions found in the file
	- checkIfTransactionsPopulated(): Used to check if the transactions is empty or not
	- getTotal(): Loops over the transactions array to group data by city and status and get total price for each grouping

- Added a total_price() route that displays the total product price by processing the file and grouping the city and status together
	'/total_price'
**************************************************************************************************************************

### Delivery
Please provide a zip or tar file containing the complete implementation.