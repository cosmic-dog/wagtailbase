from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, PageChooserPanel
from streams import blocks


# Admin.Panels PageChooserPanel and ImageChooserPanel are deprecated use FieldPanel instead

class HomePage(Page):
    """Home page model."""

    template = "home/home_page.html"
    max_count = 1   # Limit number of child pages

    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"])
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, # If migration exist and no value yet
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content = StreamField(
        [ # Wagtail use this name and renaming is bad, thing before naming
            ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("banner_title"),
        FieldPanel("banner_subtitle"),
        FieldPanel("banner_image"),
        FieldPanel("banner_cta"),
        FieldPanel("content")
    ]

    class Meta:

        verbose_name = "Child Page New"
        verbose_name_plural = "Child Pages"