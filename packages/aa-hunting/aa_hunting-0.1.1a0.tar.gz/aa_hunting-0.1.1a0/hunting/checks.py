# from django.core.checks import register
# from . import app_settings


# @register()
# def my_check(app_configs, **kwargs):
#     if app_settings.MOONS_ORE_RATE_BUY_SELL not in app_settings._valid_buy_sell:
#         errors.append(Error(
#             'Invalid MOONS_ORE_RATE_BUY_SELL',
#             hint="Must be 'buy' or 'sell'",
#             id='MOONS_ORE_RATE_BUY_SELL',
#         ))
#     return errors
