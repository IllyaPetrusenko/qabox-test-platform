import datetime

host = 'https://public.mtender.gov.md/budgets'
offset = (datetime.datetime.now() - datetime.timedelta(hours=3) - datetime.timedelta(minutes=1200))\
    .strftime("%Y-%m-%dT%H:%M:%S.000Z")