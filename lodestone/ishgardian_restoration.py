import requests
import json
import base64
import re
from bs4 import BeautifulSoup

url = "https://na.finalfantasyxiv.com/lodestone/ishgardian_restoration/builders_progress_report"

def parse():
    resp_data = requests.get(url)
    soup = BeautifulSoup(resp_data.text, "html.parser")
    world_lists = soup.find_all("ul", {"class": "report-world_list"})
    ret = {}
    for world_list in world_lists:
        lis = world_list.find_all("li")
        for li in lis:
            world_name = str(li.find("span", {"class": "world_name"}).next)
            try:
                progress = li.find("div", {"class": "bar"}).find("span").attrs.get("style").split(" ")[1]
                progress_float = float(progress[:-1])
            except:
                progress = "100%"
                progress_float = 100.0
            level = str(li.find("div", {"class": "status"}).find("p").next)
            #print(world_name + ": [" + level + "] " +progress)
            ret[world_name] = {
                "level": level,
                "progress": progress_float
            }
    return ret
