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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging


# Create your views here.
def workbench(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    # Check if the data is already scraped
    if 'scraped_items_indeed' not in request.session and 'scraped_items_simplyhired' not in request.session and 'scraped_items_timesjobs' not in request.session:
        if request.method == 'POST':
            search_option = request.POST.get('search_option')
            if search_option == 'manual':
                myprofession = request.POST.get('input_profession')
            elif search_option == 'profile':
                myprofession = profile.profession
            items_indeed = scrape_indeed(myprofession, 1)
            items_simplyhired = scrape_simplyhired(myprofession, 1)
            items_timesjobs = scrape_timesjobs(myprofession)
            # Store the scraped data in the session
            request.session['scraped_items_indeed'] = items_indeed
            request.session['scraped_items_simplyhired'] = items_simplyhired
            request.session['scraped_items_timesjobs'] = items_timesjobs
    else:
        if request.method == 'POST':
            search_option = request.POST.get('search_option')
            if search_option == 'manual':
                myprofession = request.POST.get('input_profession')
            elif search_option == 'profile':
                myprofession = profile.profession
            items_indeed = scrape_indeed(myprofession, 3)
            items_simplyhired = scrape_simplyhired(myprofession, 3)
            items_timesjobs = scrape_timesjobs(myprofession)
            # Store the scraped data in the session
            request.session['scraped_items_indeed'] = items_indeed
            request.session['scraped_items_simplyhired'] = items_simplyhired
            request.session['scraped_items_timesjobs'] = items_timesjobs
        # Use the stored data from the session
        items_indeed = request.session['scraped_items_indeed']
        items_simplyhired = request.session['scraped_items_simplyhired']
        items_timesjobs = request.session['scraped_items_timesjobs']
        combined_items = list(zip(items_indeed, items_simplyhired))
        paginator = Paginator(combined_items, 15)  # Show 10 items per page
        page_number = request.GET.get('page', 1)
        try:
            paginated_items = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            paginated_items = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver last page of results.
            paginated_items = paginator.page(paginator.num_pages)
        context = {
            'paginated_items': paginated_items,
            'paginator': paginator,
        }
        return render(request, 'job_list.html', context)

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



