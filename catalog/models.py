from django.db import models
from rest_framework import serializers
#import uuid # Required for unique book instances
from uuid import uuid4
from datetime import datetime

def generateUUID():
    return str(uuid4())


class User(models.Model):

    user_id = models.CharField(primary_key=True,default=generateUUID, max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=15, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    login_type = models.IntegerField(null=False, blank=False)
    login_counter = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VoiceReq(models.Model):
    voice_req_id = models.CharField(primary_key=True,default=generateUUID, max_length=50, unique=True, editable=False)
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    text = models.TextField(null=False, blank=False)
    audio_file_name = models.CharField(max_length=255, null=False, blank=False)
    record_start_time = models.DateTimeField(null=False, blank=False)
    record_end_time = models.DateTimeField(null=False, blank=False)
    created_date = models.DateTimeField(default=datetime.now,null=False, blank=False)
    record_type = models.SmallIntegerField(max_length=1, null=False, blank=False)

    def __str__(self):
        return self.audio_file_name

    class Meta:
        db_table = 'voice_req'


class ReceiverCaller(models.Model):
    receiver_caller_id = models.CharField(primary_key=True,default=generateUUID, max_length=50, unique=True, editable=False)
    voice_req = models.ForeignKey('VoiceReq', on_delete=models.SET_NULL, null=True)
    caller_phone_no = models.CharField(max_length=15, null=False, blank=False)
    receiver_phone_no = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.receiver_caller_id

    class Meta:
        db_table = 'receiver_caller'


class Name(models.Model):
    name_id = models.CharField(primary_key=True, default=generateUUID, max_length=50, unique=True, editable=False)
    voice_req = models.ForeignKey('VoiceReq', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name_id

    class Meta:
        db_table = 'name'


class Phone(models.Model):
    phone_id = models.CharField(primary_key=True, default=generateUUID, max_length=50, unique=True,editable=False)
    voice_req = models.ForeignKey('VoiceReq', on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.phone_id

    class Meta:
        db_table = 'phone'


class Email(models.Model):
    email_id = models.CharField(primary_key=True, default=generateUUID, max_length=50, unique=True,editable=False)
    voice_req = models.ForeignKey('VoiceReq', on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.email_id

    class Meta:
        db_table = 'email'



