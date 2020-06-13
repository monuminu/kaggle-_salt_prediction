# -*- coding: utf-8 -*-
import pandas as pd

statement_df = pd.read_csv("statement.csv")
statement_df["Txn Date"] = pd.to_datetime(statement_df["Txn Date"])

df_deposit_withdrawl_balance = statement_df.groupby('Txn Date').agg({'Debit': 'sum', 'Credit': 'sum', "Balance" : "max"})
df_deposit_withdrawl_balance["Gross Income"] = df_deposit_withdrawl_balance["Credit"] - df_deposit_withdrawl_balance["Debit"]

df_deposit_withdrawl = df_deposit_withdrawl_balance[["Debit", "Credit", "Gross Income"]].resample("M").sum().reset_index()
df_balance = df_deposit_withdrawl_balance.reset_index()
df_deposit_withdrawl["Txn Date"] = df_deposit_withdrawl["Txn Date"].dt.strftime('%m/%d/%Y')

df_balance_monthly = df_balance.loc[df_balance.groupby(df_balance["Txn Date"].dt.month).apply(lambda x : x.index.max())].reset_index(drop = True).sort_values(["Txn Date"])[["Txn Date","Balance"]]
df_balance_monthly["Month"] = df_balance_monthly["Txn Date"].dt.strftime('%b-%Y')
df_balance_monthly = df_balance_monthly.drop(["Txn Date"], axis = 1)
df_balance_monthly = df_balance_monthly[["Month", "Balance"]]

total_deposit = 100000
total_withdrawl = 230000