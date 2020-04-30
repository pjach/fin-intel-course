import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def import_csv(filename):
    data_from_file = pd.read_csv(filename, parse_dates=[["Date", "Time"]], index_col=["Date_Time"])
    return data_from_file


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


def strategy (data_frame, price_column, momentum_interval):
    mom = momentum(data_frame, price_column, momentum_interval)
    stop_loss = np.empty(len(data_frame))
    stop_loss[:] = np.NAN
    buy = np.empty(len(data_frame))
    buy[:] = np.NAN
    sell = np.empty(len(data_frame))
    sell[:] = np.NAN
    profit = np.zeros((len(data_frame)))
    tax_index = 0
    buy_price = 0
    poz = 0
    for i in range(momentum_interval-1, len(data_frame)):
        if tax_index == 1:
            profit[i] = ((data_frame[price_column][i] - data_frame[price_column][i - 1]) * poz) - 1
        else:
            profit[i] = (data_frame[price_column][i] - data_frame[price_column][i - 1]) * poz
        tax_index = 0
        if buy_price - data_frame[price_column][i] >= 20 and poz == 1:
            stop_loss[i] = data_frame[price_column][i]
            poz = 0
            buy_price = 0
            tax_index = 1
        elif mom[i] > 0 and mom[i - 1] <= 0:
            buy_price = data_frame[price_column][i]
            buy[i] = data_frame[price_column][i]
            poz = 1
            tax_index = 1
        elif mom[i] < 0 and mom[i - 1] >= 0:
                sell[i] = data_frame[price_column][i]
                poz = -1
                tax_index = 1
    data = {"Profit" : profit, "Buy_Points" : buy, "Sell_Points" : sell, "Momentum": mom.array, "Stop_Loss": stop_loss}
    return pd.DataFrame(data=data, columns=["Profit", "Buy_Points", "Sell_Points", "Momentum", "Stop_Loss"], index=data_frame.index)


tesla = import_csv(r"C:\Users\pjach\Univeras\Finansinis intelektas\3 laboratorinis\tesla.csv")

sharpes = np.arange(60, dtype=np.float)
for i in range(1,61):
    temp = strategy(tesla, "Close", i)
    sharpes[i-1] = (np.average(temp["Profit"])*252*7)/(np.std(temp["Profit"])*np.sqrt(252*7))
index = np.argmax(sharpes)
not_optimised = strategy(tesla,"Close",20)
optimised = strategy(tesla,"Close",index+1)

profit = np.sum(optimised["Profit"])

plt.plot(not_optimised["Profit"].cumsum())
plt.plot(optimised["Profit"].cumsum())
plt.legend(["Not optimised", "Optimised"])

plt.plot(optimised["Momentum"])
plt.plot(optimised["Buy_Points"], "r+")
plt.plot(optimised["Sell_Points"], "k+")

plt.plot(tesla["Close"])
plt.plot(optimised["Buy_Points"], "r+")
plt.plot(optimised["Sell_Points"], "k+")
plt.plot(optimised["Stop_Loss"], "b+")
plt.legend(["TSLA close price", "Buy point", "Sell point", "Stop Loss"])
