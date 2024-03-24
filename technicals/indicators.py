import pandas as pd 

def BollingerBands(df: pd.DataFrame, num=20, s=2):
    """
     num = the period 
     s = standard deviation
    """
    typical_price = (df.mid_c + df.mid_h + df.mid_l) / 3
    std_dev = typical_price.rolling(window=num).std()
    df["BB_MA"] = typical_price.rolling(window=num).mean()
    df["BB_UP"] = df["BB_MA"] + std_dev * 2
    df["BB_LW"] = df["BB_MA"] - std_dev * 2
    return df

def ATR(df: pd.DataFrame, num=14):
    previous_colosing_price = df.mid_c.shift(1)
    true_range1 = df.mid_h - df.mid_l
    true_range2 = abs(df.mid_h - previous_colosing_price)
    true_range3 = abs(previous_colosing_price - df.mid_l)

    true_range = pd.DataFrame({"tr1": true_range1, "tr2": true_range2, "tr3": true_range3 }).max(axis=1)
    df[f"ATR_{num}"] = true_range.rolling(window=num).mean()
    return df

def KeltnerChannels(df: pd.DataFrame, ema=20, atr=10):
    df["EMA"] = df.mid_c.ewm(span=ema, min_periods=ema).mean()
    df = ATR(df, num=atr)
    c_atr = f"ATR_{atr}"
    df["KeUp"] = df.c_atr* 2 + df.EMA
    df["KeLo"] = df.EMA - df.c_atr * 2
    df.drop(c_atr, axis=1, inplace=True)
    return df 

def RSI(df: pd.DataFrame, num=14):
    alpha = 1.0 / num
    gains = df.mid_c.diff()

    wins = pd.Series([x if x >= 0 else 0.0 for x in gains], name="wins")
    losses = pd.Series([x * -1 if x < 0 else 0.0 for x in gains], name="losses")

    wins_rma = wins.ewm(min_periods=num, alpha=alpha).mean()
    losses_rma = losses.ewm(min_periods=num, alpha=alpha).mean()

    rs = wins_rma /losses_rma

    df[f"RSI_{num}"] = 100.0 - (100. / (1.0 + rs))
    return df

def MACD(df: pd.DataFrame, slow=26, fast=12, signal=9):
    ema_long = df.mid_c.ewm(min_periods=slow, span=slow).mean()
    ema_short = df.mid_c.ewm(min_periods=fast, span=fast).mean()

    df["MACD"] = ema_short - ema_long
    df["SIGNAL"] = df.MACD.ewm(min_periods=signal, span=signal).mean()
    df["HIST"] = df.MACD - df.SIGNAL

    return df  