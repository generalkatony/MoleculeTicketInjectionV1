import pandas as pd
import requests
import json
import re

url = "https://app.molecule.io/api/v2/inventory/tickets"

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-email": "ccheong@qsol.co.uk",
    "x-token": "cYmDx-EcNdgwqepjUM5j"
}

df = pd.read_csv(r"C:\Users\cheng\PycharmProjects\MoleculeTicketInjection\Test Data\InvenTest.csv", header=0)
print(df)
df = df.drop('id', axis=1)


# Convert TRADE_DATE column to desired format

df['as_of'] = pd.to_datetime(df['as_of']).dt.strftime('%d/%m/%y')

print(df)

payload = {
    "fulfillment_date": "2023-10-09 11:48:43.930787",
    "commodity": "NG",
    "volume": 100,
    "price": 80
}

response = requests.post(url, json=payload, headers=headers)
print(response.text)