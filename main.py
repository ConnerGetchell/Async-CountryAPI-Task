# Standard library imports
import sys
import asyncio
import logging
import csv
# Third-party imports
import aiohttp

# Change the event loop policy to WindowsSelectorEventLoopPolicy for Windows
# See README.md for more details
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)



async def fetch_country_info(session, country):
    url = f'https://restcountries.com/v3.1/name/{country}?fullText=true'
    try:
        async with session.get(url) as response:
            data = await response.json()
            return data[0]
    except Exception as e:
        logging.error(f"Error fetching data for {country}: {e}")
        return None


async def get_countries_info(countries):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_country_info(session, country) for country in countries]
        return await asyncio.gather(*tasks)

# Dynamically find the first currency based on the currency code, returns empty string if no currency is found
def get_first_currency(country_data):
    if 'currencies' in country_data and country_data['currencies']:
        currency_code = next(iter(country_data['currencies']))
        return country_data['currencies'][currency_code]['name']
    return ''

def write_to_csv(data):
    with open('countries_info.csv', 'w', newline='') as csvfile:
        fieldnames = ['country_name', 'currency', 'capital', 'alt_spellings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for country_data in data:
            writer.writerow({
                'country_name': country_data['name']['common'],
                'currency': get_first_currency(country_data),
                'capital': country_data['capital'][0] if 'capital' in country_data else '',
                'alt_spellings': ', '.join(country_data['altSpellings']) if 'altSpellings' in country_data else ''
            })


async def main():
    countries = ['United States of America', 'Canada', 'Federal Republic of Germany']
    countries_info = await get_countries_info(countries)
    write_to_csv(countries_info)


if __name__ == "__main__":
    asyncio.run(main())