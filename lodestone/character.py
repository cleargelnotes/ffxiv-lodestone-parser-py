from enum import Enum, auto
from collections import namedtuple

import requests
from bs4 import BeautifulSoup


char_id = "9197144"

url = "https://na.finalfantasyxiv.com/lodestone/character/{}"

JOBS_SHORT = [
    "PLD", "WAR", "DRK", "GNB",
    "WHM", "SCH", "AST",
    "BRD", "MCH", "DNC",
    "MNK", "DRG", "NIN", "SAM",
    "BLM", "SMN", "RDM", "BLU",
    "CRP", "BSM", "ARM", "GSM", "WVR", "LTW", "ALC", "CUL",
    "BTN", "MIN", "FSH",
    
    "EUREKA"
]

class Jobs(Enum):
    PLD = auto()
    WAR = auto()
    DRK = auto()
    GNB = auto()
    
    WHM = auto()
    SCH = auto()
    AST = auto()
    
    BRD = auto()
    MCH = auto()
    DNC = auto()
    
    MNK = auto()
    DRG = auto()
    NIN = auto()
    SAM = auto()
    
    BLM = auto()
    SMN = auto()
    RDM = auto()
    BLU = auto()
    
    CRP = auto()
    BSM = auto()
    ARM = auto()
    GSM = auto()
    WVR = auto()
    LTW = auto()
    ALC = auto()
    CUL = auto()
    
    BTN = auto()
    MIN = auto()
    FSH = auto()
    
    EUREKA = auto()
    
class JobDiscipline(Enum):
    DOW = auto()
    DOM = auto()
    DOH = auto()
    DOL = auto()
    OTHER = auto()
    
class JobCombatCategory(Enum):
    NA = auto()
    TANK = auto()
    HEALER = auto()
    DPS_MELEE = auto()
    DPS_RANGED = auto()
    DPS_MAGIC = auto()

JobData = namedtuple("JobData", ["id", "name_short", "name_en", "max_level", "job_discipline", "job_combat_category"])

class JobDB(object):
    PLD = JobData(id=Jobs.PLD, name_short="PLD", name_en="Paladin", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    WAR = JobData(id=Jobs.WAR, name_short="WAR", name_en="Warrior", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    DRK = JobData(id=Jobs.DRK, name_short="DRK", name_en="Dark Knight", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    GNB = JobData(id=Jobs.GNB, name_short="GNB", name_en="Gunbreaker", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    
    WHM = JobData(id=Jobs.WHM, name_short="WHM", name_en="White Mage", max_level=80, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.HEALER)
    SCH = JobData(id=Jobs.SCH, name_short="SCH", name_en="Scholar", max_level=80, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.HEALER)
    AST = JobData(id=Jobs.AST, name_short="AST", name_en="Astrologian", max_level=80, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.HEALER)
    
    MNK = JobData(id=Jobs.MNK, name_short="MNK", name_en="Monk", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    DRG = JobData(id=Jobs.DRG, name_short="DRG", name_en="Dragoon", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    NIN = JobData(id=Jobs.NIN, name_short="NIN", name_en="Ninja", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    SAM = JobData(id=Jobs.SAM, name_short="SAM", name_en="Samurai", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    
    BRD = JobData(id=Jobs.BRD, name_short="BRD", name_en="Bard", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_RANGED)
    MCH = JobData(id=Jobs.MCH, name_short="MCH", name_en="Machinist", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_RANGED)
    DNC = JobData(id=Jobs.DNC, name_short="DNC", name_en="Dancer", max_level=80, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_RANGED)
    
    BLM = JobData(id=Jobs.BLM, name_short="BLM", name_en="Black Mage", max_level=80, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    SMN = JobData(id=Jobs.SMN, name_short="SMN", name_en="Summoner", max_level=80, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    RDM = JobData(id=Jobs.RDM, name_short="RDM", name_en="Red Mage", max_level=80, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    BLU = JobData(id=Jobs.BLU, name_short="BLU", name_en="Blue Mage", max_level=50, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    
    CRP = JobData(id=Jobs.CRP, name_short="CRP", name_en="Carpenter", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    BSM = JobData(id=Jobs.BSM, name_short="BSM", name_en="Blacksmith", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    ARM = JobData(id=Jobs.ARM, name_short="ARM", name_en="Armorer", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    GSM = JobData(id=Jobs.GSM, name_short="GSM", name_en="Goldsmith", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    LTW = JobData(id=Jobs.LTW, name_short="LTW", name_en="Leatherworker", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    WVR = JobData(id=Jobs.WVR, name_short="WVR", name_en="Weaver", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    ALC = JobData(id=Jobs.ALC, name_short="ALC", name_en="Alchemist", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    CUL = JobData(id=Jobs.CUL, name_short="CUL", name_en="Culinarian", max_level=80, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    
    BTN = JobData(id=Jobs.BTN, name_short="BTN", name_en="Botanist", max_level=80, job_discipline=JobDiscipline.DOL, job_combat_category=JobCombatCategory.NA)
    MIN = JobData(id=Jobs.MIN, name_short="MIN", name_en="Miner", max_level=80, job_discipline=JobDiscipline.DOL, job_combat_category=JobCombatCategory.NA)
    FSH = JobData(id=Jobs.FSH, name_short="FSH", name_en="Fisher", max_level=80, job_discipline=JobDiscipline.DOL, job_combat_category=JobCombatCategory.NA)
    
    EUREKA = JobData(id=Jobs.EUREKA, name_short="EUREKA", name_en="Elemental Level", max_level=60, job_discipline=JobDiscipline.OTHER, job_combat_category=JobCombatCategory.NA)


class JobDBCache(object):
    def __init__(self):
        self.jobs_by_id = {}
        self.jobs_by_short = {}
        self.jobs_by_name = {}
        
        attrs = [attr for attr in dir(JobDB) if not attr.startswith("_")]
        for attr in attrs:
            job = getattr(JobDB, attr)
            self.jobs_by_short[attr] = job
            self.jobs_by_name[job.name_en] = job
            self.jobs_by_id[job.id] = job
            
    def get_job_by_name(self, name):
        return self.jobs_by_name.get(name)
        
    def get_job_by_short(self, short):
        return self.jobs_by_short.get(short)
        
    def get_job_by_id(self, id):
        return self.jobs_by_id.get(id)
        
        
JobDBCacheSingleton = JobDBCache()
    

class JobInfo(object):
    def __init__(self, job, level="", current_exp=0, max_exp=0):
        self.job = job
        self.level = level
        self.current_exp = current_exp
        self.max_exp = max_exp
        
    def __str__(self):
        return "{} Lv.{} {}/{}".format(self.job.name_en, self.level, self.current_exp, self.max_exp)
        
    def __unicode__(self):
        return "{} Lv.{} {}/{}".format(self.job.name_en, self.level, self.current_exp, self.max_exp)
        
    def update_info(self, data):
        self.level = data.get("level")
        self.current_exp = data.get("current_exp")
        self.max_exp = data.get("max_exp")


class Profile(object):
    def __init__(self):
        self.char_name = "NONAME"
        self.char_url = ""
        self.char_title = ""
        self.jobs = {}
        for job in JOBS_SHORT:
            self.jobs[job] = JobInfo(JobDBCacheSingleton.get_job_by_short(job))
        
    def set_job_info(self, job_info):
        job_data = job_info.get("job")
        if job_data:
            self.jobs[job_data.name_short].update_info(job_info)
                
    def print_report(self):
        print("Character: {} ({})".format(self.char_name, self.char_title))
        print("---------------------------------")
        for job in JOBS_SHORT:
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
    

def parse_profile(soup):
    p = Profile()
    chara_link = soup.find_all("a", {"class": "frame__chara__link"})[0]
    p.char_url = chara_link.attrs.get("href")
    p.char_name = chara_link.find_all("p", {"class": "frame__chara__name"})[0].next
    p.char_title = chara_link.find_all("p", {"class": "frame__chara__title"})[0].next
    jobs = soup.find_all("div", {"class": "character__job__level"})
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
    
