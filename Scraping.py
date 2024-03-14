import requests
from bs4 import BeautifulSoup


# Function to search DuckDuckGo and get PyPI URLs
def search_duckduckgo(query):
    url = f"https://duckduckgo.com/html/?q=site:pypi.org+ {query} +explanation"
    response = requests.get(url)
    print(response.reason)
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='result__url')
    pypi_urls = [link['href'] for link in results if 'pypi.org/project/' in link['href']]
    return pypi_urls[:20]


# Function to extract package descriptions from PyPI pages
def get_package_descriptions(urls):
    package_descriptions = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        description_tag = soup.find('div', class_='project-description')
        if description_tag:
            description = description_tag.text.strip()
            package_descriptions.append((url, description))
    return package_descriptions


def main():
    search_word = input("Enter search word: ")
    pypi_urls = search_duckduckgo(search_word)
    package_descriptions = get_package_descriptions(pypi_urls)
    print(pypi_urls)
    saved_packages = [pkg for pkg in package_descriptions if True]

    #with open("saved_packages.txt", "w") as f:
    #    for pkg in saved_packages:
    #        f.write(f"{pkg[0]}\n{pkg[1]}\n\n")


if __name__ == "__main__":
    main()
