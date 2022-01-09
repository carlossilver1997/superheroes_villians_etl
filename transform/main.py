import argparse
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def main(filename):
    df = _read_data(filename)
    df = _remove_heroes_with_not_valid_publisher(df)
    df = _fill_values_with_custom_value(df,'alignment', 'neutral')
    df = _fill_values_with_custom_value(df,'gender', 'no defined')
    df = _fill_values_with_median(df, ['strength', 'combat', 'durability', 'intelligence', 'power', 'speed'], 'Marvel Comics')
    df = _fill_values_with_median(df, ['strength', 'combat', 'durability', 'intelligence', 'power', 'speed'], 'DC Comics')
    df = _convert_height(df)
    df = _convert_weight(df)
    _save_data(df, filename)
    return df
    

def _read_data(filename):
    logger.info('Reading file {}'.format(filename))
    missing_value_formats = ["-", None, "null"]
    df = pd.read_csv(filename, na_values=missing_value_formats)
    return df

def _fill_values_with_custom_value(df, name_column, value):
    logger.info('Filling values for {} column'.format(name_column))
    df.loc[df[name_column].isnull(),name_column] = value
    return df

def _fill_values_with_median(df, name_columns, publisher):
    logger.info('Filling values for {} columns'.format(", ".join(name_columns)))
    for name_column in name_columns:
        value_filled = df.loc[(df[name_column].notnull()) & (df['publisher'] == publisher), name_column].median()
        df.loc[(df[name_column].isna()) & (df['publisher'] == publisher), name_column] = value_filled
    return df

def _remove_heroes_with_not_valid_publisher(df):
    logger.info('Removing SuperHeroes and Villians don\'t belong Marver or DC Comics universes')
    df.drop(df.loc[(df['publisher'] != 'Marvel Comics') & (df['publisher'] != 'DC Comics'), :].index, inplace=True)
    return df

def convert_to_meters(value):
    try:
        if "cm" in value:
            value = value.strip("cm")
            if isinstance(float(value), float):
                value = float(value)
                value = value / 100
        elif "meters":
            value = value.strip("meters")
        else:
            value = 0
    except:
        value = 0
    
    return value

def convert_to_kilograms(value):
    try:
        if "tons" in value:
            value = value.strip("tons")
            if isinstance(float(value), float):
                value = float(value)
                value = value * 907.185
        elif "kg":
            value = value.strip("kg")
        else:
            value = 0
    except:
        value = 0
    
    return value
        

def _convert_height(df):
    logger.info('Removing SuperHeroes and Villians don\'t belong Marver or DC Comics universes')
    df["height"] = df["height"].apply(convert_to_meters)
    return df

def _convert_weight(df):
    df["weight"] = df["weight"].apply(convert_to_kilograms)
    return df

def _save_data(df, filename):
    logger.info('Saving data at location: {}'.format(filename))
    df.to_csv('clean_{}'.format(filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='The path to dirty data')
    args = parser.parse_args()
    df = main(args.filename)
    print(df)