import requests
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
            
        print("Character: {} ({})".format(self.char_name, self.char_title))
        print("---------------------------------")
        for job in JOBS_SHORT:
            print(self.jobs.get(job))
    
