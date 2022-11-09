# Generated by Django 3.2.5 on 2022-11-09 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0004_alter_contributor_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('back-end', 'back-end'), ('front-end', 'front-end'), ('iOS', 'iOS'), ('android', 'android')], default='back-end', max_length=10),
        ),
    ]