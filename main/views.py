from django.http import HttpRequest
from django.shortcuts import render


def main(request: HttpRequest):

    return render(request, "main/main.html")

def listPage(request: HttpRequest):
    
    return render(request, 'main/listPage.html')

def detailPage(request: HttpRequest):
    
    return render(request, 'main/detailPage.html')
