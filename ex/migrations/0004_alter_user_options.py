# Generated by Django 3.2.9 on 2021-11-03 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ex', '0003_auto_20211103_0029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can_delete_tip', 'Delete tips'),)},
        ),
    ]