# Generated by Django 4.2.5 on 2023-10-01 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredientes', '0003_pregunta_creado_por_pregunta_top_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='estado',
            field=models.CharField(choices=[('respondida', 'Respondida'), ('no respondida', 'No Respondida')], default='No Respondida', max_length=100),
        ),
    ]
