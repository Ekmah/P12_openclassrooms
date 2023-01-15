from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from epic_events.models import Client, Contract, Event


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        depth = 0
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'date_created', 'date_updated',
                  'sales_contact']


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contract
        depth = 0
        fields = ['id', 'sales_contact', 'client', 'date_created',
                  'date_updated', 'status', 'amount', 'payment_due']


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        depth = 0
        fields = ['id', 'client', 'date_created', 'date_updated',
                  'support_contact', 'event_status', 'attendees', 'event_date',
                  'notes']
