from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from menu.models import Desk, Category, Requests


def menu(request):
    code = request.GET.get('desk', None)
    if code is None:
        raise Http404

    desk = get_object_or_404(Desk, code=code)
    categories = Category.objects.all()

    return render(request, 'menu.html', {
        'desk': desk,
        'categories': categories
    })


def request_waiter(request):
    code = request.GET.get('desk', None)
    if code is None:
        raise Http404

    desk = get_object_or_404(Desk, code=code)

    request = Requests(desk=desk)
    request.save()

    return JsonResponse({'success':True})



@login_required()
def waiter(request):
    return render(request, 'waiter.html')