from django.db import models
from wagtail.models import Page
from wagtail.admin.panels  import FieldPanel
from wagtail.fields import StreamField
from streams import blocks

class FlexPage(Page):
    """Flexible page"""

    template = "flex/flex_page.html"

    content = StreamField(
        [ # Wagtail use this name and renaming is bad, thing before naming
            ("title_and_text", blocks.TitleAndTextBlock()), 
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True
    )

    subtitle = models.CharField(max_length=100, null=True, blank=True)

    content_panels= Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("content")
    ]

    class Meta: # noqa
        verbose_name = "Flex Page"
        verbose_name_plural = "Flex Pages"
