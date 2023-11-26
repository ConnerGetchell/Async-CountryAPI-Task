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
    logging.info(f"Fetched data for {countries}")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_country_info(session, country) for country in countries]
        return await asyncio.gather(*tasks)


def extract_countries_info(data):
    """
    Extracts data from JSON object into Pandas DF.
    Returns: a DataFrame containing country data: 'country_name', 'currency', 'capital', 'alt_spellings'
    """
    # Create an empty DataFrame in event that no data is returned
    countries_df = pd.DataFrame(columns=['country_name', 'currency', 'capital', 'alt_spellings'])
    country_df = pd.DataFrame(columns=['country_name', 'currency', 'capital', 'alt_spellings'])

    for country_data in data:
        try:
            country_name = country_data['name']['common'] if 'name' in country_data else ''
            currency = next(iter(country_data['currencies'].values()), {}).get('name', '') if 'currencies' in country_data else ''
            capital = country_data['capital'][0] if 'capital' in country_data else ''
            alt_spellings = ', '.join(country_data['altSpellings']) if 'altSpellings' in country_data else ''

            # Create a DataFrame for the current country
            country_df = pd.DataFrame([{
                'country_name': country_name,
                'currency': currency,
                'capital': capital,
                'alt_spellings': alt_spellings
            }])
        except Exception as e:
            logging.error(f"Error extracting country from object: {e}")

        # Concat the current country DataFrame to the countries DataFrame
        countries_df = pd.concat([countries_df, country_df], ignore_index=True)

    return countries_df.drop_duplicates()


async def main():
    countries = ['United States of America', 'Canada', 'Germany']
    countries_info = await get_countries_info(countries)

    countries_df = extract_countries_info(countries_info)
    print(countries_df) # Print data to console as per requirement
    countries_df.to_csv('countries_data.csv', index=False)

    


if __name__ == "__main__":
    asyncio.run(main())