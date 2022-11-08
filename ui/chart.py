import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mf

def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
  return support
def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
  return resistance

class Chart:

    def plot(self, filename, candles_display=100):

        df = pd.read_csv(filename, index_col=0)
        df.index = pd.to_datetime(df.index)
        df.rename(columns={'OPEN': 'Open', 'HIGH': 'High',
                'LOW': 'Low', 'CLOSE': 'Close', 'VOLUME': 'Volume'}, inplace=True)
        
        levels = []
        for i in range(2,df.shape[0]-2):
            if isSupport(df,i):
                levels.append((i,df['Low'][i]))
            elif isResistance(df,i):
                levels.append((i,df['High'][i]))
        mf.plot(df.tail(candles_display),type='candle')

        # print(df.head())

        # for level in levels:
        #     plt.hlines(level[1],xmin=level[0],\
        #             xmax=len(df.index),colors='blue')
        # fig.show()
