# Generated by Django 4.2 on 2023-04-17 08:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("yt2m", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="download",
            options={"ordering": ("-created_at",)},
        ),
        migrations.AddIndex(
            model_name="download",
            index=models.Index(
                fields=["created_at"], name="yt2m_downlo_created_b09532_idx"
            ),
        ),
    ]
