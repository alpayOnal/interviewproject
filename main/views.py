# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from main.models import *
from datetime import datetime

from uuid import uuid4
from urlparse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scrapyd_api import ScrapydAPI
from main.models import ScrapyItem
scrapyd = ScrapydAPI('http://localhost:6800')

# Create your views here.
# def main_view(request):
	# webSite = WebSite.objects()[0]
	# pageList = webSite.pageList
	# # webSite = WebSite()
	# # webSite.domain = "http://www.google.com.tr"
	# # pageList = []

	# page1 = Page()
	# page1.url = "http://www.google.com.tr1"
	# page1.last_update = datetime.now
	# pageList.append(page1)

	# webSite.pageList = pageList
	# webSite.save()
	# return HttpResponse("selam")

def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url) 
    except ValidationError:
        return False

    return True


@csrf_exempt
@require_http_methods(['POST', 'GET'])
def crawl(request):
    if request.method == 'POST':
        url = request.POST.get('url', None)

        if not url:
            return JsonResponse({'error': 'Missing  args'})
        
        if not is_valid_url(url):
            return JsonResponse({'error': 'URL is invalid'})
        
        domain = urlparse(url).netloc
        unique_id = str(uuid4())
        
        settings = {
            'unique_id': unique_id, # unique ID for each record for DB
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        task = scrapyd.schedule('default', 'crawler', 
            settings=settings, url=url, domain=domain)
        
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })

    
    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)

        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        status = scrapyd.job_status('default', task_id)
        if status == 'finished':
            try:
                item = ScrapyItem.objects.get(unique_id=unique_id) 
                return JsonResponse({'data': item.to_dict['data']})
            except Exception as e:
                return JsonResponse({'error': str(e)})
        else:
            return JsonResponse({'status': status})