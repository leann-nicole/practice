from datetime import datetime as dt

format = '%a %d %b %Y %H:%M:%S %z'

time1 = dt.strftime(input(), format)
time2 = dt.strftime(input(), format)

print(f'Date 1: {time1}')
print(f'Date 2: {time2}')

time_diff = abs(time1 - time2)

print('Time difference:', time_diff)
