# sopel-currencyconverter
A Sopel IRC bot plugin for converting various fiat/cryptocurrencies.

### Setup

```bash
cd "~/.sopel/plugins/"
wget https://raw.githubusercontent.com/dowodenum/sopel-currencyconverter/main/currencyconverter.py
pip3 install requests
```

### Configuration

Add the following block in your sopel config file (~/.sopel/default.cfg by default), replacing with your key:
```
[currencyconverter]
  apiKey = D34DB33FF33D
```
- obtain a free API key: https://free.currencyconverterapi.com

### Usage

From any channel the bot is in, or via privmsg (adjust from `.` to your bot's configured prefix):
```
<you> .help val
<bot> e.g. .val 1 BTC [to] USD
<you> .val 1 USD to CAD
<bot> you: 1.33 CAD
<you> .val 10 vef TO usd
<bot> you: 5E-11 USD
<you> .val 1 btc usd
<bot> you: 42069.69 USD
<you> .val 1 sat usd
<bot> you: 0.00041 USD
<you> .val 100 sats usd
<bot> you: 0.04 USD
<you> .val 4.20 usd sats
<bot> you: 9983.43 sats
```

----

Thanks to [NMC](https://stackoverflow.com/questions/13479163/round-float-to-x-decimals/63035573#63035573)
