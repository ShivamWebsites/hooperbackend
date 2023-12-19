from django.shortcuts import render, HttpResponse, redirect
from rest_framework import viewsets
from .models import GroupMessage,PlayerInformation
from .serializers import chatSerializer,playerSerializer


class GroupMessageViewSet(viewsets.ModelViewSet):
    queryset = GroupMessage.objects.all()
    serializer_class = chatSerializer



class playerViewSet(viewsets.ModelViewSet):
    queryset = PlayerInformation.objects.all()
    serializer_class = playerSerializer