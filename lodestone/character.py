import requests
import json
import base64
from bs4 import BeautifulSoup

from .jobs import JOBS_SHORT, JobDBCacheSingleton, JobInfo


char_id = "9197144"

url = "https://na.finalfantasyxiv.com/lodestone/character/{}"


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
    job_name = job.next_sibling.next
    job_exp = job.next_sibling.next_sibling.next
    current_exp, max_exp = parse_exp(job_exp)
    
    return {
        "level": job_level,
        "job": JobDBCacheSingleton.get_job_by_name(job_name),
        "current_exp": current_exp,
        "max_exp": max_exp
    }
    

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
        
    def retrieve_data(self):
        soup = self.retrieve_page()
        
        self.parse_char_data(soup)
        self.parse_job_data(soup)
        
        self.data_retrieved = True
        
    def parse_char_data(self, soup):
        chara_link = soup.find_all("a", {"class": "frame__chara__link"})[0]
        self.char_url = chara_link.attrs.get("href")
        self.char_name = chara_link.find_all("p", {"class": "frame__chara__name"})[0].next
        self.char_title = chara_link.find_all("p", {"class": "frame__chara__title"})[0].next
        srv_data = chara_link.find_all("p", {"class": "frame__chara__world"})[0].next.next
        split = srv_data.split("\xa0(")
        self.server = split[0]
        self.datacenter = split[1][:-1]
        
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
        
    def set_job_info(self, job_info):
        job_data = job_info.get("job")
        if job_data:
            self.jobs[job_data.name_short].update_info(job_info)
                
    def print_report(self):
        if not self.data_retrieved:
            self.retrieve_data()
            
        print("Character: {} ({}) [{} - {}]".format(self.char_name, self.char_title, self.server, self.datacenter))
        print("{} ({}) {}".format(self.char_race, self.char_clan, self.char_gender))
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
        return {
            "char": char_dict,
            "jobs": jobs_dict
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
        
    
