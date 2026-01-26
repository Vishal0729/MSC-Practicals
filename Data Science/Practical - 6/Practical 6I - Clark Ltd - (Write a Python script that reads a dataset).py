import os
import pandas as pd
# File paths
Base = r"D:/MSC Practicals/Data Science/Practical - 6/"
input_file = os.path.join(Base, "Inputs/Process_ExchangeRates.csv")
output_file = os.path.join(Base, "Outputs/Forex_Trades_Output.csv")
# Load forex data WITHOUT warnings
df = pd.read_csv(input_file, dtype=str, low_memory=False)
# Convert Rate column to float (because dtype=str)
df["Rate"] = df["Rate"].astype(float)
# Start with $1,000,000 USD
money = 1_000_000
history = []
for _, row in df.iterrows():
    rate = row["Rate"]
    # USD → GBP
    gbp = money * rate
    # GBP → USD (reverse conversion)
    usd = gbp / rate
    money = round(usd, 2)
    history.append([row["Date"], money, "USD"])
# Save results
out = pd.DataFrame(history, columns=["Date", "Money", "Currency"])
out.to_csv(output_file, index=False)
print("Final money:", money)
print("Output saved at:", output_file)