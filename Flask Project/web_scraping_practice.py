import requests
from bs4 import BeautifulSoup
import pandas as pd

joblist = []

#this method is used to extract a page from indeed based on inputs.
def extract(page, job):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50'}
    url = f'https://ca.indeed.com/jobs?q={job}&l=Toronto%2C+ON&start={page}'
    print(url)
    r = requests.get(url,headers)
    soup  = BeautifulSoup(r.content, 'html.parser')
    return soup

#this method takes the extracted page and locates the information then appends them to a list
def find_info(soup):
    divs = soup.find_all('a', class_ = 'tapItem')
    for v in divs:
        title = v.find('h2').text.strip().replace('new','')
        company = v.find('span', class_ = 'companyName').text.strip()
        #sometimes there aren't any salaries, so in this case we put a '--' so we dont get an error
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

#this method is what is used by Flask when a user inputs what job they are searching for and returns the first 3 pages of results.
def jobscrape(job):
    
    for i in range(0,31,10):
        c = extract(page=i,job=job)
        find_info(c)

    df = pd.DataFrame(joblist)

    df['Link'] = df['Link'].apply(lambda x : f'<a href="{x}">Link</a>')

    df.to_html('templates/jobs.html', render_links = True, escape = False, justify='left', index = False)


    #clearing the list between function uses so the table doesn't constantly grow
    joblist.clear()
