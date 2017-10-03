# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create Profile Module
import sys
sys.path.append('../')

import CreateProfile
# Create your views here.
def pythonfunction(string):
	sys.stdout.write(string)

def index(request):
	if(request.GET.get('createProfileButton')):
		pythonfunction( str(request.GET.get('profileNameInput')))
	return render(request, 'form/form.html')
