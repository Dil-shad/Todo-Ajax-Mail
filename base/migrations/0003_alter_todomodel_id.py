# Generated by Django 4.2.4 on 2023-09-05 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_todomodel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todomodel',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
