import requests
from bs4 import BeautifulSoup
import pandas as pd

joblist = []

def extract(page, job):
    # job.replace(" ", "+")
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'}
    url = f'https://ca.indeed.com/jobs?q={job}&l=Toronto%2C+ON&start={page}'
    print(url)
    r = requests.get(url,headers)
    soup  = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('a', class_ = 'tapItem')
    for v in divs:
        title = v.find('h2').text.strip().replace('new','')
        company = v.find('span', class_ = 'companyName').text.strip()
        try:
            salary = v.find('div', class_ = "salary-snippet").text.strip()
        except:
            salary = '--'
        try:
            summary = v.find('div', class_ = "job-snippet").text.strip().replace('\n','')
        except:
            summary = ''
        link = 'https://ca.indeed.com' + (v['href'])
        job = {
            'Title' : title,
            'Company' : company,
            'Salary' : salary,
            'Summary' : summary,
            "Link" : link
        }
        joblist.append(job)
    return

def jobscrape(job):
    
    for i in range(0,31,10):
        c = extract(page=i,job=job)
        transform(c)

    df = pd.DataFrame(joblist)

    df['Link'] = df['Link'].apply(lambda x : f'<a href="{x}">Link</a>')

    df.to_html('templates/jobs.html', render_links = True, escape = False, justify='left', index = False)



    joblist.clear()