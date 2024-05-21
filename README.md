# Webscraper - Explainable AI packages

This is an automated scraping tool dedicated to gather information about implementation of explainable AI algorithms 
([see example algorithms](info/Algorithms1.png)). The main goal is to map Algorithms to their respective implementation 
(python packages listed in [python package index](https://pypi.org/). 
It performs a duckduckGo search request, filters with the chatGPT API and saves the results in a text file. 

## ChatGPT Filter 

This tool automatically filters out duckduckGo search results with a chatGPT API request:

**_Example Prompt:_**  
Tell me if the following description of a python package
    describes a package which implements the explainable AI algorithm LIME
    answer binary either "yes" or "no". Description: \
    Local Interpretable Model-Agnostic Explanations for machine learning classifiers ... 



## Run tool 

Run the following command in order to get the results in a text file. 

```shell
Python3 Scraping.py 
```


---
**NOTE**

The tool will ask you to enter a search word. The search for packages is then being made using duckduckgo and the following query:  

**site:pypi.org {your word} explanation**

After entering your word you are asked if you want to filter the first 20 results. If yes you need to paste your openAI API key. 
This will then ask chatGPT's API (model gpt-3.5-turbo) whether the description really is connected to the wished topic.

---


The results are then being saved in a text file of the form {your word} results {date}.





## Dependencies
- [Requests 2.31.0](https://pypi.org/project/requests/#description) 
- [beautifulsoup4 4.12.3](https://pypi.org/project/beautifulsoup4/) 
