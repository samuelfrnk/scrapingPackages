import requests
from bs4 import BeautifulSoup
from itertools import islice
import urllib.parse


def makeRequest(query):
    url = f"https://duckduckgo.com/html/?q=site:pypi.org+ {query} +explanation"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def filterURLs(urlsAndDescription):
    # This method asks the User whether an additional filtering shall be performed
    # And if yes perform a request to chatGPTs API
    isFilterActive = input("Do you want to filter the URLs based on descriptions? (y/N): ")
    openAPIToken = None
    # If no filter is wished all URLS are returned
    if isFilterActive == "y":
        openAPIToken = input("Please enter your OpenAI API key: ")
    else:
        return urlsAndDescription





def filterSoup(requestedSoup):
    search_results = requestedSoup.find_all('div', class_='result__extras__url')
    descriptions = requestedSoup.find_all('a', class_='result__snippet')
    url_descriptions = []
    # Zip the raw URLS/descriptions
    zippedURLAndDescriptions = islice(zip(search_results, descriptions), 20)

    for result, description in zippedURLAndDescriptions:
        url = result.find('a').get('href')
        parsed_url = urllib.parse.urlparse(url)
        query_string = urllib.parse.parse_qs(parsed_url.query)
        # url as fallback in case pypi url cannot be fetched
        actual_url = query_string['uddg'][0] if 'uddg' in query_string else url
        desc_text = description.text.strip()
        url_descriptions.append((actual_url, desc_text))
    return url_descriptions


def performScraping(query):
    requestedSoup = makeRequest(query)
    urlsAndDescription = filterSoup(requestedSoup)
    urlsAndDescriptionFiltered = filterURLs(urlsAndDescription)


def main():
    global openAPIToken
    search_word = input("Enter search word: ")
    performScraping(search_word)


if __name__ == "__main__":
    main()
