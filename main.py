# Standard library imports
import sys
import os
import logging
import asyncio

# Third-party imports
import aiohttp
import pandas as pd

# Change the event loop policy to WindowsSelectorEventLoopPolicy for Windows.
# See README.md for more details
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set logging level to INFO for standard output.
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), stream=sys.stdout)


async def fetch_country_info(session, country):
    """
    Asynchronously fetches data for a single country.
    Returns: a dictionary of country data.
    """
    url = f'https://restcountries.com/v3.1/name/{country}'
    try:
        async with session.get(url) as response:
            if response.status != 200:
                error_data = await response.json()
                logging.error(f"Error fetching data for {country}: {error_data['message']}, status code: {response.status}")
                return None
            data = await response.json()
            return data[0]
    except Exception as e:
        logging.error(f"Error fetching data for {country}: {e}")
        return None


async def get_countries_info(countries):
    """
    Asynchronously fetches data for all countries in list.
    Returns: a list of country data dictionaries.
    """
    logging.info(f"Fetching data for {countries}")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_country_info(session, country) for country in countries]
        return await asyncio.gather(*tasks, return_exceptions=True)


def extract_country_data(country_data):
    '''
    Extracts the country name, currency, capital, and alternative spellings from the country data object.
    Returns: a dictionary of country data.
    '''
    try:
        return {
            'country_name': country_data['name']['common'] if 'name' in country_data else '',
            'currency': next(iter(country_data['currencies'].values()), {}).get('name', '') if 'currencies' in country_data else '',
            'capital': country_data['capital'][0] if 'capital' in country_data else '',
            'alt_spellings': ', '.join(country_data['altSpellings']) if 'altSpellings' in country_data else ''
        }
    except Exception as e:
        logging.error(f"Error extracting country from object: {e}")
        return None

def format_countries_info(data):
    '''
    Formats the country data dict into a dataframe.
    Returns: a dataframe of country data.
    '''
    country_dicts = []
    for country_data in data:
        if country_data is not None and not isinstance(country_data, Exception):
            country_dict = extract_country_data(country_data)
            if country_dict is not None:
                country_dicts.append(country_dict)
    countries_df = pd.DataFrame(country_dicts)
    return countries_df.drop_duplicates()


def export_data(df):
    """
    Displays the dataframe in a print statement and exports to CSV
    Returns: None
    """
    print(df) # Display the dataframe to console for project requirements
    filename = 'countries_data.csv'
    df.to_csv(filename, index=False)
    if os.path.exists(filename):
        logging.info(f"Successfully created CSV with the name: {filename}.")
    else:
        logging.error(f"Failed to create CSV with the name: {filename}.")


async def main():
    countries = ['United States of America', 'Canada', 'Germany']
    countries_info = await get_countries_info(countries)

    countries_df = format_countries_info(countries_info)
    export_data(countries_df)

  
if __name__ == "__main__":
    asyncio.run(main())