from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By


from bs4 import BeautifulSoup
import requests
from user_profile.models import Profile

from django.core.cache import cache
from user_profile.models import SavedJob

# Create your views here.
def workbench(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        links_indeed = []
        titles_simplyhired = []
        links_simplyhired = []
        titles_timesjobs = []
        links_timesjobs = []
        search_option = request.POST.get('search_option')
        if search_option == 'manual':
            myprofession = request.POST.get('input_profession')
        if search_option == 'profile':
            myprofession = profile.profession    
        cached_job_data = cache.get(f'cached_job_data_{user.id}_{myprofession}')
        if cached_job_data is None:
            driver = webdriver.Chrome()
            # Naviguer vers une page web :
            driver.get(f"https://www.indeed.com/jobs?q={myprofession}")
            # Find all the job titles on the page
            jobs_indeed = driver.find_elements(By.CLASS_NAME, "jobTitle.css-1h4a4n5.eu4oa1w0")
            titles_indeed = [title.text.strip() for title in jobs_indeed]
            for job in jobs_indeed:
                a_tag=job.find_element(By.TAG_NAME, "a")
                links_indeed.append(a_tag.get_attribute("href"))
            items_indeed=zip(titles_indeed, links_indeed)
            # Extract and print the job titles
            driver.get(f"https://www.simplyhired.com/jobs?q={myprofession}")
            # Find all the job titles on the page
            jobs_simplyhired = driver.find_elements(By.CLASS_NAME, "chakra-text.css-8rdtm5")
            titles_simplyhired = [title.text.strip() for title in jobs_simplyhired]    
            for job in jobs_simplyhired:
                a_tag=job.find_element(By.TAG_NAME, "a")
                links_simplyhired.append(a_tag.get_attribute("href"))
            items_simplyhired=zip(titles_simplyhired, links_simplyhired)
            html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={myprofession}&txtLocation=').text
            soup = BeautifulSoup(html_text , 'lxml')
            jobs_timesjobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')
            for job in jobs_timesjobs :
                titles_timesjobs.append(job.a.text.replace('\n',''))
                links_timesjobs.append(job.a['href'])
            items_timesjobs = zip(titles_timesjobs, links_timesjobs)
            cache.set(f'cached_job_data_{user.id}_{myprofession}', {
                'items_indeed': items_indeed,
                'items_simplyhired': items_simplyhired,
                'items_timesjobs': items_timesjobs,
                'saved_jobs': []  # Initialize an empty list for saved jobs
            }, 3600)  # Cache for 1 hour
        else:
            items_indeed = cached_job_data['items_indeed']
            items_simplyhired = cached_job_data['items_simplyhired']
            items_timesjobs = cached_job_data['items_timesjobs']

        context = {
            'items_indeed': items_indeed,
            'items_simplyhired': items_simplyhired,
            'items_timesjobs': items_timesjobs,
        }
        return render(request , 'job_list.html',context )
    return render(request, 'job_list.html')


@login_required
def save_job(request, job_id):
    if request.user.is_authenticated:
        # Retrieve the job using the job_id
        title = request.POST.get(f'title_{job_id}')
        link = request.POST.get(f'link_{job_id}')
        
        # Save the job to the database for the authenticated user
        SavedJob.objects.create(
            user=request.user,
            title=title,
            link=link
        )
        return JsonResponse({'message': 'Job saved successfully'})

    # Handle the case where the user is not authenticated
    return JsonResponse({'message': 'Authentication required'}, status=401)
