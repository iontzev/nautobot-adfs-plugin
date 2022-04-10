import base64

from django.conf import settings as django_settings
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.http import QueryDict, HttpResponseRedirect
from django.contrib.auth.models import User

from rest_framework import viewsets

from .backend import OAuth2

class OAuth2Callback(View):
	def get(self, request):
		code = request.GET.get("code")
		if not code:
			q = QueryDict(mutable=True)
			q['error'] = '400'
			qstr = q.urlencode()
			return HttpResponseRedirect(django_settings.LOGIN_ERROR_REDIRECT_URL + '?' + qstr)

		oauth = OAuth2()
		user = oauth.authenticate(request=request, authorization_code=code)
		if user is not None:
			if user.is_active:
				login(request, user)
				q = QueryDict(mutable=True)
				q['access_token'] = user.token
				q['refresh_token'] = user.refresh_token
				qstr = q.urlencode()
				return HttpResponseRedirect(django_settings.LOGIN_REDIRECT_URL)
			else:
				q = QueryDict(mutable=True)
				q['error'] = '403' # you account is disable
				qstr = q.urlencode()
				return HttpResponseRedirect(django_settings.LOGIN_ERROR_REDIRECT_URL)

		else:
			q = QueryDict(mutable=True)
			q['error'] = '401' # login Failed
			qstr = q.urlencode()
			return HttpResponseRedirect(django_settings.LOGIN_ERROR_REDIRECT_URL)

