import requests
from bs4 import BeautifulSoup

proxies = {
        'http': '173.208.239.10:15007'
        }

def getData(page):
    data = {}
    r = requests.get(page, proxies=proxies)
    soup = BeautifulSoup(r.content, "html.parser")
    element = soup.body.find("div", attrs={"class":"editData"}).find("div", attrs={"class":"winfieldContainer level3 editHeadMoreWrap"}).find("h1")

    data['company_name'] = "-" if element is None else element.text
    data['company_nip'] = None
    data['company_regon'] = None

    company_nip_regon = soup.body.find("div", attrs={"class":"winfieldContainer level3 editHeadMoreWrap"}).find_all("div", attrs={"class":"winfieldContainer level5"})
    for d in company_nip_regon:
        element = d.find("div", attrs={"class":"winFieldTextLabel level5"})
        if element != None:
            if element.text == "NIP:":
                tag = element.parent.find("div", attrs={"class":"winFieldTextData level5"})
                data['company_nip'] = "-" if tag is None else tag.text
            if element.text == "REGON:":
                tag = element.parent.find("div", attrs={"class":"winFieldTextData level5"})
                data['company_regon'] = "-" if tag is None else tag.text
    return data
