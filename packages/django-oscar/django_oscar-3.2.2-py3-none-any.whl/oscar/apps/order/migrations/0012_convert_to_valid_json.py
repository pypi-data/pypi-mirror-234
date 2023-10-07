# Generated by Django 3.2.15 on 2022-09-28 15:06
import json
from ast import literal_eval

from django.db import migrations
from django.core.serializers.json import DjangoJSONEncoder


def forward(apps, schema_editor):
    LineAttribute = apps.get_model("order", "LineAttribute")
    for at in LineAttribute.objects.all():
        try:  # if the value is allready valid json, continue
            json.loads(at.value)
            continue
        except json.JSONDecodeError:
            pass

        try:  # to parse the string a python, then convert to json, then continue
            val = literal_eval(at.value)
            at.value = json.dumps(val, cls=DjangoJSONEncoder)
            at.save()
            continue
        except (ValueError, SyntaxError):
            pass

        # convert the string to json as it is
        at.value = json.dumps(at.value)
        at.save()


class Migration(migrations.Migration):

    replaces = [
        ('order', '0012_json_option_value')
    ]

    dependencies = [
        ('order', '0011_auto_20200801_0817'),
    ]

    operations = [
        migrations.RunPython(forward, migrations.RunPython.noop),
    ]
