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
    post_message_url = "%s/thread_settings?access_token=%s" % (FACEBOOK_GRAPH, PAGE_ACCESS_TOKEN)
    response_msg = json.dumps({
        "setting_type":"call_to_actions",
        "thread_state":"new_thread",
        "call_to_actions":[
            {
                "payload":"GET_STARTED"
            }
        ]
    })
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())


def call_send_api(message_data):
    post_message_url = "%s/messages?access_token=%s" % (FACEBOOK_GRAPH, PAGE_ACCESS_TOKEN)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=message_data)
    pprint(status.json())

def send_message(fb_id, message):
    message_data = json.dumps(
        {"recipient":
             {"id": fb_id},
         "message":
             {"text": message}
        })
    call_send_api(message_data)


def send_image(fb_id, image_url):
    message_data = json.dumps(
        {"recipient":
             {"id": fb_id},
         "message":
             {"attachment":
                  {"type":"image",
                   "payload":
                       {"url":image_url}
                   }
              }
         }
    )
    call_send_api(message_data)

def send_buttons(fb_id, img):
    message_data = json.dumps(
        {"recipient": {"id": fb_id},
         "message":{ "attachment":{"type":"template","payload":{"template_type":"generic",
         "elements":[{
            "title":"Title",
            "image_url":img,
            "subtitle":"Subtitle",
            "buttons":[
              {
                "type":"postback",
                "title":"Yes",
                "payload": "USER_PRESSED_YES"
              },
              {
                "type":"postback",
                "title":"No",
                "payload":"USER_PRESSED_NO"
              },
              {
                "type":"postback",
                "title":"Give me more!",
                "payload":"USER_PRESSED_GIVE_ME_MORE"
              }]}]}}}})
    call_send_api(message_data)

def handle_payload(UID, payload):
    pprint("Handling payload..")
    if payload == "USER_PRESSED_YES":
        send_message(UID, "You said yes!")
    elif payload == "USER_PRESSED_NO":
        send_message(UID, "You said no!" )
    elif payload == "USER_PRESSED_GIVE_ME_MORE":
        send_message(UID, "Give me more!"),
    elif payload == "GET_STARTED":
        send_message(UID, "Welcome!")


# Create your views here.
class NeverlandView(generic.View):

    #GET request. Only called when it's hooked, by Facebook
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            get_started()
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
            for message in entry['messaging']:
                UID = message['sender']['id']
                if 'message' in message and 'text' in message['message']:
                    msg = message['message']['text']
                    send_message(UID, msg)
                if 'message' in message and 'attachments' in message['message']:
                    pprint("Receive an image")
                    for attachment in message['message']['attachments']:
                        if attachment['type'] == 'image':
                            img = attachment['payload']['url']
                            pprint("IMAGE: %s" % img)
                            send_buttons(UID, img)
                if 'postback' in message:
                    handle_payload(UID, message['postback']['payload'])

        return HttpResponse()


