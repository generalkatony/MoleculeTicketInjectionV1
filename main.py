import pandas as pd
import requests
import json
import re

url = "https://app.molecule.io/api/v2/inventory/tickets"

#molecule account x-email & x-token goes here
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-email": "ccheong@qsol.co.uk",
    "x-token": "4sGHjdrxpD8WEri4GLc7"
}

df = pd.read_csv(r"C:\Users\cheng\PycharmProjects\MoleculeTicketInjection\Test Data\InvenTest.csv", header=0)
print(df)
df = df.drop('id', axis=1)
df = df.fillna('')


# Convert TRADE_DATE column to desired format
date_format = '%Y-%m-%d %H:%M:%S'
df['as_of'] = pd.to_datetime(df['as_of'], dayfirst=True).dt.strftime(date_format)

print(df)

#csv to ticket mapping
input1 = 'as_of'
input2 = 'commodity'
input3 = 'volume'
input4 = 'price'
input5 = 'asset_name'
input6 = 'empty'
input7 = 'empty'
input8 = 'empty'
input9 = 'empty'
input10 = 'empty'
input11 = 'empty'
input12 = 'empty'
input13 = 'empty'

####################################################################
#Test Payload
payload = {
    "fulfillment_date":'2010-10-11',
    "commodity": 'NG',
    "volume": 100,
    "price":7,
    "asset":"Waha",
    "status":"estimate",
    "fill": False,
    "final_delivery": False,
    "subleg_id": '',
    "external _id": '',
    "external_source":'',
    "dedupe_external_id":'',
    "custom_field_name":''
}

#response = requests.post(url, data=json.dumps(payload), headers=headers)
#print(response.text)

####################################################################
for idx, data in df.iterrows():
    payload = {
        'fulfillment_date': data[input1],
        'commodity': data[input2],
        'volume': data[input3],
        'price': data[input4],
        'asset': data[input5],
        'status': data[input6],
        "fill": data[input7],
        "final_delivery": data[input8],
        "subleg_id": data[input9],
        "external _id": data[input10],
        "external_source": data[input11],
        "dedupe_external_id": data[input12],
        "custom_field_name": data[input13]
    }

    ###################FILTER DATA###################################
    #remove n/a data from package
    filtered_payload = {key: value for key, value in payload.items() if value is not None and value != '' }

    ########check if 'status' condition is valid##################
    # Define the allowed statuses
    allowed_statuses = ['adjustment', 'estimate', 'in_transit', 'delivered/received']

    if 'status' in filtered_payload and filtered_payload['status'] not in allowed_statuses:
        del filtered_payload['status']

    # Check if 'status' key exists in the dictionary
    if 'status' in filtered_payload:
        print('status =', filtered_payload['status'])
    else:
        print("'status' key does not exist in the dictionary.")
    ###############################################################
    ########check if 'status' condition is valid##################
    # Define the allowed fill
    allowed_fills = ['true', 'false']

    if 'fill' in filtered_payload and filtered_payload['fill'] not in allowed_fills:
        del filtered_payload['fill']

    # Check if 'fill' key exists in the dictionary
    if 'fill' in filtered_payload:
         print('fill =', filtered_payload['fill'])
    else:
         print("'fill' key does not exist in the dictionary.")
    ###############################################################
    #


    response = requests.post(url, data=json.dumps(filtered_payload), headers=headers)
    print(response.text)