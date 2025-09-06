from datetime import datetime
from dateutil.relativedelta import relativedelta

start_date = datetime(1980, 12, 1)
end_date = datetime(1981, 12, 1)

diff = relativedelta(end_date, start_date)
months = diff.years * 12 + diff.months

if months <= 0:
    label = "{:02d} Months Before Event".format(abs(months))
else:
    label = "{:02d} Months After Event".format(months)

print(label)
