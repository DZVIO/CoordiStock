# Generated by Django 5.1.7 on 2025-03-30 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_activo_tipo_alter_activo_categoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activo',
            name='categoria',
            field=models.CharField(choices=[('PC', 'PC'), ('Laptop', 'Laptop'), ('Pantalla', 'Pantalla'), ('Diadema', 'Diadema'), ('Teclado', 'Teclado'), ('Mouse', 'Mouse'), ('Base Refrigerante', 'Base Refrigerante'), ('Speaker', 'Speaker')], max_length=50, verbose_name='Categoría'),
        ),
    ]
