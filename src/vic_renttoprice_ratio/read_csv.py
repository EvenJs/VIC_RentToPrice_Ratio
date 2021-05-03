import re
import pandas as pd

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


def read_house_price_csv(data):
    data = data.drop(columns=['change', 'change.1', 'Growth PA', 'Unnamed: 16'])
    data = data.rename(columns={'locality': 'NAME', 'prelim 2020': '2020'})
    data['2020'] = data['2020'].fillna("0").astype(int)
    data = read_csv_clean(data)
    data = data.rename(columns={'level_0': 'Year', 0: 'House_Price'})
    return data


def read_unit_price_csv(data):
    data = data.drop(columns=['change', 'change.1', 'Growth PA', 'Unnamed: 16'])
    data = data.rename(columns={'locality': 'NAME', 'prelim 2020': '2020'})
    data['2020'] = data['2020'].fillna("0").astype(int)
    data = read_csv_clean(data)
    data = data.rename(columns={'level_0': 'Year', 0: 'Unit_Price'})
    return data


def read_rent_csv(data):
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
    flat_rent = flat_rent.rename(columns={'location': 'NAME'})
    house_rent = house_rent.rename(columns={'location': 'NAME'})

    house_rent = read_csv_clean(house_rent)
    flat_rent = read_csv_clean(flat_rent)

    flat_rent = flat_rent.rename(columns={'level_0': 'Year', 'location': 'NAME', 0: 'Flat_rent'})
    flat_rent['Year'] = flat_rent['Year'].astype(str)
    house_rent = house_rent.rename(columns={'level_0': 'Year', 'location': 'NAME', 0: 'House_rent'})
    house_rent['Year'] = house_rent['Year'].astype(str)
    return flat_rent, house_rent


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


def merge_table(data1, data2):
    table = pd.merge(data1, data2, on=['Year', 'NAME'], how='outer')
    return table


def format_table(table):
    table['House_Price'].replace('-', 0, inplace=True)
    table['Unit_Price'].replace('-', 0, inplace=True)
    table['House_Price'] = table['House_Price'].astype(float)
    table['Unit_Price'] = table['Unit_Price'].astype(float)
    return table


def cal_ratio(table):
    table['House_rate'] = table['House_Price'] / table['House_rent'] / 52
    table['Unit_rate'] = table['Unit_Price'] / table['Flat_rent'] / 52
    return table


def main():
    # house price
    house_price = pd.read_csv("../../data/raw/vic_house_price.csv")
    house_price = read_house_price_csv(house_price)

    # unit price
    unit_price = pd.read_csv("../../data/raw/Suburb_Unit_Final.csv")
    unit_price = read_unit_price_csv(unit_price)

    # rent price
    rent = pd.read_excel("../../data/raw/vic_rent.xlsx", None)
    flat_rent1, house_rent1 = read_rent_csv(rent)

    raw_table = merge_table(house_price, unit_price)
    raw_table = merge_table(raw_table, flat_rent1)
    raw_table = merge_table(raw_table, house_rent1)

    raw_table = format_table(raw_table)

    raw_table = cal_ratio(raw_table)
#    print(raw_table)
    return raw_table


if __name__ == "__main__":
    main()
