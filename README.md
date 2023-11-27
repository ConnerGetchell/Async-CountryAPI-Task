# Async-CountryAPI-Task:
Conner Getchell
11/26/23

A task to be completed for Altair Data job interview. 

# How to Run:
1. Pull down repo
2. Terminal: Navigate to .\venv\Scripts
3. Terminal: 'activate' to start virtual enviroment
4. Terminal: Navigate back to root directory of project
5. Terminal: 'pip install -r requirements.txt'
6. Terminal: Finally, run the application with 'py main.py'

# Notes:
1. Normally I would git ignore the virtual enviroment, but for the sake of demonstration in this application I felt that I should include it:
    * Environments:
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/ are included in this project repo!!

2. Python version 3.9.7 
    * aiohttp is not yet compatible with 3.12.x

3. I had to change to the WindowsSelectorEventLoopPolicy for Windows on this version of Python for async methods. The default was seemingly working,
but for each async function I was getting a RuntimeEror: Event loop is closed. This solution cleaned that up for Windows users.

4. The script is called "main.py"

# Task at hand:
Objective: Create a Python script that asynchronously pulls data for three different countries from the
RESTCountries API, returning the currency, capital, and alternate spellings for each country.

Technical Requirements:
1. Set up the project in a virtual environment using Python 3.9 or higher.
2. Provide a requirements.txt file that lists the packages installed via pip to make the script run.
3. Ensure asynchronous interaction with the API using the aiohttp and asyncio Python libraries.

Specific Tasks:
* Use the RESTCountries API to retrieve information for three countries.
    * One of the countries must be the United States of America, participant can choose the
    other two countries.
    * The endpoint used to retrieve this information is up to the participant (refer to the API
    documentation for options).

* Extract and print the following information for each country:
    * Country Name, Currency, Capital, Alternate Spellings
* Write these four data elements to a CSV with the four categories as columns, as shown below.

| country_name              | currency            | capital            | alt_spellings                     |
|---------------------------|---------------------|--------------------|-----------------------------------|
| United States of America  | United States Dollar| Washington, D.C.   | USA, US, United States of America |
| Canada                    | Canadian Dollar     | Ottawa             | CA                                |
| Germany                   | Euro                | Berlin             | Deutschland                       |

Additional Considerations:
* Handle errors gracefully (e.g., network errors, API request errors).
* Implement proper asynchronous handling using asyncio and aiohttp libraries.
* Implement some sort of logging using the logging library.
* Organize the code into functions or classes for better readability and maintainability.

