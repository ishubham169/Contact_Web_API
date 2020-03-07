from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Contact, Message
from .serializers import ContactSerializer, MessageSerializer
import datetime
import json
from rest_framework.decorators import action
with open('./config.json') as config_file:
    config = json.load(config_file)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    @action(detail=True, methods=['GET'])
    def info(self, request, pk=None):
        try:
            contact = Contact.objects.get(id=pk)
            response = {"First_name": contact.first_name, "Last_name": contact.last_name,
                        "Phone_number": contact.phone_number}
            return Response(response, status=status.HTTP_200_OK)
        except:
            return Response({"message":"User Not Exist"}, status=status.HTTP_404_NOT_FOUND)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def list(self, request, *args, **kwargs):
        contacts = Contact.objects.all()
        response_list = []
        for contact in contacts:
            messages = Message.objects.filter(contact=contact.id)
            for message in messages:
                text = message.message
                delivered_Time = message.delivered_datetime
                response_list.append({"first_name": contact.first_name, "last_name": contact.last_name, "message": text,
                                      "time": delivered_Time})
        response_list = sorted(response_list, key=lambda i: (i["time"]))
        response = {"data": response_list}
        return Response(response, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def send(self, request, pk=None):
        payload = request.data
        phone_number = payload['phone_number']
        message = payload['message']
        is_success = send_twilio_message(phone_number, message)
        if is_success:
            contact = Contact.objects.get(id=pk)
            obj = Message(contact=contact, message=message, delivered_datetime=datetime.datetime.now())
            obj.save()
            return Response({"message":"Message sent successfully", "isSuccess":is_success})

        return Response({"message": "Something went Wrong!", "isSuccess": is_success})


def send_twilio_message(number, message):
    from twilio.rest import Client

    account_sid = config['TWILIO']['ACCOUNT_SID']
    auth_token = config['TWILIO']['AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    try:
        message = client.messages \
            .create(
            body=message,
            from_=config['TWILIO']['SENDER'],
            to=number
        )
    except:
        return False
    if message.error_message:
        return False
    return True