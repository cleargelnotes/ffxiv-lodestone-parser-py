import requests
import json
import base64
from bs4 import BeautifulSoup

url_info = "https://na.finalfantasyxiv.com/lodestone/freecompany/{}"
url_members = "https://na.finalfantasyxiv.com/lodestone/freecompany/{}/member/"

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
        # TODO
        return []
        
    def parse_members(self, soups):
        # TODO
        pass
