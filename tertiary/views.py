from django.shortcuts import render
def profile(request):
    return render(request, 'template/profile.html')
def quotes(request):
    return render(request, 'template/quotes.html')
