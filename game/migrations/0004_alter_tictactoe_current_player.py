# Generated by Django 4.1.1 on 2023-06-09 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_alter_tictactoe_current_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tictactoe',
            name='current_player',
            field=models.CharField(default='X', max_length=1),
        ),
    ]