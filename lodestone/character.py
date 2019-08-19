import requests
from bs4 import BeautifulSoup

char_id = "9197144"

url = "https://na.finalfantasyxiv.com/lodestone/character/{}"

JOBS = [
    "PLD", "WAR", "DRK", "GNB",
    "WHM", "SCH", "AST",
    "BRD", "MCH", "DNC",
    "MNK", "DRG", "NIN", "SAM",
    "BLM", "SMN", "RDM", "BLU",
    "CRP", "BSM", "ARM", "GSM", "WVR", "LTW", "ALC", "CUL",
    "BTN", "MIN", "FSH"
]

class Job(object):
    def __init__(self, name, level="", current_exp=0, max_exp=0):
        self.name = name
        self.level = level
        self.current_exp = current_exp
        self.max_exp = max_exp
        
    def __str__(self):
        return "{} Lv.{} {}/{}".format(self.name, self.level, self.current_exp, self.max_exp)
        
    def __unicode__(self):
        return "{} Lv.{} {}/{}".format(self.name, self.level, self.current_exp, self.max_exp)
        
    def update_info(self, data):
        self.level = data.get("level")
        self.current_exp = data.get("current_exp")
        self.max_exp = data.get("max_exp")


class Profile(object):
    def __init__(self):
        self.char_name = "NONAME"
        self.char_url = ""
        self.char_title = ""
        self.jobs = {
            "PLD": Job("Paladin"),
            "WAR": Job("Warrior"),
            "DRK": Job("Dark Knight"),
            "GNB": Job("Gunbreaker"),
            
            "WHM": Job("White Mage"),
            "SCH": Job("Scholar"),
            "AST": Job("Astrologian"),
            
            "MNK": Job("Monk"),
            "DRG": Job("Dragoon"),
            "NIN": Job("Ninja"),
            "SAM": Job("Samurai"),
            
            "BRD": Job("Bard"),
            "MCH": Job("Machinist"),
            "DNC": Job("Dancer"),
            
            "BLM": Job("Black Mage"),
            "SMN": Job("Summoner"),
            "RDM": Job("Red Mage"),
            "BLU": Job("Blue Mage"),
            
            "CRP": Job("Carpenter"),
            "BSM": Job("Blacksmith"),
            "ARM": Job("Armorer"),
            "GSM": Job("Goldsmith"),
            "LTW": Job("Leatherworker"),
            "ALC": Job("Alchemist"),
            "WVR": Job("Weaver"),
            "CUL": Job("Culinarian"),
            
            "BTN": Job("Botanist"),
            "MIN": Job("Miner"),
            "FSH": Job("Fisher"),
        }
        
    def set_job_info(self, job_info):
        job_name = job_info.get("name")
        for job in self.jobs.keys():
            if self.jobs[job].name == job_name:
                self.jobs[job].update_info(job_info)
                break
                
    def print_report(self):
        print("Character: {} ({})".format(self.char_name, self.char_title))
        print("---------------------------------")
        for job in JOBS:
            print(self.jobs.get(job))
                
                
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
    job_level = job.next
    job_name = job.next_sibling.next
    job_exp = job.next_sibling.next_sibling.next
    current_exp, max_exp = parse_exp(job_exp)
    
    return {
        "level": job_level,
        "name": job_name,
        "current_exp": current_exp,
        "max_exp": max_exp
    }
    

def parse_profile(soup):
    p = Profile()
    chara_link = soup.find_all("a", {"class": "frame__chara__link"})[0]
    p.char_url = chara_link.attrs.get("href")
    p.char_name = chara_link.find_all("p", {"class": "frame__chara__name"})[0].next
    p.char_title = chara_link.find_all("p", {"class": "frame__chara__title"})[0].next
    job_groups = soup.find_all("ul", {"class": "character__job"})
    for job_group in job_groups:
        jobs = job_group.find_all("div", {"class": "character__job__level"})
        for job in jobs:
            parsed_job = parse_job(job)
            p.set_job_info(parsed_job)
            
    return p


def retrieve_page(cid):
    resp_data = requests.get(url.format(cid))
    soup = BeautifulSoup(resp_data.text, "html.parser")
    return soup
    
    
def retrieve_profile(cid):
    soup = retrieve_page(cid)
    return parse_profile(soup)
    
