# Generated by Django 4.1.1 on 2022-11-03 22:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tracking", "0003_alter_contributor_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contributor",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="contributors",
                to="tracking.project",
            ),
        ),
    ]
