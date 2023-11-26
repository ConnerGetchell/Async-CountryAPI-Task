# Standard library imports
import sys
import os
import logging
import asyncio
import csv

# Third-party imports
import aiohttp

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
    url = f'https://restcountries.com/v3.1/name/{country}?fullText=true'
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


def write_to_csv(data):
    """Writes countries data to CSV file."""
    filename = 'countries_info.csv'
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['country_name', 'currency', 'capital', 'alt_spellings']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for country_data in data:
                writer.writerow({
                    'country_name': country_data['name']['common'] 
                        if 'name' in country_data else '',
                    'currency': next(iter(country_data['currencies'].values()), {}).get('name', '') 
                        if 'currencies' in country_data else '',
                    'capital': country_data['capital'][0] 
                        if 'capital' in country_data else '',
                    'alt_spellings': ', '.join(country_data['altSpellings']) 
                        if 'altSpellings' in country_data else ''
                })

        logging.info(f"Succesfully wrote to CSV: {filename}")
    except Exception as e:
        logging.error(f"Error writing to CSV: {e}")


async def main():
    countries = ['United States of America', 'Canada', 'Federal Republic of Germany']
    countries_info = await get_countries_info(countries)
    write_to_csv(countries_info)


if __name__ == "__main__":
    asyncio.run(main())