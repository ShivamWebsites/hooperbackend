# Generated by Django 4.2.4 on 2023-09-22 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default=None, max_length=1000)),
                ('is_seen', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_messages_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
