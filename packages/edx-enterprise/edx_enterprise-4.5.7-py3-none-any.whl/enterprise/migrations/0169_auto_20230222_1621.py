# Generated by Django 3.2.17 on 2023-02-21 18:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0168_auto_20230222_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licensedenterprisecourseenrollment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
        ),
        migrations.AlterField(
            model_name='historicallearnercreditenterprisecourseenrollment',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='historicallicensedenterprisecourseenrollment',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
        migrations.AlterField(
            model_name='learnercreditenterprisecourseenrollment',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
