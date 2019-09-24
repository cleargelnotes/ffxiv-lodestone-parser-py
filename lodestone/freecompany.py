import requests
import json
import base64
from bs4 import BeautifulSoup

url_info = "https://na.finalfantasyxiv.com/lodestone/freecompany/{}"
url_members = "https://na.finalfantasyxiv.com/lodestone/freecompany/{}/member/"

fc_id = "9233505136016441986"

class FreeCompany(object):
    def __init__(self, fc_id, retrieve_data=False):
        self.fc_id = fc_id
        self.data_retrieved = False
        if retrieve_data:
            self.retrieve_data()
            
    def retrieve_data(self):
        soups = self.retrieve_pages()
        self.parse_members(soups.get("members"))
        self.data_retrieved = True
        
    def retrieve_pages(self):
        resp_data = requests.get(url_info.format(self.fc_id))
        soup_info = BeautifulSoup(resp_data.text, "html.parser")
        
        member_soups = self.retrieve_member_soups()
        
        return {
            "info": soup_info,
            "members": member_soups
        }
        
    def retrieve_member_soups(self):
        soup_0 = BeautifulSoup(requests.get(url_members.format(self.fc_id)).text, "html.parser")
        ret = [soup_0]
        # get total number of pages
        li_pager = soup_0.find_all("li", {"class": "btn__pager__current"})[0]
        pagestr = li_pager.next
        totalpages = int(pagestr.split(" of ")[1])
        for i in range(1, totalpages):
            ret.append(BeautifulSoup(requests.get("{}?page={}".format(url_members.format(self.fc_id), i+1)).text, "html.parser"))
        
        return ret
        
    def parse_members(self, soups):
        self.members = []
        for soup in soups:
            soup_uls = soup.find("div", {"class": "ldst__contents"}).find("div", {"class": "ldst__window"}).findChildren("ul")
            for ul in soup_uls:
                lis = ul.find_all("li", {"class": "entry"})
                for entry in lis:
                    char_id = entry.find("a", {"class": "entry__bg"}).attrs.get("href")[:-1].split("/")[-1]
                    divdata = entry.find("div", {"class": "entry__freecompany__center"})
                    if divdata:
                        name = divdata.find("p", {"class": "entry__name"}).next
                        rank_lis = divdata.find("ul", {"class": "entry__freecompany__info"}).find_all("li")
                        rank = rank_lis[0].find("span").next
                        if name and rank:
                            self.members.append({
                                "name": name,
                                "rank": rank,
                                "char_id": char_id
                            })
