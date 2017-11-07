import requests
from bs4 import BeautifulSoup
import re


def get_html(url):
   _html = ""
   resp = requests.get(url)
   if resp.status_code == 200:
      _html = resp.text
   return _html


def get_diet(num):
    factor = num
    factor = int(factor)

    URL = "http://www.inhun.hs.kr/76967/dggb/module/mlsv/selectMlsvDetailPopup.do?mlsvId=%d" % (factor)
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find_all("td")
    element = str(element)

    element = element.replace('<td class="ta_l">',' ')
    element = element.replace('</td>', ' ')
    element = element.replace('[', ' ')
    element = element.replace(']', ' ')
    element = element.replace('&amp;', ' ')
    element = element.replace('0 kcal', ' ')

    element = element.replace('중식', ' ', 1)
    element = element.replace('석식', ' ', 1)
    element = element.replace(',', ' ', 1)
    element = element.replace(" ", "")

    element = ''.join(element.split())
    element = element.replace(',', ', ')

    return element
