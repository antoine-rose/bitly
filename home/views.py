from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.contrib import messages

from .serializers import urlSerializer

from .validate_url import validate_url

from .models import Url
from .form import SubmitUrlForm

class urlList(APIView):
    def get(self,request):
        url_list = Url.objects.all()
        serializer = urlSerializer(url_list, many=True)
        return Response(serializer.data)

    def put(self,request):
        pass

    def post(self,request):
        pass

class Home(View):
    def get(self, request):
        submit_url_form = SubmitUrlForm()
        request.COOKIES['messages'] = ''
        if 'shortened_url' in request.COOKIES:
            shortened_url = request.COOKIES['shortened_url']
            short_url = Url.objects.get(url=shortened_url).short_url
            visit_count = Url.objects.get(url=shortened_url).visit_count
            context = {
                'submit_url_form': submit_url_form,
                'shortened_url': shortened_url,
                'short_url': short_url,
                'domain_name': 'http://bitly.com/',
                'visit_count': visit_count,
            }
            return render(request, 'home/historic.html',context)
        else:
            context = {'submit_url_form': submit_url_form,}
            return render(request, 'home/index.html',context)


    def post(self,request):
        submit_url_form = SubmitUrlForm(request.POST)
        url = request.POST.__getitem__('url')
        context = {'submit_url_form': submit_url_form,}
        is_valid, validated_url = validate_url(url)
        if not is_valid:
            messages.add_message(request, messages.ERROR, 'home/index.html')
            print("Invalid URL")
            return render(request, "home/index.html", context)

        request.COOKIES['messages'] = ''

        existing_url, is_created = Url.objects.get_or_create(url=validated_url)
        if is_created:
            new_url = Url.objects.get(url=validated_url)
            new_url.create_short_url()
            url = new_url
        else:
            url = existing_url

        shortened_url = url.url
        short_url = Url.objects.get(url=shortened_url).short_url
        visit_count = Url.objects.get(url=shortened_url).visit_count
        context = {
            'submit_url_form': submit_url_form,
            'shortened_url': shortened_url,
            'short_url': short_url,
            'domain_name': 'http://bitly.com/',
            'visit_count': visit_count,
        }
        response = render(request, 'home/historic.html',context)
        response.set_cookie('shortened_url', shortened_url)
        return response


def redirect(request):
    try:
        url_content = Url.objects.get(short_url=request.path[1:])
        url = url_content.url
        url_content.update_visit_count()
    except:
        raise Http404
    return HttpResponseRedirect(url)
