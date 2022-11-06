import pandas as pd
import mplfinance as mf

class Chart:

    def plot(self, filename):
        df = pd.read_csv(filename, index_col=0)
        df.index = pd.to_datetime(df.index)
        df.rename(columns={'OPEN': 'Open', 'HIGH': 'High',
                'LOW': 'Low', 'CLOSE': 'Close', 'VOLUME': 'Volume'}, inplace=True)
        mf.plot(df.iloc[:-50,:])
