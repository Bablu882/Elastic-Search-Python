# Generated by Django 4.1.4 on 2023-01-18 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Accountid', models.CharField(max_length=100, unique=True)),
                ('AccountName', models.CharField(max_length=100)),
                ('State', models.CharField(max_length=100)),
                ('LastPurchasedDtae', models.CharField(max_length=50)),
                ('TotalPurchase', models.CharField(max_length=100)),
                ('PersonHasOptedOutOfEmail', models.CharField(choices=[('OptIn', 'OptIn'), ('OptOut', 'OptOut')], max_length=20)),
                ('CategoryOfInterest', models.CharField(max_length=100)),
                ('PeriodOfInterest', models.CharField(max_length=100)),
                ('TypeOfInterest', models.CharField(max_length=100)),
                ('YoungerAudience', models.CharField(max_length=100)),
                ('Star5', models.IntegerField()),
                ('AccountLastPurchaseDate', models.CharField(max_length=50)),
                ('HolidayCelebrated', models.CharField(max_length=100)),
                ('Email', models.EmailField(max_length=254)),
                ('ShippingCity', models.CharField(max_length=100)),
                ('FindClients_visible', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Contactid', models.CharField(blank=True, max_length=100, null=True)),
                ('ContactName', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('InterestID', models.CharField(max_length=100, unique=True)),
                ('InterestName', models.CharField(max_length=100)),
                ('ApprovalStatus', models.CharField(choices=[('True', 'True'), ('False', 'False')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Productid', models.CharField(max_length=100, unique=True)),
                ('ProductName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OpportunityId', models.CharField(max_length=100, unique=True)),
                ('OpportunityName', models.CharField(max_length=100)),
                ('StageName', models.CharField(max_length=100)),
                ('Billing_City', models.CharField(max_length=100)),
                ('AverageitemSold', models.CharField(max_length=100)),
                ('AccountId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_app.account', to_field='Accountid')),
            ],
        ),
        migrations.CreateModel(
            name='Interest_Junction_c',
            fields=[
                ('InterestNameJunction', models.CharField(max_length=100)),
                ('InterestName', models.CharField(max_length=100)),
                ('InterestJunctionID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('link_With', models.CharField(choices=[('Account', 'Account'), ('Product', 'Product')], max_length=50)),
                ('Account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_app.account', to_field='Accountid')),
                ('Interest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_app.interest', to_field='InterestID')),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='my_app.product', to_field='Productid')),
            ],
        ),
    ]
