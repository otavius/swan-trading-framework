# swan-trading-framework

The Swan Trading Framework currently works with the Oanda API. Looking to branch into the alpaca api soon once I finish developing for the oanda api. Will continue with updates and also update the README everytime. Python >=3.10

## Folders to create 
Firstly, in the code base you may see an import like constant.account for example. This is the folder(which you can name whatever you like) that holds api keys, URLS , and other private stuff. Definitely create a folder that holds important info!

## API Folder 
The api folder contains connection points to the oanda api. This folder will grow with adding more api to connect too.

## Data Folder 
Stores all the downloaded data from the Oanda api. Also you get data from other source you deem fit for backtesting. Remeber the higher the quality of data you get. The better the result are well to me at least.

## Infrastructure 
There is serval file within the infrastructure folder. You have the collect data python file. Here you can change the candle count which is set to 3000(the amount of candles it will download). Then you have the increaments the timeframes you would like to download the data from. 

## Logs 
The logs folder with keep certain logs that "your" trading bot with create. Such as error logs, symbol logs(Will take the price of every symbol you trade!).  



