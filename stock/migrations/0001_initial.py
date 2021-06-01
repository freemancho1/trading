# Generated by Django 3.2.3 on 2021-06-01 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acc_name', models.CharField(max_length=20, unique=True, verbose_name='Account Name')),
                ('t_type', models.CharField(max_length=4, verbose_name='Trading Type')),
                ('t_count', models.IntegerField(verbose_name='Trading Count')),
                ('base_money', models.FloatField(verbose_name='Base Money')),
                ('balance', models.FloatField(null=True, verbose_name='Current Balance')),
                ('ratio', models.FloatField(null=True, verbose_name='Ratio')),
                ('first_date', models.DateField(auto_now_add=True, verbose_name='First Trading Date')),
                ('last_date', models.DateField(auto_now=True, verbose_name='Last Trading Date')),
            ],
            options={
                'db_table': 'trading_stock_account',
                'ordering': ['t_type', 't_count'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('com_code', models.CharField(db_index=True, max_length=7, verbose_name='Company Code')),
                ('com_name', models.CharField(max_length=500, verbose_name='Company Name')),
                ('m_type', models.CharField(max_length=4, verbose_name='Market Type')),
                ('chg_date', models.DateField(auto_now=True, verbose_name='Change Date')),
                ('t_volume', models.FloatField(verbose_name='Number of Listed Stocks')),
                ('data_size', models.IntegerField(null=True, verbose_name='Data Size')),
            ],
            options={
                'db_table': 'trading_stock_company',
                'ordering': ['com_code'],
            },
        ),
        migrations.CreateModel(
            name='MarketData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Trading Date')),
                ('com_code', models.CharField(db_index=True, max_length=7, verbose_name='Company Code')),
                ('com_name', models.CharField(max_length=500, verbose_name='Company Name')),
                ('m_type', models.CharField(max_length=4, verbose_name='Market Type')),
                ('open', models.FloatField(verbose_name='Open Price')),
                ('low', models.FloatField(verbose_name='Low Price')),
                ('high', models.FloatField(verbose_name='High Price')),
                ('close', models.FloatField(verbose_name='Close Price')),
                ('diff', models.FloatField(verbose_name='Difference Price')),
                ('ratio', models.FloatField(verbose_name='Difference Ratio')),
                ('volume', models.FloatField(verbose_name='Volume')),
                ('value', models.FloatField(verbose_name='Trading Value')),
                ('t_volume', models.FloatField(verbose_name='Number of Listed Stocks')),
                ('t_value', models.FloatField(verbose_name='Total Value')),
            ],
            options={
                'db_table': 'trading_stock_marketdata',
                'ordering': ['-date', 'com_code'],
            },
        ),
        migrations.CreateModel(
            name='ModelInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100, verbose_name='Model Name')),
                ('com_code', models.CharField(default='000000', max_length=7, verbose_name='Company Code')),
                ('date', models.DateField(db_index=True, verbose_name='Training Date')),
                ('info', models.JSONField(default={}, verbose_name='Model Create Info')),
                ('model_path', models.CharField(max_length=300, verbose_name='Model File Path')),
                ('max_value', models.FloatField(null=True, verbose_name='Max Value')),
                ('accuracy', models.FloatField(null=True, verbose_name='Model Accuracy')),
            ],
            options={
                'db_table': 'trading_stock_modelinfo',
                'ordering': ['model_name', '-date'],
            },
        ),
        migrations.CreateModel(
            name='ModelingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Trading Date')),
                ('com_code', models.CharField(db_index=True, max_length=7, verbose_name='Company Code')),
                ('open', models.FloatField(verbose_name='Open Price')),
                ('low', models.FloatField(verbose_name='Low Price')),
                ('high', models.FloatField(verbose_name='High Price')),
                ('close', models.FloatField(verbose_name='Close Price')),
                ('volume', models.FloatField(verbose_name='Volume')),
            ],
            options={
                'db_table': 'trading_stock_modelingdata',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ModelingInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Modeling Date')),
                ('com_code', models.CharField(db_index=True, max_length=7, verbose_name='Company Code')),
                ('r_open', models.FloatField(null=True, verbose_name='Real Today Open Price')),
                ('r_close', models.FloatField(null=True, verbose_name='Real Today Close Price')),
                ('p_open', models.FloatField(null=True, verbose_name='Predict Open Price')),
                ('p_close', models.FloatField(null=True, verbose_name='Predict Close Price')),
                ('o_ratio', models.FloatField(null=True, verbose_name='Open Price Ratio')),
                ('c_ratio', models.FloatField(null=True, verbose_name='Close Price Ratio')),
                ('p_ratio', models.FloatField(null=True, verbose_name='Predict Open-Close Price Ratio')),
                ('accuracy', models.FloatField(null=True, verbose_name='Test Accuracy')),
            ],
            options={
                'db_table': 'trading_stock_modelinginfo',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='MyTrading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(db_index=True, verbose_name='Trading Date')),
                ('com_code', models.CharField(db_index=True, max_length=7, verbose_name='Company Code')),
                ('t_type', models.CharField(max_length=4, verbose_name='Trading Type')),
                ('t_count', models.IntegerField(verbose_name='Trading Count')),
                ('p_close', models.FloatField(null=True, verbose_name='Predict Close Price')),
                ('buy_price', models.FloatField(verbose_name='Buy Price')),
                ('sell_price', models.FloatField(verbose_name='Sell Price')),
                ('ratio', models.FloatField(verbose_name='Ratio')),
                ('volume', models.FloatField(verbose_name='Trading Volume')),
                ('profit', models.FloatField(verbose_name='Trading Profit')),
            ],
            options={
                'db_table': 'trading_stock_mytrading',
                'ordering': ['-date', 'com_code'],
            },
        ),
    ]