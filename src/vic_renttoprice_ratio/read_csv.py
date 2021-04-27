import pandas as pd
import re

# suburb name replace dict
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

def read_csv_clean(data):
    data['NAME'] = data['NAME'].apply(lambda x: re.sub(r"\(.*\)", "", x))
    data['NAME'] = data['NAME'].str.strip()

    for sub in suburb_replace:
        data['NAME'] = data['NAME'].replace(sub, suburb_replace[sub])

    data.set_index('NAME', inplace=True)
    data = data.unstack()
    data = pd.DataFrame(data)
    data.reset_index(inplace=True)
    return data

# def edit_suburb_name(data):


if __name__ == "__main__":

    # house price
    house_price = pd.read_csv("../../data/raw/test.csv")
    house_price = house_price.drop(columns=['change', 'change.1', 'Growth PA', 'Unnamed: 16'])
    house_price = house_price.rename(columns={'locality': 'NAME', 'prelim 2020': '2020'})
    house_price['2020'] = house_price['2020'].fillna("0").astype(int)
    house_price = read_csv_clean(house_price)
    house_price = house_price.rename(columns={'level_0': 'Year', 0: 'House_Price'})

    # unit price
    unit_price = pd.read_csv("../../data/raw/Suburb_Unit_Final.csv")
    unit_price = unit_price.drop(columns=['change', 'change.1', 'Growth PA', 'Unnamed: 16'])
    unit_price = unit_price.rename(columns={'locality': 'NAME', 'prelim 2020': '2020'})
    unit_price['2020'] = unit_price['2020'].fillna("0").astype(int)
    unit_price = read_csv_clean(unit_price)
    unit_price = unit_price.rename(columns={'level_0': 'Year', 0: 'Unit_Price'})

    # rent price
    rent = pd.read_excel("../../data/raw/1.xlsx", None)
    flat_rent = rent['1bedflat']
    house_rent = rent['2bedhouse']
    flat_rent = flat_rent.astype(int)
    house_rent = house_rent.astype(int)
    flat_rent.reset_index(inplace=True)
    house_rent.reset_index(inplace=True)
    flat_rent["location"] = flat_rent["location"].str.upper()
    house_rent["location"] = house_rent["location"].str.upper()
    flat_rent = flat_rent.rename(columns={'location': 'NAME'})
    house_rent = house_rent.rename(columns={'location': 'NAME'})

    house_rent = read_csv_clean(house_rent)
    flat_rent = read_csv_clean(flat_rent)

    # print(house_price.info())
    # print(unit_price.info())


