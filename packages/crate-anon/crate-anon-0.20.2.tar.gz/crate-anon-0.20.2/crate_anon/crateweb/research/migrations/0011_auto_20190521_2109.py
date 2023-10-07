# Generated by Django 2.1.7 on 2019-05-21 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("research", "0010_query_last_run"),
    ]

    operations = [
        migrations.AddField(
            model_name="query",
            name="formatted_sql",
            field=models.TextField(
                default=None,
                null=True,
                verbose_name="SQL with highlighting and formatting",
            ),  # noqa
        ),
        migrations.AddField(
            model_name="sitewidequery",
            name="formatted_sql",
            field=models.TextField(
                default=None,
                null=True,
                verbose_name="SQL with highlighting and formatting",
            ),  # noqa
        ),
    ]
