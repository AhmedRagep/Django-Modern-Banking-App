# Generated by Django 4.2.6 on 2023-10-13 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_kyc_identity_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='kyc',
            name='account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.account'),
        ),
    ]
