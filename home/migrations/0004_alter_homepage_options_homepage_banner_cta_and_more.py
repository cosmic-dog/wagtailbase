# Generated by Django 5.0.2 on 2024-09-09 11:14

import django.db.models.deletion
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_banner_title'),
        ('wagtailcore', '0091_remove_revision_submitted_for_moderation'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': 'Child Page New', 'verbose_name_plural': 'Child Pages'},
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_cta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='banner_subtitle',
            field=wagtail.fields.RichTextField(default='Text text'),
            preserve_default=False,
        ),
    ]
