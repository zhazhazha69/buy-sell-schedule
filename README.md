# Buy/Sell-schedule 
## Version 3
![Screenshot](https://github.com/zhazhazha69/buy-sell-schedule/blob/v3/Screenshot.jpg?raw=true)

## Setup
1. On line 23, configure the database connection settings
2. On lines 280, 327 specify in the queries the actual data of your database
3. Forward to battle!

## Requirements
- Python 3
- dash
- plotly
- pandas
- sqlalchemy
- driver for your database
- information source (from exchange_data import get_data) - "get_data", it should give information in the format: "index_limit, buy_percent, sell_percent, total_buy_quantity, total_sell_quantity, total_quantity"

## Run
Install the driver for your database and
```
git commit https://github.com/zhazhazha69/buy-sell-schedule/tree/v3
pip install -r requirements.txt 
python app.py 
```

###### Made with ♥️