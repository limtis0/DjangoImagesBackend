# Generated by Django 4.1.7 on 2023-02-20 09:45

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expiringlink',
            name='uuid',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=22),
        ),
        migrations.AlterField(
            model_name='image',
            name='private_uuid',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=22, unique=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='uuid',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=22, primary_key=True, serialize=False),
        ),
    ]
