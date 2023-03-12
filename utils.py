import requests
from bs4 import BeautifulSoup
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}
proxies = ['69.30.240.226:15005','69.30.197.122:15005','173.208.239.10:15005','173.208.136.2:15005','69.30.240.226:15006','69.30.197.122:15006','173.208.239.10:15006','173.208.136.2:15006','69.30.240.226:15007','69.30.197.122:15007','173.208.239.10:15007','173.208.136.2:15007','69.30.240.226:15008','69.30.197.122:15008','173.208.239.10:15008','173.208.136.2:15008','195.154.255.118:15005','195.154.222.228:15005','195.154.255.34:15005','195.154.222.26:15005','195.154.255.118:15006','195.154.222.228:15006','195.154.255.34:15006','195.154.222.26:15006','195.154.255.118:15007','195.154.222.228:15007','195.154.255.34:15007','195.154.222.26:15007','195.154.255.118:15008','195.154.222.228:15008','195.154.255.34:15008','195.154.222.26:15008']

def getData(page):
    next = 0
    time.sleep(1)    
    data = {}
    r = None
    try:
        r = requests.get(page, proxies={"http":proxies[next]}, headers=headers)
    except:
        next = (next + 1) % len(proxies)
        print("\nChanging Proxy")
        getData(page)
    
    soup = BeautifulSoup(r.content, "html.parser")
    element = soup.body.find("div", attrs={"class":"editData"}).find("div", attrs={"class":"winfieldContainer level3 editHeadMoreWrap"}).find("h1")
    url_element = soup.body.find("div", attrs={"class":"editData"}).find("div", attrs={"class":"winfieldContainer level2 contentTableKontakt"}).find("div", attrs={"class":"winfieldContainer level3 wwwKontakt"})

    data['company_name'] = "-" if element is None else element.find("span", attrs={"class":"edyFrimaNazwa"}).text
    data['company_nip'] = "-"
    data['company_regon'] = "-"
    data['company_link'] = "-" if url_element.a is None else url_element.a.text

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