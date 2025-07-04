# Generated by Django 3.0 on 2024-06-03 04:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0004_auto_20240602_2115'),
    ]

    operations = [
        migrations.RenameField(
            model_name='admin',
            old_name='address',
            new_name='adminaddress',
        ),
        migrations.RenameField(
            model_name='admin',
            old_name='full_name',
            new_name='adminfullname',
        ),
        migrations.RenameField(
            model_name='admin',
            old_name='image',
            new_name='adminimage',
        ),
        migrations.RenameField(
            model_name='admin',
            old_name='mobile',
            new_name='adminmobile',
        ),
        migrations.RenameField(
            model_name='admin',
            old_name='is_staff',
            new_name='is_employee',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='slug',
            new_name='categoryslug',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='categorytitle',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='address',
            new_name='customeraddress',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='full_name',
            new_name='customerfullname',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='mobile',
            new_name='customermobile',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='ostatus',
            new_name='ostatus',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='productorderedby',
            new_name='productorderedby',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='shipping_address',
            new_name='productshippingaddress',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='category',
            new_name='categoryname',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='productdescription',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='productprice',
            new_name='productprice',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='slug',
            new_name='productslug',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='producttitle',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='joined_on',
        ),
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
    ]
