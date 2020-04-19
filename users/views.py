from django.shortcuts import render

# Create your views here.


def test(request):
    context = {'greeting': 'hello'}
    return render(request, 'users/test.html', context)
