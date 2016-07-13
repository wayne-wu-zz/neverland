#from django.shortcuts import render

import json, requests, random, re
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

PAGE_ACCESS_TOKEN = "EAAXffOTVZAtYBAGrTcncAZBsl96bNfOuz6h15LnHkZBnqvJmoiaha02e6mcwiIZBSFUfBpZCRm2oVZBvZCDK4onG42AFE2IarwPG9pe5uZB1chCZBFZAOqAkZBWv0kPj9vDxjmnfl4f5yW6uGRnt1wyWkJPEjIOw5eiKjH78vg2V8KtngZDZD"
VERIFY_TOKEN = "tinkerbell"

def post_facebook_message(fb_id, send_message):
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s", PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fb_id}, "message": {"text": send_message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


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
            for message in entry['messaging']:
                if 'message' in message:
                    pprint("Text in Message")
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])
        return HttpResponse()
 
