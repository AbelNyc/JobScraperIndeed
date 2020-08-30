
import requests,pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv 

lst_csv = []
r = requests.get("https://www.indeed.com/jobs?as_and=software%20engineering%202021&as_phr&as_any&as_not&as_ttl&as_cmp&jt=all&st&as_src&salary&radius=25&l&fromage=any&limit=50&sort&psf=advsrch&from=advancedsearch&vjk=feb8c8fef1d0b421")


soup = BeautifulSoup(r.text,"html.parser")
print(soup.prettify())

file= pd.DataFrame(columns=["Location","Company","Summary","Title","Link"])


def extract_job_title(soup): 
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
      for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
          jobs.append(a["title"])
    file['Title'] = pd.Series(jobs)
    lst_csv.append(jobs)

    return(jobs)

def company(soup):
    company_names=[]
    for div in soup.find_all(name="div",attrs={"class":"row"}):
        companies = div.find_all(name="span",attrs={"class":"company"})
        for company in companies:
                company_names.append(company.text.strip())
        else:
            companies2 = div.find_all(name="span",attrs={"class":"turnstileLink"})
            for company in companies2:
                    company_names.append(company.text.strip())
    file['Company'] = pd.Series(company_names)
    return(company_names)



def location(soup):
    locations = []
    cities = soup.findAll('span',attrs={'class':'location'})
    for city in cities:
        locations.append(city.text)
    file['Location'] = pd.Series(locations)
    return locations

def extract_job_link(): 
   urlss=[]
   tbl = soup.find(id="resultsCol")
   for link in tbl.find_all('a'):
        if link.has_attr('href') and "clk" in link.attrs['href']:
            url = link.attrs['href']
            full_url = "www.indeed.com" + str(url)
            urlss.append(full_url.strip())
   file['Link'] = pd.Series(urlss)
   return urlss
    
extract_job_title(soup)
company(soup)
location(soup)
extract_job_link()


file.to_csv("Jobs.csv")
