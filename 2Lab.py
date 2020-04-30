import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def price_channel(data_frame, length):
    if length > 1:
        length = length-1
    end = length
    start = 0
    copied_data = data_frame[["High", "Low"]].copy(deep=True)
    for i, val in enumerate(data_frame["High"]):
        copied_data["High"][i] = 0
        copied_data["Low"][i] = 0
    if i <= length:
        return copied_data
    else:
        while end <= i:
            copied_data["High"][end] = data_frame["High"][start:end].max()
            copied_data["Low"][end] = data_frame["Low"][start:end].min()
            start += 1
            end += 1
    return copied_data


def a_d(data_frame):
    return np.cumsum((((data_frame["Close"] - data_frame["Low"]) - (data_frame["High"] - data_frame["Close"]))
                      / (data_frame["High"] - data_frame["Low"])) * data_frame["Vol"])


def momentum(data_frame, column_name, period):
    if period > 1:
        period = period-1
    copied_data = data_frame[column_name].copy(deep=True)
    for index, value in enumerate(copied_data):
        if index >= period:
            num = (data_frame[column_name][index] - data_frame[column_name][index - period])
            copied_data.array[index] = num
        else:
            copied_data.array[index] = 0
    return copied_data


def import_csv(filename):
    data_from_file = pd.read_csv(filename, parse_dates=["Date"], index_col=["Date"])
    return data_from_file


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


aapl = import_csv(r"C:\Users\pjach\Univeras\Finansinis intelektas\1 laboratorinis darbas\aapl.csv")
aapll = import_csv(r"C:\Users\pjach\Univeras\Finansinis intelektas\1 laboratorinis darbas\aapll.csv")
tesla = import_csv(r"C:\Users\pjach\Univeras\Finansinis intelektas\1 laboratorinis darbas\ntesla.csv")
teslas = import_csv(r"C:\Users\pjach\Univeras\Finansinis intelektas\1 laboratorinis darbas\teslas.csv")
# A/D
ad = a_d(tesla)
plot(ad,"Date","","A/D","TSLA")
plot(tesla["AccDst-PrVol"],"Date","","A/D Tradestation","TSLA")

# Momentum
tesla_mom = momentum(tesla[2:],"Close",13)
plot(tesla["Momentum"], "Days","","Tradestation momentum","TSLA")
plot(tesla_mom, "Days","","Momentum","TSLA")

# Price channel
pc = price_channel(tesla[1:],21)
plot(tesla["Low"], "Date", "Price", "TESLA High/Low with price channel index", "")
plt.plot(pc["High"])
plt.plot(pc["Low"])

plot(tesla["Low"], "Date", "Price", "TESLA High/Low with price channel index, Tradestation", "")
plt.plot(tesla["UpperBand"])
plt.plot(tesla["LowerBand"])