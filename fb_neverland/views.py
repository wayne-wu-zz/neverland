#from django.shortcuts import render

import json, requests, random, re
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


VERIFY_TOKEN = "tinkerbell"

# Create your views here.
class NeverlandView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        pprint("Message received")
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        pprint("print incoming_message:")
        pprint(incoming_message)
	    for entry in incoming_message['entry']:
	        pprint ("print entry: ")
            pprint (entry)
            #pprint(entry)
            for 'message' in entry['messaging']:
		        #print message
                #if 'text' in message:
                pprint("print message")
                pprint(message)
        return HttpResponse()
 
