import requests
from bs4 import BeautifulSoup
import csv
import sys
import time
import utils
from itertools import cycle

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

proxies = ['69.30.240.226:15005','69.30.197.122:15005','173.208.239.10:15005','173.208.136.2:15005','69.30.240.226:15006','69.30.197.122:15006','173.208.239.10:15006','173.208.136.2:15006','69.30.240.226:15007','69.30.197.122:15007','173.208.239.10:15007','173.208.136.2:15007','69.30.240.226:15008','69.30.197.122:15008','173.208.239.10:15008','173.208.136.2:15008','195.154.255.118:15005','195.154.222.228:15005','195.154.255.34:15005','195.154.222.26:15005','195.154.255.118:15006','195.154.222.228:15006','195.154.255.34:15006','195.154.222.26:15006','195.154.255.118:15007','195.154.222.228:15007','195.154.255.34:15007','195.154.222.26:15007','195.154.255.118:15008','195.154.222.228:15008','195.154.255.34:15008','195.154.222.26:15008']
next = 0

site_maps = []

# GETTIN SITE MAP TREE
site_map_url = "https://www.owg.pl/sitemap.xml"
try:
    site_map_tree = requests.get(site_map_url, proxies={"http":proxies[next]}, headers=headers)
except:
    next = (next + 1) % len(proxies)
    site_map_tree = requests.get(site_map_url, proxies={"http":proxies[next]}, headers=headers)

site_map_tree_soup = BeautifulSoup(site_map_tree.content, features="xml").find('sitemapindex').find_all('sitemap')
for sm in site_map_tree_soup:
    site_maps.append(sm.find('loc').text)


# LOOPING THROUGH EACH SITE MAP TO GET PAGES
pages_to_scrap = []
current_prog = 0
next = 0
for ssm in site_maps:
    ssite_map_tree = None
    try:
        ssite_map_tree = requests.get(ssm, proxies={"http":proxies[next]}, headers=headers)
    except:
        next = (next + 1) % len(proxies)
        print("\nChanging Proxy\n")
        ssite_map_tree = requests.get(ssm, proxies={"http":proxies[next]}, headers=headers)
        time.sleep(5)
        print("Sleeping zz...")
        continue

    ssite_map_tree_soup = BeautifulSoup(ssite_map_tree.content, features="xml").find('urlset').find_all('url')
    for link_block in ssite_map_tree_soup:
        link = link_block.find('loc').text
        keyword = None
        if link[19:25] == "krs-rp":
            keyword = "/krs-rp/"
        elif link[19:21] == "sc":
            keyword = "/sc/"
        elif link[19:24] == "ceidg":
            keyword = "/ceidg/"
        else:
            break
        link = link.replace(keyword, "/obf-kontakty/")
        pages_to_scrap.append(link)

    sys.stdout.write("\r{0}>".format("="*round(current_prog/len(site_maps)*10)))
    sys.stdout.write("\033[94m GETTING ALL PAGES LINKS: \033[0m")
    sys.stdout.write(str(round(current_prog/len(site_maps)*100))+"%")
    sys.stdout.flush()

    # sleep to prevent getting blocked!
    time.sleep(0.1)
    current_prog+=1
#    if current_prog == 3:
#       break

# SAVING BACKUP
#f = open("backup.txt", "w")
#for l in pages_to_scrap:
#    f.write(l+"\n")
#f.close()

# LOOPING THROUGH EACH LINK AND RETREIVING DATA
filename = "results.csv"
current_prog = 0
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['company_name', 'company_nip', 'company_regon', 'company_link'])
    w.writeheader()
    for page in pages_to_scrap:
        info = None
        try:
            info = utils.getData(page)
        except:
            print("Exception at: "+page+"\nSleeping 10")
            time.sleep(10)
            continue
        if info['company_name'] == '-' or info['company_nip'] == '-' or info['company_regon'] == '-' or info['company_link'] == '-':
            continue
        w.writerow(info)
        if current_prog == 0:
            print("\n FOUND "+str(len(pages_to_scrap))+" LINK\n")
        sys.stdout.write("\r{0}>".format("="*round(current_prog/len(pages_to_scrap)*10)))
        sys.stdout.write("\033[92m RETREIVING DATA FROM PAGES LINKS: \033[0m")
        sys.stdout.write("   "+str(current_prog)+"/"+str(len(pages_to_scrap)))
        sys.stdout.flush()
        # sleep to prevent getting blocked!
        time.sleep(0.1)
        current_prog+=1
#        if current_prog == 60:
#            break

print("\033[90m ALL GOOD !! \033[0m")
