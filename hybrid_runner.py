import pandas as pd
import os
from indicators import stochastic, pivot_points_daily, ema, macd

SYMBOLS = [   
    "SUCE", "DCRC", "GOCO", "ELNA", "CFGH", "TALM",
    "APSW", "AIFI", "ACAMD", "SCTS", "QNBE", "BTFH",
    "DTPP", "AFDI", "DOMT", "EGBE", "ROTO", "EPPK",
    "GRCA", "VALU", "CANA", "OIH", "JUFO", "CCAP",
    "RACC", "FWRY", "UBEE", "EGCH", "CPCI", "LCSW",
    "WCDF", "AIHC", "SNFC", "OFH", "CCRS", "CIEB",
    "ZMID", "RTVC", "SPIN", "PHTV", "PHAR", "TMGH",
    "OCDI", "EFIC", "UEFM", "AMES", "MBSC", "ADIB",
    "BINV", "ORWE", "ADCI", "NAHO", "FAIT", "RREI",
    "MCRO", "AREH", "IBCT", "PHDC", "ENGC", "MPRC",
    "SDTI", "MEPA", "RUBX", "EBSC", "GGRN", "ARAB",
    "SUGR", "ZEOT", "WKOL", "NCCW", "EGAL", "SCFM",
    "PHGC", "ABUK", "RAYA", "FERC", "EHDR", "EAST",
    "INFI", "AIDC", "MOIN", "KWIN", "MBEG", "OBRI",
    "ATQA", "GSSC", "AFMC", "TANM", "ISMA", "GIHD",
    "IEEC", "ACAP", "PRCL", "GTEX", "CEFM", "ACRO",
    "CRST", "SCEM", "EXPA", "MCQE", "CLHO", "ORAS",
    "EALR", "MASR", "ELKA", "DAPH", "MHOT", "NAPR",
    "MPCI", "UNIT", "EIUD", "OLFI", "BIDI", "UNIP",
    "EEII", "ELEC", "ORHD", "ASCM", "CERA", "NARE",
    "HELI", "ARCC", "KZPC", "ASPI", "NHPS", "PRDC",
    "EDFM", "POUL", "KRDI", "GTWL", "SKPC", "BIOC",
    "MFPC", "ANFI", "ISPH", "EKHOA", "SPMD", "INEG",
    "ADPC", "EGAS", "ACTF", "MAAL", "ICFC", "MICH",
    "HBCO", "AMIA", "COPR", "SAUD", "CIRA", "NIPH",
    "NINH", "ELSH", "GBCO", "EASB", "HRHO", "GGCC",
    "ICID", "CNFN", "MIPH", "EGTS", "EMFD", "SMFR",
    "AALR", "ALUM", "ISMQ", "EFID", "HDBK", "SWDY",
    "GDWA", "TAQA", "UEGC", "AMOC", "ARVA", "AMER",
    "KABO", "BONY", "ALCN", "RMDA", "ACGC", "MENA",
    "MOSC", "ECAP", "OCPH", "MPCO", "DSCW", "ATLC",
    "EPCO", "ETEL", "CSAG", "CICH", "AJWA", "CAED",
    "COMI", "SVCE", "EFIH", "IFAP", "SIPC", "MOED",
    "IDRE", "ODIN", "PRMH", "MILS", "ETRS", "COSG",
    "SEIG", "GPPL", "DEIN",
]

def load_csv(symbol):
    file_path = f"data/{symbol}.csv"
    if not os.path.exists(file_path):
        print(f"[{symbol}] ❌ لا يوجد ملف CSV → NO DATA")
        return None
    df = pd.read_csv(file_path)
    if not set(["open","high","low","close","volume"]).issubset(df.columns):
        print(f"[{symbol}] ❌ CSV ناقص أعمدة → NO DATA")
        return None
    return df

def analyze(symbol):
    df = load_csv(symbol)
    if df is None or len(df) < 50:
        return {"symbol": symbol, "score": 0, "reason": "NO_DATA"}

    # Stochastic daily
    k, d = stochastic(df)
    last_k = float(k.iloc[-1])
    last_d = float(d.iloc[-1])
    stoch_cross = k.iloc[-2] < d.iloc[-2] and k.iloc[-1] > d.iloc[-1]

    # Pivot
    P, R1, S1, R2, S2 = pivot_points_daily(df)

    # EMA
    ema20 = float(ema(df['close'], 20).iloc[-1])
    ema50 = float(ema(df['close'], 50).iloc[-1])
    ema_cross = ema20 > ema50

    # MACD
    macd_line, signal_line = macd(df['close'])
    macd_cross = macd_line.iloc[-2] < signal_line.iloc[-2] and macd_line.iloc[-1] > signal_line.iloc[-1]

    # Scoring
    score = 0
    if ema_cross: score += 2
    if macd_cross: score += 2
    if stoch_cross: score += 2
    if last_d < 20: score += 1  # oversold

    return {
        "symbol": symbol,
        "score": score,
        "k": last_k,
        "d": last_d,
        "pivot_P": P,
        "pivot_R1": R1,
        "pivot_S1": S1,
        "ema_cross": ema_cross,
        "macd_cross": macd_cross,
    }

def run():
    results = []
    for symbol in SYMBOLS:
        print(f"\nتحليل {symbol} ...")
        res = analyze(symbol)
        print(res)
        results.append(res)

    # ترتيب النتائج
    top = sorted([r for r in results if r["score"] > 0], key=lambda x: x["score"], reverse=True)

    print("\n--- TOP RESULTS ---")
    for r in top:
        print(r)

if __name__ == "__main__":
    run()
