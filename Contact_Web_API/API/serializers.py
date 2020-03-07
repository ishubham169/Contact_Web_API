from rest_framework import serializers
from .models import Contact, Message


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'phone_number')


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'contact_id', 'message', 'delivered_datetime')
