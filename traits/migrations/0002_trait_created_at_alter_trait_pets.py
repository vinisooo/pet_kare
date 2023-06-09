# Generated by Django 4.2 on 2023-04-04 02:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0002_alter_pet_group"),
        ("traits", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trait",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="trait",
            name="pets",
            field=models.ManyToManyField(related_name="traits", to="pets.pet"),
        ),
    ]
