import pandas as pd, yfinance as yf, sqlite3, os

d = r"D:/MSC Practicals/Data Science/Practical - 4/"
df = pd.read_csv(os.path.join(d, "Inputs/VKHCG_Shares.csv"))
c = sqlite3.connect(os.path.join(d, "Outputs/Shares.db"))

for s,u,t in zip(df["Shares"], df["Units"], df["sTable"]):
    try:
        x = yf.download(s, progress=False, threads=False, auto_adjust=True)
        if "/" in s:
            raise ValueError("Invalid ticker format")

        if not x.empty:
            x["UnitsOwn"], x["ShareCode"] = u, s
            x.to_csv(os.path.join(d,f"Outputs/{t}.csv"), index=False)
            x.to_sql(t, c, if_exists="replace", index=False)
            print(f"Completed {s}")
        else: print(f"Error {s}")
    except: print(f"Skipped {s} due to exception")

c.close()
print("Done")
