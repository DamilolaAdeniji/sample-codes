import logging
import pandas as pd
import azure.functions as func
import json
from dotenv import load_dotenv
import os
load_dotenv()


def main(req: func.HttpRequest) -> func.HttpResponse:
    accountName = os.environ['ACCOUNT_NAME']
    containerName = os.environ['containername']
    filename = os.environ['filename']


#    logging.info('Python HTTP trigger function processed a request.')
    df = pd.read_excel(f'https://{accountName}.blob.core.windows.net/{containerName}/{filename}')
    df = df[df.columns[:2]]
    latest_price = df[df.DATE == df.DATE.max()].iloc[0][1]
    df = df[df.DATE < df.DATE.min()]
    previous_price = df[df.DATE == df.DATE.max()].iloc[0][1]
    performance = round((latest_price/previous_price - 1) * 100,2)

    result = {"latest_value": latest_price,"previous_value":previous_price,"performance":f'{performance}%'}
    
    return func.HttpResponse(json.dumps(result), mimetype="application/json")
 #   return func.HttpResponse('{'+"'"+'price'+"'"+':'"'"+f"{latest_price}"+"'"+'}', mimetype="text/plain")

   
