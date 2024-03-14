# Webscraper

This is an automated scraping tool dedicated to gather information about implementation of explainable AI algorithms 
([see examples](info/Algorithms1.png)) 

## Run tool 

Run the following command in order to get the results in a text file. 

```shell
Python3 Scraping.py 
```


---
**NOTE**

The tool will ask you to enter a search word. The search for packages is then being made using duckduckgo and the following query: 
**site:pypi.org {your word} explanation**

---


## Dependencies
- [Requests 2.31.0](https://pypi.org/project/requests/#description) 
- [beautifulsoup4 4.12.3](https://pypi.org/project/beautifulsoup4/) 
