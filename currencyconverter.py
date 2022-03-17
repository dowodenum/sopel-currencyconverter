import requests
import re
import math
import decimal

from sopel import config, trigger
from sopel.plugin import commands, example
from sopel.config.types import StaticSection, ValidatedAttribute

class CurrencyConverterSection(StaticSection):
    apiKey = ValidatedAttribute('apiKey', default=None)

def configure(config):
    config.define_section('currencyconverter', CurrencyConverterSection, validate=False)
    config.currencyconverter.configure_setting('apiKey', 'free.currencyconverterapi.com API key')

def setup(bot):
    bot.config.define_section('currencyconverter', CurrencyConverterSection)

def value_to_decimal(value, decimal_places):
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP  # define rounding method
    return decimal.Decimal(str(float(value))).quantize(decimal.Decimal('1e-{}'.format(decimal_places)))


@commands('val')
@example('.val 1 BTC [to] USD')
def val(bot, trigger):
    apiUrl = 'https://free.currencyconverterapi.com/api/v6/convert'
    apiKey = bot.config.currencyconverter.apiKey
    satsout = False

    arg = trigger.group(2).upper().replace(' TO ',' ').split(' ')

    # low-hanging fruit syntax checks
    if len(arg) < 3:
        bot.reply("Error: syntax - .val <amount> <currency1> [to] <currency2>")
        return

    try:
        amount, input, output = float(arg[0]), arg[1], arg[2]
    except ValueError:
        bot.reply("Error: syntax - .val <amount> <currency1> [to] <currency2>")
        return

    # handle satoshis as we do BTC, 1 BTC = 100,000,000 sats
    if input[:3] == 'SAT':
        input = 'BTC'
        amount = amount / 100000000
    if output[:3] == 'SAT':
        output = 'BTC'
        satsout = True

    # build pair in "BTC_CAD" format
    pair = input + '_' + output

    # do request
    r = requests.get(apiUrl, params={'q': pair, 'compact': 'ultra', 'apiKey': apiKey})

    # attempt to extract exchange rate from response
    try:
        s = r.json()[pair]
    except KeyError:
        bot.reply('Error - One of [' + input + '/' + output + '] is not a recognized currency code.')
        return

    # get the initial result
    t = float(s) * amount

    # converting to sats? Multiply output BTC by 100 million, and change the string back
    if satsout:
        output = 'sats'
        t = t * 100000000

    # do some kludgy adaptive rounding
    if t >= 0.005:
        u = str(value_to_decimal(t, 2))
    elif t >= 0.00005:
        u = str(value_to_decimal(t, 5))
    elif t >= 0.0000005:
        u = str(value_to_decimal(t, 7))
    elif t >= 0.000000005:
        u = str(value_to_decimal(t, 9))
    else:
        u = str(value_to_decimal(t, 11))

    bot.reply(u + ' ' + output)
    return
