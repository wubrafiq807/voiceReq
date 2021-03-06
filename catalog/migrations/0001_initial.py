# Generated by Django 2.1.7 on 2019-08-13 03:10

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('email_id', models.CharField(default=catalog.models.generateUUID, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('email', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'email',
            },
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('name_id', models.CharField(default=catalog.models.generateUUID, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'name',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('phone_id', models.CharField(default=catalog.models.generateUUID, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('phone', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'phone',
            },
        ),
        migrations.CreateModel(
            name='ReceiverCaller',
            fields=[
                ('receiver_caller_id', models.CharField(default=catalog.models.generateUUID, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('caller_phone_no', models.CharField(max_length=15)),
                ('receiver_phone_no', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'receiver_caller',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(default=catalog.models.generateUUID, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
                ('login_type', models.IntegerField()),
                ('login_counter', models.IntegerField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='VoiceReq',
            fields=[
                ('voice_req_id', models.CharField(default=catalog.models.generateUUID, editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('text', models.TextField()),
                ('audio_file_name', models.CharField(max_length=255)),
                ('record_start_time', models.DateField(max_length=15)),
                ('record_end_time', models.DateField(max_length=15)),
                ('created_date', models.DateField(max_length=15)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.User')),
            ],
            options={
                'db_table': 'voice_req',
            },
        ),
        migrations.AddField(
            model_name='receivercaller',
            name='voice_req_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.VoiceReq'),
        ),
        migrations.AddField(
            model_name='phone',
            name='voice_req_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.VoiceReq'),
        ),
        migrations.AddField(
            model_name='name',
            name='voice_req_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.VoiceReq'),
        ),
        migrations.AddField(
            model_name='email',
            name='voice_req_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.VoiceReq'),
        ),
    ]
