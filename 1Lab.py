import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

dates = pd.date_range('20190214', periods=6)
numbers = ([[101, 103], [105.5, 75], [102, 80.3], [100, 85], [110, 98], [109.6, 125.7]])
df = pd.DataFrame(numbers, index=dates, columns=['A', 'B'])

rowData1 = df.loc['2019-02-18']
print('1:\n', rowData1, '\n')

rowData2 = df.loc[datetime(2019, 2, 18)]
print('2: \n', rowData2, '\n')

print('3\n', df.tail(2).head(1), '\n')

print('4\n', df.head(2)[['B']], '\n')

print('5\n', df.sort_values(by=['B'], ascending=False), '\n')

print('6\n', df['A'].max(), '\n')

maxAValue = df['A'].max()*2
df.replace(df['A'].max(), maxAValue, inplace=True)
print('7\n', df, '\n')

print('8\n', df[df.A > 105], '\n')

df['A'].plot()

df.drop(df[df.B > df.A].index, inplace=True)
print('10\n', df, '\n')

a = np.random.randint(low=1, high=10, size=10)
b = np.random.randint(low=1, high=10, size=10)

print("=== 1 ===")
print(a)
print(b)
c = 0
for i, val in enumerate(a):
    c = c + a[i] + b[i]
print(np.sum(a+b))
print(np.sum([a, b]))

print("=== 2 ===")
a = np.random.randint(low=1, high=10, size=10)
for i, val in enumerate(a):
    if val > 0:
        a[i] = 0
print(a)
print(np.where(a > 0, 0, a))

print("=== 3 ===")
a = np.random.randint(low=1, high=10, size=10)
for i, val in enumerate(a):
    print(a)
a = a[a < 6]
print(a)

print("=== 4 ===")
a = np.random.randint(low=1, high=10, size=10)
b = []
c = range(9)
for i in c:
    if a[i] == a[i+1]:
        b = np.append(b, i).astype(int)
print(a)
print(b)
d = np.diff(a, 1)
print(np.where(d == 0)[0])

print("=== 5 ===")
a = np.random.randint(low=1, high=10, size=10)
c = []
ind = range(10)
for i in ind:
    if a[i] > b[i]:
      c = np.append(c, i).astype(int)
print(a)
print(b)
print(c)
print(np.where(a > b)[0])

print("=== 6 ===")
a = np.random.randint(low=1, high=10, size=10)
print(a)
for i in range(1, len(a), 1):
    a[i-1] = a[i]
print(a)
print("-----------")
a = np.random.randint(low=1, high=10, size=10)
print(a)
a = np.append(a, a[-1:])
print(a[1:])

print("=== 7 ===")
a = np.random.randint(low=1, high=10, size=10)
print(a)
for i in range(int(len(a)/2)):
    b = a[i]
    a[i] = a[(len(a)-1) - i]
    a[(len(a)-1) - i] = b
print(a)
a = np.split(a, 2)
print(a)
a = np.concatenate((a[1][::-1], a[0][::-1]), axis=None)
print(a)


print("=== 8 ===")
a = np.random.randint(low=1, high=10, size=10)
print(a)
for i, val in enumerate(a):
    if (i + 1) % 2 == 0:
        a[i] = 0
print(a)
print("------------")
a = np.random.randint(low=1, high=10, size=10)
a[1::2] = 0
print(a)

print("=== 9 ===")
a = np.random.randint(10, size=(5, 6))
print(a)
for row in a:
    print(np.average(row))
print(np.average(a.T, 1))

print("=== 10 ===")
a = np.random.randint(10, size=(5, 5))
print(a)
b = []
rows = a.shape[0]
cols = a.shape[1]
for i in range(rows):
    b.append(a[i][i])
print(b)
print("---------------")
c = np.ravel(a)
print(c[::cols+1])


# Data reading method
def import_csv(filename):
    data = pd.read_csv(filename, parse_dates=["Date"], index_col=["Date"])
    return data


# Plotting method
def plot(y_axis, x_label, y_label, title, ticker):
    fig, ax = plt.subplots()
    ax.plot(y_axis)
    ax.xaxis_date()  # interpret the x-axis values as dates
    fig.autofmt_xdate()  # make space for and rotate the x-axis tick labels
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid()
    plt.legend([ticker])
    plt.show()

# Data reading
msft_daily = import_csv(r"C:\Users\pjach\Desktop\msft_daily.csv")
msft_minute = import_csv(r"C:\Users\pjach\Desktop\msft_minute.csv")
bren_ticks = import_csv(r"C:\Users\pjach\Desktop\BRENTCMDUSD.csv")
nat_gas_monthly = import_csv(r"C:\Users\pjach\Desktop\monthly_csv.csv")

# Index change from date to the number of ticks
bren_ticks.index = range(1,2055)

# Plotting data
# Ticks
plt.plot(bren_ticks["BidPrice"])
plt.title("Brent Crude Oil, Bid prices, tick volume - 1.3")
plt.xlabel("Tick")
plt.ylabel("Price")
plt.grid()
plt.legend("BRCO")

# Daily and minutes
plot(msft_daily["Volume"], "Date", "Volume", "Microsoft daily stocks volume", "MSFT")
plot(msft_minute["Close"], "Date", "Close", "Microsoft minute stocks close prices", "MSFT")

# Plotting extra task with natural gases
plt.plot(nat_gas_monthly.groupby(nat_gas_monthly.index.month).mean())
plt.title("Natural gas monthly averages 1997-2019")
plt.xlabel("Month")
plt.ylabel("Price")
plt.grid()
plt.legend("NATGAS price")

# Fake data
date_range = pd.date_range(pd.datetime.today(), periods=10)
price = np.random.randn(10).cumsum()
price = abs(price[:])*15
df = pd.DataFrame(price, columns=["Value"], index=date_range)
plot(df["Value"], "Date", "Price", "Data", "ABCD")

