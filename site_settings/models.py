from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import register_setting, BaseGenericSetting

# What is decorator???????????????????? "@decorate_name"
@register_setting
class SocialMediaSettings(BaseGenericSetting):
    """Social media settings for our website"""

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube URL")

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("youtube")
        ], heading="Social Media Settings")
    ]