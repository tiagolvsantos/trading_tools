import logging
import pandas as pd
import numpy as np
import math
import pandas_ta as ta
from scipy import stats
from scipy.signal import argrelextrema
#import matplotlib.pyplot as plt

log = logging.getLogger(__name__)

def _parse_dataframe(df):
    df = df.sort_values(by=['date'], ascending=True) # order df oldest records first
    df['close'] = df['close'].astype(float) # parse to float
    df['high'] = df['high'].astype(float) # parse to float
    df['low'] = df['low'].astype(float) # parse to float
    df['volume'] = df['volume'].astype(float) # parse to float
    return df

def moving_average(df, n):
    """Calculate the moving average for the given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    MA = pd.Series(df['close'].rolling(n, min_periods=n).mean(), name=f'MA_{str(n)}')
    df = pd.concat((df,MA), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def exponential_moving_average(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    EMA = pd.Series(df['close'].ewm(span=n, min_periods=n).mean(), name=f'EMA_{str(n)}')
    df = pd.concat((df,EMA), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def momentum(df, n):
    """
    
    :param df: pandas.DataFrame 
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    M = pd.Series(df['close'].diff(n), name=f'Momentum_{str(n)}')
    df = pd.concat((df,M), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def rate_of_change(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    M = df['close'].diff(n - 1)
    N = df['close'].shift(n - 1)
    ROC = pd.Series(M / N, name=f'ROC_{str(n)}')
    df = pd.concat((df,ROC), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def average_true_range(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    i = 0
    TR_l = [0]
    while i <= len(df)-2:
        TR = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR_l.append(TR)
        i += 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean(), name=f'ATR_{str(n)}')
    df = pd.concat((df,ATR), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def bollinger_bands(df, n):
    """
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    MA = pd.Series(df['close'].rolling(n, min_periods=n).mean())
    MSD = pd.Series(df['close'].rolling(n, min_periods=n).std())
    b1 = 4 * MSD / MA
    B1 = pd.Series(b1, name=f'BollingerB_{str(n)}')
    df = df.join(B1)
    b2 = (df['close'] - MA + 2 * MSD) / (4 * MSD)
    B2 = pd.Series(b2, name=f'Bollinger%b_{str(n)}')
    df = pd.concat((df,B2), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def ppsr(df):
    """Calculate Pivot Points, Supports and Resistances for given data
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """

    df = _parse_dataframe(df) 

    PP = pd.Series((df['high'] + df['low'] + df['close']) / 3)
    R1 = pd.Series(2 * PP - df['low'])
    S1 = pd.Series(2 * PP - df['high'])
    R2 = pd.Series(PP + df['high'] - df['low'])
    S2 = pd.Series(PP - df['high'] + df['low'])
    R3 = pd.Series(df['high'] + 2 * (PP - df['low']))
    S3 = pd.Series(df['low'] - 2 * (df['high'] - PP))
    psr = {'PP': PP, 'R1': R1, 'S1': S1, 'R2': R2, 'S2': S2, 'R3': R3, 'S3': S3}
    PSR = pd.DataFrame(psr)
    df = pd.concat((df,PSR), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def stochastic_oscillator_k(df):
    """Calculate stochastic oscillator %K for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """

    df = _parse_dataframe(df) 

    SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='SO%k')
    df = pd.concat((df,SOk), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def stochastic_oscillator_d(df, n):
    """Calculate stochastic oscillator %D for given data.
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    SOk = pd.Series((df['close'] - df['low']) / (df['high'] - df['low']), name='SO%k')
    SOd = pd.Series(SOk.ewm(span=n, min_periods=n).mean(), name=f'SO%d_{str(n)}')
    df = pd.concat((df,SOd), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def trix(df, n):
    """Calculate TRIX for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 
    EX1 = df['close'].ewm(span=n, min_periods=n).mean()
    EX2 = EX1.ewm(span=n, min_periods=n).mean()
    EX3 = EX2.ewm(span=n, min_periods=n).mean()
    i = 0
    ROC_l = [np.nan]
    while i + 1 <= len(df)-2:
        ROC = (EX3[i + 1] - EX3[i]) / EX3[i]
        ROC_l.append(ROC)
        i += 1
    Trix = pd.Series(ROC_l, name=f'Trix_{str(n)}')
    df = pd.concat((df,Trix), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def average_directional_movement_index(df, n, n_ADX):
    """Calculate the Average Directional Movement Index for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :param n_ADX: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    i = 0
    UpI = []
    DoI = []
    while i + 1 <= len(df)-2:
        UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
        DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
        UpD = UpMove if UpMove > DoMove and UpMove > 0 else 0
        UpI.append(UpD)
        DoD = DoMove if DoMove > UpMove and DoMove > 0 else 0
        DoI.append(DoD)
        i += 1
    i = 0
    TR_l = [0]
    while i < len(df) -2:
        TR = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR_l.append(TR)
        i += 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(span=n, min_periods=n).mean())
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean() / ATR)
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean() / ATR)
    ADX = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n_ADX, min_periods=n_ADX).mean(), name=f'ADX_{str(n)}_{str(n_ADX)}')
    df = pd.concat((df,ADX), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def macd(df, n_fast=12, n_slow=26):
    """Calculate MACD, MACD Signal and MACD difference
    
    :param df: pandas.DataFrame
    :param n_fast: 
    :param n_slow: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    EMAfast = pd.Series(df['close'].ewm(span=n_fast, min_periods=n_slow).mean())
    EMAslow = pd.Series(df['close'].ewm(span=n_slow, min_periods=n_slow).mean())
    MACD = pd.Series(EMAfast - EMAslow, name=f'MACD_{str(n_fast)}_{str(n_slow)}')
    MACDsign = pd.Series(MACD.ewm(span=9, min_periods=9).mean(), name=f'MACDsign_{str(n_fast)}_{str(n_slow)}')
    MACDdiff = pd.Series(MACD - MACDsign, name=f'MACDdiff_{str(n_fast)}_{str(n_slow)}')
    df = pd.concat((df,MACD), axis=1)
    df = pd.concat((df,MACDsign), axis=1)
    df = pd.concat((df,MACDdiff), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def mass_index(df):
    """Calculate the Mass Index for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    Range = df['high'] - df['low']
    EX1 = Range.ewm(span=9, min_periods=9).mean()
    EX2 = EX1.ewm(span=9, min_periods=9).mean()
    Mass = EX1 / EX2
    MassI = pd.Series(Mass.rolling(25).sum(), name='Mass Index')
    df = pd.concat((df,MassI), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def vortex_indicator(df, n):
    """Calculate the Vortex Indicator for given data.
    
    Vortex Indicator described here:
        http://www.vortexindicator.com/VFX_VORTEX.PDF
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    i = 0
    TR = [0]
    while i < len(df) -2:
        Range = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR.append(Range)
        i += 1
    i = 0
    VM = [0]
    while i < len(df) -2:
        Range = abs(df.loc[i + 1, 'high'] - df.loc[i, 'low']) - abs(df.loc[i + 1, 'low'] - df.loc[i, 'high'])
        VM.append(Range)
        i += 1
    VI = pd.Series(pd.Series(VM).rolling(n).sum() / pd.Series(TR).rolling(n).sum(), name=f'Vortex_{str(n)}')
    df = pd.concat((df,VI), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def kst_oscillator(df, r1, r2, r3, r4, n1, n2, n3, n4):
    """Calculate KST Oscillator for given data.
    
    :param df: pandas.DataFrame
    :param r1: 
    :param r2: 
    :param r3: 
    :param r4: 
    :param n1: 
    :param n2: 
    :param n3: 
    :param n4: 
    :return: pandas.DataFrame
    """
    M = df['close'].diff(r1 - 1)
    N = df['close'].shift(r1 - 1)
    ROC1 = M / N
    M = df['close'].diff(r2 - 1)
    N = df['close'].shift(r2 - 1)
    ROC2 = M / N
    M = df['close'].diff(r3 - 1)
    N = df['close'].shift(r3 - 1)
    ROC3 = M / N
    M = df['close'].diff(r4 - 1)
    N = df['close'].shift(r4 - 1)
    ROC4 = M / N
    KST = pd.Series(ROC1.rolling(n1).sum() + ROC2.rolling(n2).sum() * 2 + ROC3.rolling(n3).sum() * 3 + ROC4.rolling(n4).sum() * 4, name=f'KST_{str(r1)}_{str(r2)}_{str(r3)}_{str(r4)}_{str(n1)}_{str(n2)}_{str(n3)}_{str(n4)}')
    df = df.join(KST)
    return df.sort_values(by=['date'], ascending=False)


def relative_strength_index(df, n):
    """Calculate Relative Strength Index(RSI) for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= len(df) -2:
        UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
        DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
        UpD = UpMove if UpMove > DoMove and UpMove > 0 else 0
        UpI.append(UpD)
        DoD = DoMove if DoMove > UpMove and DoMove > 0 else 0
        DoI.append(DoD)
        i += 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
    #RSI = pd.Series(PosDI / (PosDI + NegDI), name=f'RSI_{str(n)}')
    RSI = pd.Series(PosDI / (PosDI + NegDI)*100, name=f'RSI_{str(n)}')
    df = pd.concat((df,RSI), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def true_strength_index(df, r, s):
    """Calculate True Strength Index (TSI) for given data.
    
    :param df: pandas.DataFrame
    :param r: 
    :param s: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    M = pd.Series(df['close'].diff(1))
    aM = abs(M)
    EMA1 = pd.Series(M.ewm(span=r, min_periods=r).mean())
    aEMA1 = pd.Series(aM.ewm(span=r, min_periods=r).mean())
    EMA2 = pd.Series(EMA1.ewm(span=s, min_periods=s).mean())
    aEMA2 = pd.Series(aEMA1.ewm(span=s, min_periods=s).mean())
    TSI = pd.Series(EMA2 / aEMA2, name=f'TSI_{str(r)}_{str(s)}')
    df = pd.concat((df,TSI), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def accumulation_distribution(df, n):
    """Calculate Accumulation/Distribution for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    M = ad.diff(n - 1)
    N = ad.shift(n - 1)
    ROC = M / N
    AD = pd.Series(ROC, name=f'Acc/Dist_ROC_{str(n)}')
    df = pd.concat((df,AD), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def chaikin_oscillator(df):
    """Calculate Chaikin Oscillator for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 
    ad = (2 * df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume']
    Chaikin = pd.Series(ad.ewm(span=3, min_periods=3).mean() - ad.ewm(span=10, min_periods=10).mean(), name='Chaikin')
    df = pd.concat((df,Chaikin), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def money_flow_index(df, n):
    """Calculate Money Flow Index and Ratio for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    PP = (df['high'] + df['low'] + df['close']) / 3
    i = 0
    PosMF = [0]
    while i < len(df)-2:
        if PP[i + 1] > PP[i]:
            PosMF.append(PP[i + 1] * df.loc[i + 1, 'volume'])
        else:
            PosMF.append(0)
        i += 1
    PosMF = pd.Series(PosMF)
    TotMF = PP * df['volume']
    MFR = pd.Series(PosMF / TotMF)
    MFI = pd.Series(MFR.rolling(n, min_periods=n).mean(), name=f'MFI_{str(n)}')
    df = pd.concat((df,MFI), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def on_balance_volume(df, n):
    """Calculate On-Balance volume for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    i = 0
    OBV = [0]
    while i < len(df)-2:
        if df.loc[i + 1, 'close'] - df.loc[i, 'close'] > 0:
            OBV.append(df.loc[i + 1, 'volume'])
        if df.loc[i + 1, 'close'] - df.loc[i, 'close'] == 0:
            OBV.append(0)
        if df.loc[i + 1, 'close'] - df.loc[i, 'close'] < 0:
            OBV.append(-df.loc[i + 1, 'volume'])
        i += 1
    OBV = pd.Series(OBV)
    OBV_ma = pd.Series(OBV.rolling(n, min_periods=n).mean(), name=f'OBV_{str(n)}')
    df = pd.concat((df,OBV_ma), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def force_index(df, n):
    """Calculate Force Index for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    F = pd.Series(df['close'].diff(n) * df['volume'].diff(n), name=f'Force_{str(n)}')

    df = pd.concat((df,F), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def ease_of_movement(df, n):
    """Calculate Ease of Movement for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = _parse_dataframe(df) 

    EoM = (df['high'].diff(1) + df['low'].diff(1)) * (df['high'] - df['low']) / (2 * df['volume'])
    Eom_ma = pd.Series(EoM.rolling(n, min_periods=n).mean(), name=f'EoM_{str(n)}')
    df = pd.concat((df,Eom_ma), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def commodity_channel_index(df, n):
    """Calculate Commodity Channel Index for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    PP = (df['high'] + df['low'] + df['close']) / 3
    CCI = pd.Series((PP - PP.rolling(n, min_periods=n).mean()) / PP.rolling(n, min_periods=n).std(), name=f'CCI_{str(n)}')

    df = pd.concat((df,CCI), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def coppock_curve(df, n):
    """Calculate Coppock Curve for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    M = df['close'].diff(int(n * 11 / 10) - 1)
    N = df['close'].shift(int(n * 11 / 10) - 1)
    ROC1 = M / N
    M = df['close'].diff(int(n * 14 / 10) - 1)
    N = df['close'].shift(int(n * 14 / 10) - 1)
    ROC2 = M / N
    Copp = pd.Series((ROC1 + ROC2).ewm(span=n, min_periods=n).mean(), name=f'Copp_{str(n)}')

    df = pd.concat((df,Copp), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def keltner_channel(df, n):
    """Calculate Keltner Channel for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    KelChM = pd.Series(((df['high'] + df['low'] + df['close']) / 3).rolling(n, min_periods=n).mean(), name=f'KelChM_{str(n)}')

    KelChU = pd.Series(((4 * df['high'] - 2 * df['low'] + df['close']) / 3).rolling(n, min_periods=n).mean(), name=f'KelChU_{str(n)}')

    KelChD = pd.Series(((-2 * df['high'] + 4 * df['low'] + df['close']) / 3).rolling(n, min_periods=n).mean(), name=f'KelChD_{str(n)}')

    df = pd.concat((df,KelChM), axis=1)
    df = pd.concat((df,KelChU), axis=1)
    df = pd.concat((df,KelChD), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def ultimate_oscillator(df):
    """Calculate Ultimate Oscillator for given data.
    
    :param df: pandas.DataFrame
    :return: pandas.DataFrame
    """
    i = 0
    TR_l = [0]
    BP_l = [0]
    while i <len(df)-2:
        TR = max(df.loc[i + 1, 'high'], df.loc[i, 'close']) - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        TR_l.append(TR)
        BP = df.loc[i + 1, 'close'] - min(df.loc[i + 1, 'low'], df.loc[i, 'close'])
        BP_l.append(BP)
        i += 1
    UltO = pd.Series((4 * pd.Series(BP_l).rolling(7).sum() / pd.Series(TR_l).rolling(7).sum()) + (
                2 * pd.Series(BP_l).rolling(14).sum() / pd.Series(TR_l).rolling(14).sum()) + (
                                 pd.Series(BP_l).rolling(28).sum() / pd.Series(TR_l).rolling(28).sum()),
                     name='Ultimate_Osc')
    df = pd.concat((df,UltO), axis=1)
    return df.sort_values(by=['date'], ascending=False)


def donchian_channel(df, n):
    """Calculate donchian channel of given pandas data frame.
    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    i = 0
    dc_l = []
    while i < n - 1:
        dc_l.append(0)
        i += 1

    i = 0
    while i + n - 1 < len(df)-2:
        dc = max(df['high'].ix[i:i + n - 1]) - min(df['low'].ix[i:i + n - 1])
        dc_l.append(dc)
        i += 1

    donchian_chan = pd.Series(dc_l, name=f'Donchian_{str(n)}')
    donchian_chan = donchian_chan.shift(n - 1)
    return df.sort_values(by=['date'], ascending=False).join(donchian_chan)


def standard_deviation(df, n):
    """Calculate Standard Deviation for given data.
    
    :param df: pandas.DataFrame
    :param n: 
    :return: pandas.DataFrame
    """
    df = df.join(pd.Series(df['close'].rolling(n, min_periods=n).std(), name=f'STD_{str(n)}'))

    return df.sort_values(by=['date'], ascending=False)


def fibonacci_retracement(df):
    price_min = float(df['close'].min())
    price_max = float(df['close'].max())

    diff = price_max - price_min
    fib_0 = round(price_max,2)
    fib_0_236 = round(price_max - 0.236 * diff,2)
    fib_0_382 = round(price_max - 0.382 * diff,2)
    fib_0_5 = round(price_max - 0.5 * diff,2)
    fib_0_618 = round(price_max - 0.618 * diff,2)
    fib_0_786 = round(price_max - 0.786 * diff,2)
    fib_1 = round(price_min,2)
    df_data = [['0', fib_0], ['0_236', fib_0_236], ['0_382', fib_0_382], ['0_5', fib_0_5], ['0_618', fib_0_618], ['0_786', fib_0_786], ['1', fib_1]]
    return pd.DataFrame(df_data, columns=['Levels', 'levels_value'])


#https://github.com/twopirllc/pandas-ta#cycles-1
def rsi(df_data: pd.DataFrame, periods = 14, ema = True):
    df_data["close"] = pd.to_numeric(df_data["close"])
    close_delta = df_data['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi


def vwap(df_data: pd.DataFrame):
    stdev_multiple_1 = 1.28
    stdev_multiple_2 = 2.01
    stdev_multiple_3 = 2.51
    df_data["volume"]  = pd.to_numeric(df_data["volume"])
    df_data["high"]  = pd.to_numeric(df_data["high"])
    df_data["low"] = pd.to_numeric(df_data["low"])
    df_data["close"] = pd.to_numeric(df_data["close"])


    df_data['VWAP'] = (df_data["volume"]  * (df_data["high"]+ df_data["low"]) / 2).cumsum() / df_data["volume"].cumsum()
    df_data['VWAP_MEAN_DIFF'] = ((df_data["high"] + df_data["low"]) / 2) - df_data.VWAP
    df_data['SQ_DIFF'] = df_data.VWAP_MEAN_DIFF.apply(lambda x: math.pow(x, 2))
    df_data['SQ_DIFF_MEAN'] = df_data.SQ_DIFF.expanding().mean()
    df_data['STDEV_TT'] = df_data.SQ_DIFF_MEAN.apply(math.sqrt)
    df_data['STDEV_1'] = df_data.VWAP + stdev_multiple_1 * df_data['STDEV_TT']
    df_data['STDEV_N1'] = df_data.VWAP - stdev_multiple_1 * df_data['STDEV_TT']
    df_data['STDEV_2'] = df_data.VWAP + stdev_multiple_2 * df_data['STDEV_TT']
    df_data['STDEV_N2'] = df_data.VWAP - stdev_multiple_2 * df_data['STDEV_TT']
    df_data['WVAP_TO_PRICE_DIFF'] = df_data.VWAP - df_data["close"]

    #df_data.iloc[[0]]
    return df_data


def zscore(df_data: pd.DataFrame):
    return pd.DataFrame(stats.zscore(pd.to_numeric(df_data.close)))


def bollinger_bands(df, period=20, multiplier=2):
    df['UpperBand'] = df['close'].rolling(period).mean() + df['close'].rolling(period).std() * multiplier
    df['LowerBand'] = df['close'].rolling(period).mean() - df['close'].rolling(period).std() * multiplier

    return df

# CVD
def cumulative_volume_delta(df):
    df["volume"]  = pd.to_numeric(df["volume"])
    df["high"]  = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["open"] = pd.to_numeric(df["open"])

    df['open_close_max'] = df.high - df[["open", "close"]].max(axis=1)
    df['open_close_min'] = df[["open", "close"]].min(axis=1) - df.low
    df['open_close_abs'] = (df.close - df.open).abs()
    df['is_close_larger'] = df.close >= df.open
    df['is_open_larger'] = df.open > df.close
    df['is_body_cond_met'] = df.is_close_larger | df.is_open_larger

    df.loc[df.is_body_cond_met == False, 'open_close_abs_2x'] = 0
    df.loc[df.is_body_cond_met == True, 'open_close_abs_2x'] = 2*df.open_close_abs

    df['nominator'] = df.open_close_max + df.open_close_min + df.open_close_abs_2x
    df['denom'] = df.open_close_max + df.open_close_min + df.open_close_abs

    df['delta'] = 0
    df.loc[df.denom == 0, 'delta'] = 0.5
    df.loc[df.denom != 0, 'delta'] = df.nominator / df.denom
    df.loc[df.is_close_larger == False, 'delta'] = df.loc[df.is_close_larger == False, 'volume'] * (-df.loc[df.is_close_larger == False, 'delta'])
    df.loc[df.is_close_larger == True, 'delta'] = df.loc[df.is_close_larger == True, 'volume'] * (df.loc[df.is_close_larger == True, 'delta'])

    for count, (index, row) in enumerate(df.iterrows(), start=1):
        if count != 1:
            df.loc[index , 'cumulative_delta'] =  df.loc[index -1 , 'delta'] +  df.loc[index , 'delta'] 
    return df

# SUPERT (trend), SUPERTd (direction), SUPERTl (long), SUPERTs (short)
def supertrend(df_data):
    return ta.supertrend(df_data['high'], df_data['low'], df_data['close'], length=10, multiplier=3)


def _peak_detect(price):
    # Find our relative extrema
    # Return the max indexes of the extrema
    max_idx = list(argrelextrema(price, np.greater, order=10)[0])
    # Return the min indexes of the extrema
    min_idx = list(argrelextrema(price, np.less, order=10)[0])
    idx = max_idx + min_idx + [len(price) - 1]
    idx.sort()
    current_idx = idx[-5:]

    start = min(current_idx)
    end = max(current_idx)

    current_pat = price[current_idx]
    return current_idx, current_pat, start, end

def _is_Gartley(moves, err_allowed):
    XA = moves[0]
    AB = moves[1]
    BC = moves[2]
    CD = moves[3]

    AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)

    if XA>0 and AB<0 and BC>0 and CD<0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
           return 1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    elif XA<0 and AB>0 and BC<0 and CD>0:
        # AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        # BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        # CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    else:
        return np.NaN

def _is_Butterfly(moves, err_allowed):
    XA = moves[0]
    AB = moves[1]
    BC = moves[2]
    CD = moves[3]

    AB_range = np.array([0.786 - err_allowed, 0.786 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)

    if XA>0 and AB<0 and BC>0 and CD<0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
           return 1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    elif XA<0 and AB>0 and BC<0 and CD>0:
        # AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        # BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        # CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    else:
        return np.NaN

def _is_Bat(moves, err_allowed):
    XA = moves[0]
    AB = moves[1]
    BC = moves[2]
    CD = moves[3]

    AB_range = np.array([0.382 - err_allowed, 0.5 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([1.618 - err_allowed, 2.618 + err_allowed]) * abs(BC)

    if XA>0 and AB<0 and BC>0 and CD<0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
           return 1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    elif XA<0 and AB>0 and BC<0 and CD>0:
        # AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        # BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        # CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    else:
        return np.NaN

def _is_Crab(moves, err_allowed):
    XA = moves[0]
    AB = moves[1]
    BC = moves[2]
    CD = moves[3]

    AB_range = np.array([0.382 - err_allowed, 0.618 + err_allowed]) * abs(XA)
    BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
    CD_range = np.array([2.24 - err_allowed, 3.618 + err_allowed]) * abs(BC)

    if XA>0 and AB<0 and BC>0 and CD<0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < CD_range[1]:
           return 1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    elif XA<0 and AB>0 and BC<0 and CD>0:
        # AB_range = np.array([0.618 - err_allowed, 0.618 + err_allowed]) * abs(XA)
        # BC_range = np.array([0.382 - err_allowed, 0.886 + err_allowed]) * abs(AB)
        # CD_range = np.array([1.27 - err_allowed, 1.618 + err_allowed]) * abs(BC)
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return -1
            # plt.plot(np.arange(start, i+15), price.values[start:i+15])
            # plt.scatter(idx, current_pat, c='r')
            # plt.show()
        else:
            return np.NaN
    else:
        return np.NaN
def harmonics(df, symbol):
    err_allowed = 10.0/100
    # data = df
    # data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y %H:%M:%S.%f')
    # data = data.set_index(data['date'])
    # data = data.drop_duplicates(keep=False)
    # price = data['close'].copy()
    # # Find peaks
    # for i in range(100, len(price)):
    #     current_idx, current_pat, start, end = _peak_detect(price.values[:i])

    #     XA = current_pat[1] - current_pat[0]
    #     AB = current_pat[2] - current_pat[1]
    #     BC = current_pat[3] - current_pat[2]
    #     CD = current_pat[4] - current_pat[3]

    #     moves = [XA, AB, BC, CD]

    #     gartley = _is_Gartley(moves, err_allowed)
    #     butterfly = _is_Butterfly(moves, err_allowed)
    #     bat = _is_Bat(moves, err_allowed)
    #     crab = _is_Crab(moves, err_allowed)

    #     harmonics = np.array([gartley, butterfly, bat, crab])
    #     if np.any(harmonics == 1) or np.any(harmonics == -1):
    #         labels = [
    #             'Gartley',
    #             'Butterfly',
    #             'Bat',
    #             'Crab'
    #         ]

    #         for j in range(len(harmonics)):
    #             if harmonics[j] in [1, -1]:
    #                 sense = 'Bearish ' if harmonics[j] == -1 else 'Bullish '
    #                 label = f"{symbol[0]} {symbol[1]}  {sense} {labels[j]}" 

    #                 plt.title(label)
    #                 plt.plot(np.arange(start, i+15), price.values[start:i+15])
    #                 plt.scatter(current_idx, current_pat, c='r')
    #                 plt.show()

