# Generated by Django 3.1.7 on 2021-03-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complaint', '0014_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='branch',
            field=models.CharField(choices=[('cse', 'cse'), ('ece', 'ece'), ('eee', 'eee'), ('civil', 'civil'), ('mech', 'mech'), ('mme', 'mme'), ('chemical', 'chemical'), ('biotech', 'biotech'), ('none', 'none')], default='none', max_length=10),
        ),
    ]
