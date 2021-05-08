import bs4
import requests
from bs4 import BeautifulSoup
import pandas as pd
# from selenium import webdriver
# browser = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

# &page=2


def getCurrentPageCards(currentPageURL):
    def getCardData(cardLink):
        response = requests.get(cardLink, headers=headers)
        data = response.content.decode()
        soup = BeautifulSoup(data, 'html.parser')

        newname = soup.find('h1', {'class': 'headline'}).text
        location = soup.find('p', {'class': 'mb-0'}).text
        newage = soup.find('div', {'id': 'person-details-age'}).text
        phone_no = soup.find('a', {'class': 'v-card--flat'}).text
        current_addr = soup.find('a', {'class': 'raven--text'}).text

        return (newname, location, newage, phone_no, current_addr)

    result = requests.get(currentPageURL, headers=headers)
    data = result.content.decode()
    soup = BeautifulSoup(data, 'html.parser')
    divs = soup.find_all('div', {'class': 'pb-2'})

    cards = []
    # currentPageCards = {}
    for div in divs:
        link = div.find('a', {'class': 'card-link'})
        if link:
            print("Gotccha! New Card found")
            cardLink = "https://www.411.com" + link.get('href')
            cards.append(getCardData(cardLink))
    return cards


def getTotalPageCount(baseURL):
    response = requests.get(baseURL, headers=headers)
    data = response.content.decode()
    soup = BeautifulSoup(data, 'html.parser')
    pageCount = 0
    for item in soup.find_all():
        if "data-v-19ddcf8a" in item.attrs:
            pageCount += 1
    return pageCount


if(__name__ == "__main__"):
    query = 'novel'
    location = ''
    baseURL = "https://www.411.com/name/{}?fs=1&searchedName={}&searchedLocation={}".format(
        query.title(), query, location)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    totalPages = getTotalPageCount(baseURL)
    totalCards = []
    # get base card URL
    cards = getCurrentPageCards(baseURL)
    totalCards.extend(cards)
    for pageNumber in range(2, totalPages + 1):
        restPagesURL = baseURL + "&page={}".format(pageNumber)
        cards = getCurrentPageCards(restPagesURL)
        totalCards.extend(cards)

    print(totalCards[0])
    df = pd.DataFrame(totalCards, columns=[
                      "Name", "Location", "Age", "Phone_no", "Current_addr"])
    # df.to_excel("test.xlsx")
    df.to_csv("411.csv")

    # outputDF = pd.DataFrame.from_dict(currentPageCards, orient='index', columns=[
    #     'Name', 'Location', 'Age', 'Phone Number', 'Current Address'])
    # return outputDF
    # # outputDF.to_csv('411.csv')
