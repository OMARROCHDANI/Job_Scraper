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

from scraping_logic.indeed import scrape_indeed
from scraping_logic.simplyhired import scrape_simplyhired
from scraping_logic.timesjobs import scrape_timesjobs


# Create your views here.
def workbench(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        search_option = request.POST.get('search_option')
        if search_option == 'manual':
            myprofession = request.POST.get('input_profession')
        if search_option == 'profile':
            myprofession = profile.profession    
        cached_job_data = cache.get(f'cached_job_data_{user.id}_{myprofession}')
        if cached_job_data is None:
            items_indeed = scrape_indeed(myprofession, 3)
            items_simplyhired = scrape_simplyhired(myprofession, 3)
            items_timesjobs = scrape_timesjobs(myprofession)
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
