from django.shortcuts import HttpResponse
from datetime import datetime
# Create your views here.

def hello_view(requests):
    if requests.method == "GET":
        return HttpResponse("Hello, Its my project!")
    
def now_date_view(requests):
    if requests.method == "GET":
        now = datetime.now()
        return HttpResponse(now)

def goodby_view(requests):
    if requests.method == "GET":
        return HttpResponse("Goodby user!")