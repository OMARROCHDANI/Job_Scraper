from bs4 import BeautifulSoup
import requests


titles_timesjobs = []
links_timesjobs = []

html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=computer science&txtLocation=').text
soup = BeautifulSoup(html_text , 'lxml')
jobs_timesjobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
for job in jobs_timesjobs :
    titles_timesjobs.append(job.a.text.replace('\n',''))
    links_timesjobs.append(job.a['href'])
items_timesjobs = zip(titles_timesjobs, links_timesjobs)
for title, link in items_timesjobs:
        print(f"Title: {title}, Link: {link}")
print(len(items_timesjobs))