import pandas as pd
import numpy as np

data_types = ["val", "test"]
tp_threshold = 0.97
tn_threshold = 0.99

for data_type in data_types:
    print(f"Data type: {data_type}")
    df = pd.read_csv(f"~/Downloads/cpp_results_{data_type}.csv")
    dfmc = pd.read_csv(f"~/Downloads/cpp_results_{data_type}_with_mc.csv")
    df = df.dropna(axis=0).astype(float)
    dfmc = dfmc.dropna(axis=0).astype(float)

    print(f"Average change in tp_precision after new calibration: {(df['tp_precision.1'] - df['tp_precision']).mean()}")
    print(f"Average change in tp_precision after multicalibrate + new calibration: {(dfmc['tp_precision.1'] - dfmc['tp_precision']).mean()}\n")

    print(f"Average change in tn_precision after new calibration: {(df['tn_precision.1'] - df['tn_precision']).mean()}")
    print(f"Average change in tn_precision after multicalibrate + new calibration: {(dfmc['tn_precision.1'] - dfmc['tn_precision']).mean()}\n")

    print(f"Average change in tp_percent after new calibration: {(df['tp_percent.1'] - df['tp_percent']).mean()}")
    print(f"Average change in tp_percent after multicalibrate + new calibration: {(dfmc['tp_percent.1'] - dfmc['tp_percent']).mean()}\n")

    print(f"Average change in tn_percent after new calibration: {(df['tn_percent.1'] - df['tn_percent']).mean()}")
    print(f"Average change in tn_percent after multicalibrate + new calibration: {(dfmc['tn_percent.1'] - dfmc['tn_percent']).mean()}\n")

    print(f"Average change in total_coverage after new calibration: {(df['total_coverage.1'] - df['total_coverage']).mean()}")
    print(f"Average change in total_coverage after multicalibrate + new calibration: {(dfmc['total_coverage.1'] - dfmc['total_coverage']).mean()}\n")

    print(f"Average change in total_ar after new calibration: {(df['total_ar.1'] - df['total_ar']).mean()}")
    print(f"Average change in total_ar after multicalibrate + new calibration: {(dfmc['total_ar.1'] - dfmc['total_ar']).mean()}\n")
