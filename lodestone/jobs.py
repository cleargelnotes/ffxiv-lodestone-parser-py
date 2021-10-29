from enum import Enum, auto
from collections import namedtuple


JOBS_SHORT = [
    "PLD", "WAR", "DRK", "GNB",
    "WHM", "SCH", "AST", "SGE",
    "BRD", "MCH", "DNC",
    "MNK", "DRG", "NIN", "SAM", "RPR",
    "BLM", "SMN", "RDM", "BLU",
    "CRP", "BSM", "ARM", "GSM", "WVR", "LTW", "ALC", "CUL",
    "BTN", "MIN", "FSH",
    
    "EUREKA", "BOZJA"
]

class Jobs(Enum):
    PLD = auto()
    WAR = auto()
    DRK = auto()
    GNB = auto()
    
    WHM = auto()
    SCH = auto()
    AST = auto()
    SGE = auto()
    
    BRD = auto()
    MCH = auto()
    DNC = auto()
    
    MNK = auto()
    DRG = auto()
    NIN = auto()
    SAM = auto()
    RPR = auto()
    
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
    BOZJA = auto()
    
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

JobData = namedtuple("JobData", ["id", "name_short", "name_en", "class_en", "max_level", "job_discipline", "job_combat_category"])

class JobDB(object):
    PLD = JobData(id=Jobs.PLD, name_short="PLD", name_en="Paladin", class_en="Gladiator", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    WAR = JobData(id=Jobs.WAR, name_short="WAR", name_en="Warrior", class_en="Marauder", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    DRK = JobData(id=Jobs.DRK, name_short="DRK", name_en="Dark Knight", class_en="Dark Knight", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    GNB = JobData(id=Jobs.GNB, name_short="GNB", name_en="Gunbreaker", class_en="Gunbreaker", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.TANK)
    
    WHM = JobData(id=Jobs.WHM, name_short="WHM", name_en="White Mage", class_en="Conjurer", max_level=90, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.HEALER)
    SCH = JobData(id=Jobs.SCH, name_short="SCH", name_en="Scholar", class_en="Arcanist", max_level=90, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.HEALER)
    AST = JobData(id=Jobs.AST, name_short="AST", name_en="Astrologian", class_en="Astrologian", max_level=90, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.HEALER)
    SGE = JobData(id=Jobs.SGE, name_short="SGE", name_en="Sage", class_en="Sage", max_level=90, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.HEALER)
    
    MNK = JobData(id=Jobs.MNK, name_short="MNK", name_en="Monk", class_en="Pugilist", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    DRG = JobData(id=Jobs.DRG, name_short="DRG", name_en="Dragoon", class_en="Lancer", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    NIN = JobData(id=Jobs.NIN, name_short="NIN", name_en="Ninja", class_en="Rogue", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    SAM = JobData(id=Jobs.SAM, name_short="SAM", name_en="Samurai", class_en="Samurai", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    RPR = JobData(id=Jobs.RPR, name_short="RPR", name_en="Reaper", class_en="Reaper", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_MELEE)
    
    BRD = JobData(id=Jobs.BRD, name_short="BRD", name_en="Bard", class_en="Archer", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_RANGED)
    MCH = JobData(id=Jobs.MCH, name_short="MCH", name_en="Machinist", class_en="Machinist", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_RANGED)
    DNC = JobData(id=Jobs.DNC, name_short="DNC", name_en="Dancer", class_en="Dancer", max_level=90, job_discipline=JobDiscipline.DOW, job_combat_category=JobCombatCategory.DPS_RANGED)
    
    BLM = JobData(id=Jobs.BLM, name_short="BLM", name_en="Black Mage", class_en="Thaumaturge", max_level=90, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    SMN = JobData(id=Jobs.SMN, name_short="SMN", name_en="Summoner", class_en="Arcanist", max_level=90, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    RDM = JobData(id=Jobs.RDM, name_short="RDM", name_en="Red Mage", class_en="Red Mage", max_level=90, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    BLU = JobData(id=Jobs.BLU, name_short="BLU", name_en="Blue Mage", class_en="Blue Mage", max_level=70, job_discipline=JobDiscipline.DOM, job_combat_category=JobCombatCategory.DPS_MAGIC)
    
    CRP = JobData(id=Jobs.CRP, name_short="CRP", name_en="Carpenter", class_en="Carpenter", max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    BSM = JobData(id=Jobs.BSM, name_short="BSM", name_en="Blacksmith", class_en="Blacksmith", max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    ARM = JobData(id=Jobs.ARM, name_short="ARM", name_en="Armorer", class_en="Armorer", max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    GSM = JobData(id=Jobs.GSM, name_short="GSM", name_en="Goldsmith", class_en="Goldsmith", max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    LTW = JobData(id=Jobs.LTW, name_short="LTW", name_en="Leatherworker", class_en="Leatherworker", max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    WVR = JobData(id=Jobs.WVR, name_short="WVR", name_en="Weaver", class_en="Weaver",  max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    ALC = JobData(id=Jobs.ALC, name_short="ALC", name_en="Alchemist", class_en="Alchemist",  max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    CUL = JobData(id=Jobs.CUL, name_short="CUL", name_en="Culinarian", class_en="Culinarian", max_level=90, job_discipline=JobDiscipline.DOH, job_combat_category=JobCombatCategory.NA)
    
    BTN = JobData(id=Jobs.BTN, name_short="BTN", name_en="Botanist", class_en="Botanist", max_level=90, job_discipline=JobDiscipline.DOL, job_combat_category=JobCombatCategory.NA)
    MIN = JobData(id=Jobs.MIN, name_short="MIN", name_en="Miner", class_en="Miner", max_level=90, job_discipline=JobDiscipline.DOL, job_combat_category=JobCombatCategory.NA)
    FSH = JobData(id=Jobs.FSH, name_short="FSH", name_en="Fisher", class_en="Fisher", max_level=90, job_discipline=JobDiscipline.DOL, job_combat_category=JobCombatCategory.NA)
    
    EUREKA = JobData(id=Jobs.EUREKA, name_short="EUREKA", name_en="Elemental Level", class_en="Elemental Level", max_level=60, job_discipline=JobDiscipline.OTHER, job_combat_category=JobCombatCategory.NA)
    BOZJA = JobData(id=Jobs.BOZJA, name_short="BOZJA", name_en="Resistance Rank", class_en="Resistance Rank", max_level=25, job_discipline=JobDiscipline.OTHER, job_combat_category=JobCombatCategory.NA)


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
            self.jobs_by_name[job.class_en] = job
            
    def get_job_by_name(self, name):
        return self.jobs_by_name.get(name)
        
    def get_job_by_short(self, short):
        return self.jobs_by_short.get(short)
        
    def get_job_by_id(self, id):
        return self.jobs_by_id.get(id)
        
        
JobDBCacheSingleton = JobDBCache()
    
def job_data_to_dict(job):
    return {
        "id": job.id.name,
        "name": job.name_en,
        "max_level": job.max_level,
        "job_discipiline": job.job_discipline.name,
        "job_combat_category": job.job_combat_category.name
    }

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
        
    def to_json_dict(self):
        ret = job_data_to_dict(self.job)
        ret.update({
            "level": self.level,
            "current_exp": self.current_exp,
            "max_exp": self.max_exp
        })
        return ret
