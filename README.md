# stock-backtesting
Stock Backtesting Notebook and Script

## Setup
1. [Register for a Finnhub.io token](https://finnhub.io/register).

2. Create env.sh file in this directory:
```bash
FINNHUB_TOKEN=<put your finnhub.io token here>
```
(this file will populate environment variables inside docker container)

3. Make sure you have Docker installed. https://www.docker.com/. We use Docker to keep the environment consistent.

## Run
There are 2 ways to run this code:

### Jupyter Notebook ("development")
This is helpful for playing with strategies.

```bash
./notebook.sh
```

Keep terminal running. The logs should print out 3 links shortly. Open the 127.0.0.1:8888 link, which should be the last link printed.

### In Terminal ("production")
```bash
./run.sh
```

## A note on making changes
prod.py is a direct export from the notebook and should be kept in sync manually. `File > Download As > Python (.py)`
