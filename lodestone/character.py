import requests
import json
import base64
import re
from bs4 import BeautifulSoup
from enum import Enum, auto

from .jobs import JOBS_SHORT, JobDBCacheSingleton, JobInfo
from .freecompany import FC_CACHE


char_id = "9197144"

url = "https://na.finalfantasyxiv.com/lodestone/character/{}"
job_url = "https://na.finalfantasyxiv.com/lodestone/character/{}/class_job"


def parse_formatted_int(num):
    if num == "--":
        return 0
    try:
        val = int(num.replace(",", ""))
        return val
    except:
        return 0


def parse_exp(exp):
    split = exp.split(" / ")
    return parse_formatted_int(split[0]), parse_formatted_int(split[1])


def parse_job(job):
    job_level = parse_formatted_int(job.next)
    job_name_div = job.find_next("div")
    job_name = job_name_div.next
    job_exp_div = job_name_div.find_next("div")
    job_exp = job_exp_div.next
    current_exp, max_exp = parse_exp(job_exp)
    
    return {
        "level": job_level,
        "job": JobDBCacheSingleton.get_job_by_name(job_name),
        "current_exp": current_exp,
        "max_exp": max_exp
    }
    

class EquipmentSlots(Enum):
    WEAPON = auto()
    OFFHAND = auto()
    HEAD = auto()
    BODY = auto()
    HANDS = auto()
    BELT = auto()
    LEGS = auto()
    FEET = auto()
    EARRINGS = auto()
    NECKLACE = auto()
    BRACELETS = auto()
    RING = auto()
    CRYSTAL = auto()
    #@staticmethod
    #def parse_slot(slot):
    #    if slot.endswith(" Arm") or slot.endswith(" Primary Tool"):
    #        return EquipmentSlots.WEAPON
    #    if slot == "Shield" or slot.endswith(" Secondary Tool"):
    #        return EquipmentSlots.OFFHAND
    #    if slot == "
    

class Profile(object):
    def __init__(self, char_id, retrieve_data=False):
        self.char_id = char_id
        self.char_name = "NONAME"
        self.char_url = ""
        self.char_title = ""
        self.server = ""
        self.datacenter = ""
        self.jobs = {}
        self.data_retrieved = False
        for job in JOBS_SHORT:
            self.jobs[job] = JobInfo(JobDBCacheSingleton.get_job_by_short(job))
            
        if retrieve_data:
            self.retrieve_data()
        
    def retrieve_page(self):
        resp_data = requests.get(url.format(self.char_id))
        soup = BeautifulSoup(resp_data.text, "html.parser")
        return soup
        
    def retrieve_job_page(self):
        resp_data = requests.get(job_url.format(self.char_id))
        soup = BeautifulSoup(resp_data.text, "html.parser")
        return soup
        
    def retrieve_data(self):
        soup = self.retrieve_page()
        job_soup = self.retrieve_job_page()
        
        self.parse_char_data(soup)
        self.parse_job_data(job_soup)
        self.parse_gearset_data(soup)
        self.parse_attribute_data(soup)
        
        self.data_retrieved = True
        
    def parse_char_data(self, soup):
        chara_link = soup.find_all("a", {"class": "frame__chara__link"})[0]
        self.char_url = chara_link.attrs.get("href")
        self.char_name = chara_link.find_all("p", {"class": "frame__chara__name"})[0].next
        try:
            self.char_title = chara_link.find_all("p", {"class": "frame__chara__title"})[0].next
        except:
            self.char_title = ""
        srv_data = chara_link.find_all("p", {"class": "frame__chara__world"})[0].next.next
        split = srv_data.split("\xa0(")
        self.server = split[0]
        self.datacenter = split[1][:-1]
        
        try:
            block_fc = soup.find("div", {"class": "character__freecompany__name"})
            fc_h4 = block_fc.find("h4")
            fc_h4_a = fc_h4.find("a")
            fc_name = fc_h4_a.next
            fc_id = fc_h4_a.attrs.get("href")[:-1].split("/")[-1]
            self.fc = {
                "name": fc_name,
                "id": fc_id
            }
            self.supplement_fc_data()
        except:
            import traceback
            traceback.print_exc()
            self.fc = {}
        
        profile_data_div = soup.find_all("div", {"class": "character__profile__data"})[0]
        char_blocks = profile_data_div.find_all("div", {"class": "character-block"})
        block_race_clan_gender = char_blocks[0]
        race_clan_gender = block_race_clan_gender.find_all("p", {"class": "character-block__name"})[0].contents
        profile_pic = block_race_clan_gender.find_all("img", {"class": "character-block__face"})[0]
        self.profile_pic = base64.b64encode(requests.get(profile_pic.attrs.get("src")).content)
        
        full_body_image_div = soup.find_all("div", {"class": "character__detail__image"})[0]
        full_body_image = full_body_image_div.find_all("img")[0]
        self.full_body_pic = base64.b64encode(requests.get(full_body_image.attrs.get("src")).content)
        
        race = race_clan_gender[0]
        clan_gender = race_clan_gender[2].split("/")
        clan = clan_gender[0].strip()
        gender = clan_gender[1].strip()
        self.char_race = race
        self.char_clan = clan
        self.char_gender = gender
        
    def parse_job_data(self, soup):
        jobs = soup.find_all("div", {"class": "character__job__level"})
        for job in jobs:
            parsed_job = parse_job(job)
            self.set_job_info(parsed_job)
            
    def parse_gearset_data(self, soup):
        profile_page = soup.find("div", {"class": "character__content"})
        equips = profile_page.find_all("div", {"class": re.compile("icon-c--\d\d?")})
        self.equipment = []
        for equip in equips:
            tooltip_div = equip.find("div", {"class": "db-tooltip"})
            if not tooltip_div:
                continue
            
            iid_div = tooltip_div.find("div", {"class": "db-tooltip__bt_item_detail"})
            iid_a = iid_div.find("a")
            iid = iid_a.attrs.get("href").split("/")[-2]
            
            iname_h2 = tooltip_div.find("h2", {"class": "db-tooltip__item__name"})
            iname = iname_h2.next
            
            ilvl_div = tooltip_div.find("div", {"class": "db-tooltip__item__level"})
            try:
                ilvl = int(ilvl_div.next.rsplit(" ", 1)[1])
            except:
                ilvl = 0
                
            islot_p = tooltip_div.find("p", {"class": "db-tooltip__item__category"})
            islot_raw = islot_p.next
            
            item_data = {
                "id": iid,
                "name": iname,
                "ilvl": ilvl,
                "category": islot_raw
            }
            
            # check if there is glamour
            glamour_div = tooltip_div.find("div", {"class": "db-tooltip__item__mirage"})
            if glamour_div:
                igname_p = glamour_div.find("p")
                igname = igname_p.next
                igid_a = igname.next
                igid = igid_a.attrs.get("href").split("/")[-2]
                item_data.update({
                    "glamour": {
                        "id": igid,
                        "name": igname
                    }
                })
            
            # check if there is dye
            dye_div = tooltip_div.find("div", {"class": "stain"})
            if dye_div:
                dye_a = dye_div.find("a")
                dyeid = dye_a.attrs.get("href").split("/")[-2]
                dyename = dye_a.next
                item_data.update({
                    "dye": {
                        "id": dyeid,
                        "name": dyename
                    }
                })
                
            # check if there are materias
            ul_div = tooltip_div.find("ul", {"class": "db-tooltip__materia"})            
            if ul_div:
                materias = []
                for materia_div in ul_div.find_all("div", {"class": "db-tooltip__materia__txt"}):
                    materias.append({
                        "name": materia_div.next
                    })
                if materias:
                    item_data.update({
                        "materias": materias
                    })
            
            self.equipment.append(item_data)
            
            
    def parse_attribute_data(self, soup):
        attribute_page = soup.find_all("div", {"class": "character__content"})[0]
        self.attributes = {}
        profile_data_div = attribute_page.find("div", {"class": "character__profile__data"})
        h3_list = profile_data_div.find_all("h3", {"class": "heading--lead"})
        for h3 in h3_list:
            attr_table = h3.nextSibling
            tr_list = attr_table.find_all("tr")
            for tr in tr_list:
                th = tr.find("th")
                td = tr.find("td")
                span = th.find("span")
                attr_name = span.next
                attr = {
                    "tooltip": span.attrs.get("data-tooltip"),
                    "value": parse_formatted_int(td.next)
                }
                self.attributes[attr_name] = attr
                
        hp_p = attribute_page.find("p", {"class": "character__param__text__hp--en-us"})
        try:
            hp_val = parse_formatted_int(hp_p.nextSibling.next)
        except:
            hp_val = 0
        mp_p = attribute_page.find("p", {"class": "character__param__text__mp--en-us"})
        try:
            mp_val = parse_formatted_int(mp_p.nextSibling.next)
        except:
            mp_val = 0
        cp_p = attribute_page.find("p", {"class": "character__param__text__cp--en-us"})
        try:
            cp_val = parse_formatted_int(cp_p.nextSibling.next)
        except:
            cp_val = 0
        gp_p = attribute_page.find("p", {"class": "character__param__text__gp--en-us"})
        try:
            gp_val = parse_formatted_int(gp_p.nextSibling.next)
        except:
            gp_val = 0
        self.attributes.update({
            "HP": {"value": hp_val},
            "MP": {"value": mp_val},
            "CP": {"value": cp_val},
            "GP": {"value": gp_val},
        })
        
        
    def set_job_info(self, job_info):
        job_data = job_info.get("job")
        if job_data:
            self.jobs[job_data.name_short].update_info(job_info)
            
    def supplement_fc_data(self):
        fc = FC_CACHE.get(self.fc.get("id"))
        member_rank = fc.get_member_rank(self.char_id)
        self.fc.update({
            "rank": member_rank,
            "tag": fc.tag
        })
        
    def print_report(self):
        if not self.data_retrieved:
            self.retrieve_data()
            
        print("Character: {} ({}) [{} - {}]".format(self.char_name, self.char_title, self.server, self.datacenter))
        print("{} ({}) {}".format(self.char_race, self.char_clan, self.char_gender))
        print("FC {} {} ({}) - {}".format(self.fc.get("name"), self.fc.get("tag"), self.fc.get("id"), self.fc.get("rank")))
        print("---------------------------------")
        for job in JOBS_SHORT:
            print(self.jobs.get(job))
            
    def to_json(self):
        return json.dumps(self.to_json_dict())
            
    def to_json_dict(self):
        if not self.data_retrieved:
            self.retrieve_data()
            
        char_dict = self.get_char_json_data()
        jobs_dict = self.get_jobs_json_data()
        fc_dict = self.get_fc_json_data()
        equipment_dict = self.get_equipment_json_data()
        attribute_dict = self.get_attribute_json_data()
        return {
            "char": char_dict,
            "jobs": jobs_dict,
            "fc": fc_dict,
            "equipment": equipment_dict,
            "attributes": attribute_dict
        }
        
    def get_char_json_data(self):
        return {
            "name": self.char_name,
            "title": self.char_title,
            "server": self.server,
            "datacenter": self.datacenter,
            "url": self.char_url,
            "race": self.char_race,
            "clan": self.char_clan,
            "gender": self.char_gender,
            "profile_picture": self.profile_pic.decode("utf-8"),
            "full_body_picture": self.full_body_pic.decode("utf-8")
        }
        
    def get_jobs_json_data(self):
        ret = {}
        for job in JOBS_SHORT:
            job_info = self.jobs[job]
            ret[job] = job_info.to_json_dict()
        return ret
        
    def get_fc_json_data(self):
        return self.fc
        
    def get_equipment_json_data(self):
        return self.equipment
        
    def get_attribute_json_data(self):
        ret = {}
        for k in self.attributes.keys():
            ret[k] = self.attributes[k].get("value")
        return ret
        
    
