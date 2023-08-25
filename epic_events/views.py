from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics, permissions
from .serializers import ClientSerializer, UserSerializer, GroupSerializer, \
    RegisterSerializer, ContractSerializer, EventSerializer
from .models import Client, Contract


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.DjangoModelPermissions]


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    # queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def perform_create(self, serializer):
        sales_contact_id = self.request.data["sales_contact_id"]
        sales_contact = User.objects.get(id=sales_contact_id)
        serializer.save(sales_contact=sales_contact)

    def get_queryset(self):
        queryset = Client.objects.filter(
            sales_contact=self.request.user,
            sales_contact__groups=Group.objects.get(name='sales_team')
        ) | Client.objects.filter(
            event__in=self.request.user.event_set.all(),
            event__support_contact__groups=Group.objects.get(
                name='support_team'))
        queryset = queryset.distinct()
        last_name = self.request.query_params.get('last_name')
        if last_name is not None:
            queryset = queryset.filter(last_name=last_name)

        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(email=email)
        return queryset


class ContractViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    # queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def perform_create(self, serializer):
        client_id = self.request.data["client_id"]
        client = Client.objects.get(id=client_id)
        sales_contact_id = self.request.data["sales_contact_id"]
        sales_contact = User.objects.get(id=sales_contact_id)
        serializer.save(client=client, sales_contact=sales_contact)

    def get_queryset(self):
        queryset = Contract.objects.filter(
            client__in=self.request.user.client_set.all())

        last_name = self.request.query_params.get('last_name')
        if last_name is not None:
            queryset = queryset.filter(
                client__last_name=last_name)

        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(
                client__email=email)

        payment_due = self.request.query_params.get('payment_due')
        if payment_due is not None:
            queryset = queryset.filter(
                payment_due=payment_due)

        amount = self.request.query_params.get('amount')
        if amount is not None:
            queryset = queryset.filter(
                amount=amount)
        return queryset


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows projects to be viewed or edited.
    """

    serializer_class = EventSerializer
    permission_classes = (permissions.DjangoModelPermissions,)

    def perform_create(self, serializer):
        client_id = self.request.data["client_id"]
        client = Client.objects.get(id=client_id)
        support_contact_id = self.request.data["support_contact_id"]
        support_contact = User.objects.get(id=support_contact_id)
        event_status_id = self.request.data["event_status_id"]
        event_status = Contract.objects.get(id=event_status_id)
        serializer.save(client=client, support_contact=support_contact,
                        event_status=event_status)

    def get_queryset(self):
        queryset = self.request.user.event_set.all()

        last_name = self.request.query_params.get('last_name')
        if last_name is not None:
            queryset = queryset.filter(
                client__last_name=last_name)

        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(
                client__email=email)

        event_date = self.request.query_params.get('event_date')
        if event_date is not None:
            queryset = queryset.filter(event_date=event_date)
        return queryset
