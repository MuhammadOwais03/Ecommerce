# Generated by Django 4.2.3 on 2023-09-25 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(default='shoes', max_length=200, null=True),
        ),
    ]
