# Generated by Django 2.0 on 2019-08-15 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20190815_1024'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='voice_req_id',
            new_name='voice_req',
        ),
        migrations.RenameField(
            model_name='name',
            old_name='voice_req_id',
            new_name='voice_req',
        ),
        migrations.RenameField(
            model_name='phone',
            old_name='voice_req_id',
            new_name='voice_req',
        ),
        migrations.RenameField(
            model_name='receivercaller',
            old_name='voice_req_id',
            new_name='voice_req',
        ),
        migrations.RenameField(
            model_name='voicereq',
            old_name='user_id',
            new_name='user',
        ),
    ]