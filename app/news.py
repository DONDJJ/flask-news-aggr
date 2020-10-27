import requests
import bs4
import json
import _thread
from app.que import que

YANDEX_URL = 'https://yandex.ru/'
MEDUZA_URL = 'https://meduza.io/api/v3/search?chrono=news&locale=ru&page=0&per_page=10'
RIA_URL ='https://ria.ru/'
LENTA_URL = 'https://lenta.ru/rss/last24'
SPORT_EXPRESS='https://www.sport-express.ru/'

def get_content_from_url(url):
    RESPONSE = requests.get(url)
    return bs4.BeautifulSoup(RESPONSE.content, features='html.parser')

def yandex_news_check():
    BsObj = get_content_from_url(YANDEX_URL)
    # YANDEX_RESPONSE = requests.get(YANDEX_URL)
    #
    # BsObj = bs4.BeautifulSoup(YANDEX_RESPONSE.content, features='html.parser')

    news1 = BsObj.select('.news__item-content ')
    news2 = BsObj.findAll('a')

    text_list = []
    for i in news1:
        text_list.append(i.getText())

    href_list = []
    for i in news2:
        if 'news/story' in i['href']:
            href_list.append(i['href'])

    return text_list, href_list


def meduza_check():
    MEDUZA_RESPONSE = requests.get(MEDUZA_URL)

    all_content = json.loads(MEDUZA_RESPONSE.text)

    news_list = []

    for i in [j for j in all_content['documents'].keys() if str(j).startswith('news')]:
        news_list.append(i)

    news_text_list = []
    href_list = []
    for i in news_list:
        news_text_list.append(all_content['documents'][i]['title'])
        href_list.append("https://meduza.io/" + all_content['documents'][i]['url'])

    return news_text_list, href_list

def ria_check():
    BsObj = get_content_from_url(RIA_URL)
    news = BsObj.findAll('a', {'class':'cell-list__item-link color-font-hover-only'})
    text_list = []
    href_list = []

    for i in news:
        text_list.append(i.getText())
        href_list.append(i['href'])

    return text_list, href_list

def lenta_check():
    RESPONSE = requests.get(LENTA_URL)
    BsObj = bs4.BeautifulSoup(RESPONSE.content)
    text_list = [i.getText() for i in BsObj.findAll('title') if not i.getText().startswith('Lenta')]
    href_list = [i.getText() for i in BsObj.findAll('guid')]

    return text_list, href_list

def SE_common(sport):
    BsObj = get_content_from_url(SPORT_EXPRESS + sport + '/news/')
    news = BsObj.findAll('a', {'class': 'se19-news-item__link'})

    text_list = []
    href_list = []

    for i in news:
        text_list.append(i.getText())
        href_list.append(i['href'])

    return text_list, href_list

def sport_express_check_football():
    return SE_common('football')
def sport_express_check_hockey():
    return SE_common('hockey')
def sport_express_check_autosport():
    return SE_common('autosport')


if __name__ == '__main__':
    pass


# РИА
