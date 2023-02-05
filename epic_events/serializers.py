from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

from rest_framework import serializers
from epic_events.models import Client, Contract, Event


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'password']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name',
                  'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        depth = 0
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'date_created', 'date_updated',
                  'sales_contact_id']
        read_only_fields = ['sales_contact']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        depth = 0
        fields = ['id', 'sales_contact_id', 'date_created', 'client_id',
                  'date_updated', 'status', 'amount', 'payment_due']

        read_only_fields = ['sales_contact', 'client']
        extra_kwargs = {
            'client': {'read_only': True}
        }


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        depth = 0
        fields = ['id', 'client_id', 'date_created', 'date_updated',
                  'support_contact_id', 'event_status_id', 'attendees',
                  'event_date', 'notes']
        read_only_fields = ['client', 'support_contact', 'event_status']
