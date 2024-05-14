import requests
from bs4 import BeautifulSoup
from itertools import islice
import urllib.parse
import datetime

hasFiltered = False
filteredCount = 0


def makeRequest(query):
    url = f"https://duckduckgo.com/html/?q=site:pypi.org+ {query} + explanation"
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def isValidPacket(description, api_token, query):
    # This Method performs the request to chatGPT API and decides whether Packet should be filtered
    query = """Tell me if the following description of a python package
    describes a package which implements the explainable AI algorithm {}
    also answer binary either "yes" or "no". Description: \n {}.""".format(query, description)

    url = 'https://api.openai.com/v1/chat/completions'

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": query}],
        "temperature": 0.7
    }

    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        assistant_message_content = response_data['choices'][0]['message']['content'].strip()
        if assistant_message_content.lower() == "yes":
            return True
        else:
            return False
    else:
        print("request to chatgpt failed: {} (no filtering will be performed)".format(response.text))
        return True


def filterURLs(urlsAndDescription, query):
    global hasFiltered
    global filteredCount
    # This method asks the User whether an additional filtering shall be performed
    # And if yes perform a request to chatGPTs API
    isFilterActive = input("Do you want to filter the URLs based on descriptions? (y/N): ").lower()
    openAPIToken = None
    filteredURLandDescriptions = []
    if isFilterActive == "y":
        hasFiltered = True
        openAPIToken = input("Please enter your OpenAI API key: ")
        for url, description in urlsAndDescription:
            if isValidPacket(description, openAPIToken, query):
                filteredURLandDescriptions.append((url, description))
            else:
                print("Packet with URL " + url + " has been filtered out. description: \n " + description)
                filteredCount += 1
    else:
        # If no filter is wished all URLS are returned
        return urlsAndDescription
    return filteredURLandDescriptions


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


def outPutResults(urlsAndDescriptionFiltered, query):
    descriptionsWished = input("Do you want the descriptions of the packets included as well ? (y/N): ").lower()
    now = datetime.datetime.now()
    time_string = now.strftime("%Y-%m-%d %H:%M")
    file_name = f"{query} results {time_string}.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(f"{query} search results (Filter on: {hasFiltered}, {filteredCount} results filtered out):\n \n")
        for url, description in urlsAndDescriptionFiltered:
            if descriptionsWished == 'y':
                file.write(f"URL: {url}\nDescription: \n{description}\n\n")
            else:
                file.write(f"URL: {url}\n\n")
    print(f"Results have been written to {file_name}")


# This method coordinates the whole search
def performScraping(query):
    requestedSoup = makeRequest(query)
    urlsAndDescription = filterSoup(requestedSoup)
    urlsAndDescriptionFiltered = filterURLs(urlsAndDescription, query)
    outPutResults(urlsAndDescriptionFiltered, query)


def main():
    search_word = input("Enter search word: ")
    performScraping(search_word)


if __name__ == "__main__":
    main()
