#from django.shortcuts import render

import json, requests, random, re
from pprint import pprint
from django.views import generic
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

PAGE_ACCESS_TOKEN = "EAAXffOTVZAtYBAGrTcncAZBsl96bNfOuz6h15LnHkZBnqvJmoiaha02e6mcwiIZBSFUfBpZCRm2oVZBvZCDK4onG42AFE2IarwPG9pe5uZB1chCZBFZAOqAkZBWv0kPj9vDxjmnfl4f5yW6uGRnt1wyWkJPEjIOw5eiKjH78vg2V8KtngZDZD"
VERIFY_TOKEN = "tinkerbell"
FACEBOOK_GRAPH = "https://graph.facebook.com/v2.6/me"

def get_started():
    post_message_url = "%s/thread_settings?access_token=%s" %(FACEBOOK_GRAPH, PAGE_ACCESS_TOKEN)
    response_msg = json.dumps({
        "setting_type":"call_to_actions",
        "thread_state":"new_thread",
        "call_to_actions":[
            {
                "payload":"USER_DEFINED_PAYLOAD"
            }
        ]
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


def send_message(fb_id, message):
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % (PAGE_ACCESS_TOKEN)
    response_msg = json.dumps({"recipient": {"id": fb_id}, "message": {"text": message}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())

def send_image(fb_id, image):
    post_message_url = "https://graph.facebook.com/v2.6/me/messages?access_token=%s" % (PAGE_ACCESS_TOKEN)
    response_msg = json.dumps({"recipient": {"id": fb_id}, "message": {"attachment":{"type":"image","payload":{"url":image}}}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())

# Create your views here.
class NeverlandView(generic.View):

    #GET request. Only called when it's hooked, by Facebook
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    #POST. Called when user is sends a message
    def post(self, request, *args, **kwargs):
        pprint("Message received")
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        pprint("print incoming_message:")
        pprint(incoming_message)
        for entry in incoming_message['entry']:
            pprint("Sender ID: ")
            pprint(entry['id'])
            UID = None
            if True: #user.check(UID)['success']:
                #string RID = user.current_RID(UID)
                for message in entry['messaging']:
                    UID = message['sender']['id']
                    if 'message' in message and 'text' in message['message']:
                        msg = message['message']['text']
                        send_message(UID, msg)
                    if 'attachments' in message:
                        img = message['attachments']['payload']['url']
                        send_image(UID, img)
            else:
                #pprint(user.check(UID)['message'])
                send_message(message['sender']['id'], "Need Setting")

        return HttpResponse()


