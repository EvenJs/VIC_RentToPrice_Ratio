import requests
import pandas as pd
import re


url = 'https://data.gov.au/geoserver/vic-suburb-locality-boundaries-psma-administrative-boundaries/wfs?request=' \
      'GetFeature&typeName=ckan_af33dd8c_0534_4e18_9245_fc64440f742e&outputFormat=json'
res = requests.get(url)
# vic_map = json.loads(res)
vic_map = res.json()


suburb_replace = {'BALCOMBE': 'MOOROODUC',
                  'FIVEWAYS': 'CRANBOURNE SOUTH',
                  'JEERALANG NORTH': 'JEERALANG',
                  'KANGAROO GROUND SOUTH': 'KANGAROO GROUND',
                  'SANCTUARY LAKES': 'COCOROC',
                  'SYNDAL': 'GLEN WAVERLEY',
                  'WOOLAMAI WATERS': 'CAPE WOOLAMAI',
                  'WEST ST KILDA': 'ST KILDA WEST',
                  'ST KILDA RD': 'ST KILDA',
                  'EAST ST KILDA': 'ST KILDA EAST',
                  'EAST HAWTHORN': 'HAWTHORN EAST',
                  'EAST BRUNSWICK': 'BRUNSWICK EAST',
                  'WEST BRUNSWICK': 'BRUNSWICK WEST',
                  'MT ELIZA': 'MOUNT ELIZA',
                  'MT MARTHA': 'MOUNT MARTHA',
                  'BENDIGO EAST': 'EAST BENDIGO',
                  'NEWCOMBE': 'NEWCOMB',
                  'WANAGARATTA': 'WANGARATTA',
                  }


# ----------------------------------------------------------------------
# house price
data = pd.read_csv("../../data/raw/test.csv")
data = data.drop(columns=['change', 'change.1', 'Growth PA', 'Unnamed: 16'])
data = data.rename(columns={'locality': 'NAME', 'prelim 2020': '2020'})
data['2020'] = data['2020'].fillna("0").astype(int)

data['NAME'] = data['NAME'].apply(lambda x: re.sub(r"\(.*\)", "", x))
data['NAME'] = data['NAME'].str.strip()

data.replace('BALCOMBE', 'MOOROODUC', inplace=True)
data.replace('FIVEWAYS', 'CRANBOURNE SOUTH', inplace=True)
data.replace('JEERALANG NORTH', 'JEERALANG', inplace=True)
data.replace('KANGAROO GROUND SOUTH', 'KANGAROO GROUND', inplace=True)
data.replace('SANCTUARY LAKES', 'COCOROC', inplace=True)
data.replace('SYNDAL', 'GLEN WAVERLEY', inplace=True)
data.replace('WOOLAMAI WATERS', 'CAPE WOOLAMAI', inplace=True)

data.set_index('NAME', inplace=True)
house_price = data.unstack()
house_price = pd.DataFrame(house_price)
house_price.reset_index(inplace=True)
house_price = house_price.rename(columns={'level_0': 'Year', 0: 'House_Price'})

# --------------------------------------------------------------------
# unit price
data = pd.read_csv("../../data/raw/Suburb_Unit_Final.csv")
data = data.drop(columns=['change', 'change.1', 'Growth PA', 'Unnamed: 16'])

data = data.rename(columns={'locality': 'NAME', 'prelim 2020': '2020'})
data['2020'] = data['2020'].fillna("0").astype(int)
data['NAME'] = data['NAME'].apply(lambda x: re.sub(r"\(.*\)", "", x))
data['NAME'] = data['NAME'].str.strip()

data.replace('BALCOMBE', 'MOOROODUC', inplace=True)
data.replace('FIVEWAYS', 'CRANBOURNE SOUTH', inplace=True)
data.replace('JEERALANG NORTH', 'JEERALANG', inplace=True)
data.replace('KANGAROO GROUND SOUTH', 'KANGAROO GROUND', inplace=True)
data.replace('SANCTUARY LAKES', 'COCOROC', inplace=True)
data.replace('SYNDAL', 'GLEN WAVERLEY', inplace=True)
data.replace('WOOLAMAI WATERS', 'CAPE WOOLAMAI', inplace=True)

data.set_index('NAME', inplace=True)
unit_price = data.unstack()
unit_price = pd.DataFrame(unit_price)
unit_price.reset_index(inplace=True)
unit_price = unit_price.rename(columns={'level_0': 'Year', 0: 'Unit_Price'})

# --------------------------------------------------------
# RENTAL
data = pd.read_excel("../../data/raw/1.xlsx", None)
flat_rent = data['1bedflat']
house_rent = data['2bedhouse']

flat_rent.set_index(["location"], inplace=True)
house_rent.set_index(["location"], inplace=True)

flat_rent = flat_rent.astype(int)
house_rent = house_rent.astype(int)

flat_rent.reset_index(inplace=True)
house_rent.reset_index(inplace=True)

flat_rent["location"] = flat_rent["location"].str.upper()
house_rent["location"] = house_rent["location"].str.upper()

flat_rent.replace('WEST ST KILDA', 'ST KILDA WEST', inplace=True)
flat_rent.replace('ST KILDA RD', 'ST KILDA', inplace=True)
flat_rent.replace('EAST ST KILDA', 'ST KILDA EAST', inplace=True)
flat_rent.replace('EAST HAWTHORN', 'HAWTHORN EAST', inplace=True)
flat_rent.replace('EAST BRUNSWICK', 'BRUNSWICK EAST', inplace=True)
flat_rent.replace('WEST BRUNSWICK', 'BRUNSWICK WEST', inplace=True)
flat_rent.replace('MT ELIZA', 'MOUNT ELIZA', inplace=True)
flat_rent.replace('MT MARTHA', 'MOUNT MARTHA', inplace=True)
flat_rent.replace('BENDIGO EAST', 'EAST BENDIGO', inplace=True)
flat_rent.replace('NEWCOMBE', 'NEWCOMB', inplace=True)
flat_rent.replace('WANAGARATTA', 'WANGARATTA', inplace=True)

house_rent.replace('WEST ST KILDA', 'ST KILDA WEST', inplace=True)
house_rent.replace('ST KILDA RD', 'ST KILDA', inplace=True)
house_rent.replace('EAST ST KILDA', 'ST KILDA EAST', inplace=True)
house_rent.replace('EAST HAWTHORN', 'HAWTHORN EAST', inplace=True)
house_rent.replace('EAST BRUNSWICK', 'BRUNSWICK EAST', inplace=True)
house_rent.replace('WEST BRUNSWICK', 'BRUNSWICK WEST', inplace=True)
house_rent.replace('MT ELIZA', 'MOUNT ELIZA', inplace=True)
house_rent.replace('MT MARTHA', 'MOUNT MARTHA', inplace=True)
house_rent.replace('BENDIGO EAST', 'EAST BENDIGO', inplace=True)
house_rent.replace('NEWCOMBE', 'NEWCOMB', inplace=True)
house_rent.replace('WANAGARATTA', 'WANGARATTA', inplace=True)

flat_rent.set_index('location', inplace=True)
flat_rent = flat_rent.unstack()
flat_rent = pd.DataFrame(flat_rent)
flat_rent.reset_index(inplace=True)
flat_rent = flat_rent.rename(columns={'level_0': 'Year', 'location': 'NAME', 0: 'Flat_rent'})
flat_rent['Year'] = flat_rent['Year'].astype(str)

house_rent.set_index('location', inplace=True)
house_rent = house_rent.unstack()
house_rent = pd.DataFrame(house_rent)
house_rent.reset_index(inplace=True)
house_rent = house_rent.rename(columns={'level_0': 'Year', 'location': 'NAME', 0: 'House_rent'})
house_rent['Year'] = house_rent['Year'].astype(str)

# ---------------------------------
# make a final table
raw_data = pd.merge(house_price, unit_price, on=['Year', 'NAME'], how='outer')
raw_data = pd.merge(raw_data, flat_rent, on=['Year', 'NAME'], how='outer')
raw_data = pd.merge(raw_data, house_rent, on=['Year', 'NAME'], how='outer')

raw_data['House_Price'].replace('-', 0, inplace=True)
raw_data['Unit_Price'].replace('-', 0, inplace=True)
raw_data['House_Price'] = raw_data['House_Price'].astype(float)
raw_data['Unit_Price'] = raw_data['Unit_Price'].astype(float)

# calculate the rent to price ratio
raw_data['House_rate'] = raw_data['House_Price']/raw_data['House_rent']/52
raw_data['Unit_rate'] = raw_data['Unit_Price']/raw_data['Flat_rent']/52

# raw_data.to_csv("../../data/processed/raw_data.csv")
