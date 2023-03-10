import requests
from bs4 import BeautifulSoup
import csv
import sys
import time

proxies = {
        'http': '173.208.239.10:15007'
        }

site_maps = []

# GETTIN SITE MAP TREE
site_map_url = "https://www.owg.pl/sitemap.xml"
site_map_tree = requests.get(site_map_url, proxies=proxies)
site_map_tree_soup = BeautifulSoup(site_map_tree.content, features="xml").find('sitemapindex').find_all('sitemap')
for sm in site_map_tree_soup:
    site_maps.append(sm.find('loc').text)


# LOOPING THROUGH EACH SITE MAP TO GET PAGES
pages_to_scrap = []
current_prog = 0
for ssm in site_maps:
    ssite_map_tree = requests.get(ssm, proxies=proxies)
    ssite_map_tree_soup = BeautifulSoup(ssite_map_tree.content, features="xml").find('urlset').find_all('url')
    for link_block in ssite_map_tree_soup:
        link = link_block.find('loc').text
        if link[19:25] == "krs-rp" or link[19:21] == "sc":
            pages_to_scrap.append(link_block.find('loc').text)
    sys.stdout.write("\r{0}>".format("="*round(current_prog/len(site_maps)*10)))
    sys.stdout.write("\033[94m GETTING ALL PAGES LINKS: \033[0m")
    sys.stdout.write(str(round(current_prog/len(site_maps)*100))+"%")
    sys.stdout.flush()
    # sleep to prevent getting blocked!
    time.sleep(0.5)
    current_prog+=1

# SAVING BACKUP
#f = open("backup.txt", "w")
#for l in pages_to_scrap:
#    f.write(l+"\n")
#f.close()


# LOOPING THROUGH EACH LINK AND RETREIVING DATA
for link in pages_to_scrap:
    r = requests.get(link, proxies=proxies)
    soup = BeautifulSoup(r.content, "html.parser")
print("done")
