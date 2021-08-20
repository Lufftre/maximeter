import pandas as pd

df = pd.read_csv('maxipolar.csv', sep=';').drop(0)
df = df.set_index('twa/tws')
def performance(tws, twa, sow):
    tws = min(df.columns, key=lambda x: abs(float(x) - tws))
    twa = min(df.index, key=lambda x: abs(x - twa))
    return sow / df[str(tws)][twa]

if __name__ == '__main__':
    print(df)
