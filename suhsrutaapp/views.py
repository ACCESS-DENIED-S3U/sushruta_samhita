from django.shortcuts import render

# Create your views here.
def test1(request):
    return render(request, 'suhsrutaapp/d_dash.html')


def test2(request):
    return render(request, 'suhsrutaapp/request.html')