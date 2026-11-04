import pandas as pd

# Split the data into training and testing sets for each asset. This is run once. 
for asset in ["Asset_A", "Asset_B", "Asset_C", "Asset_D", "Asset_E", "Asset_F"]:
    df = pd.read_csv(f"Data/EvaluationData/{asset}.csv", parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    split_index = int(len(df) * 0.8)
    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]


    train_df.to_csv(f"Data/EvaluationData/Training/{asset}_train.csv", index=False)
    test_df.to_csv(f"Data/EvaluationData/Testing/{asset}_test.csv", index=False)

