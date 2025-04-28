from openaq import OpenAQ
from pandas import json_normalize
import pandas as pd
import dotenv
import os

dotenv.load_dotenv()
API_KEY = os.environ.get('OPENAQ_API_KEY')

client = OpenAQ(api_key=API_KEY)
response = client.locations.list(
    bbox=[-0.464172,5.449908,0.030212,5.691491]
)
data = response.dict()
# print(data)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
df = json_normalize(data['results'])
print(df.head())
print(df['sensors'].head())
print(df.columns.tolist())
print(response.headers)
client.close()