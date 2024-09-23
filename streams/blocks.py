"""StreamFields live in here."""

# wagtail.core is deprecated??? 

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

   #title = models.CharField - in blocks replace models with "blocks" and "Field" with "Block"
    title = blocks.CharBlock(required=True, help_text='Add your title') # This is Struct
    text = blocks.CharBlock(required=True, help_text='Add additional text') # This is Struct

    class Meta: # noqa
        template = "streams/title_and_text.html"
        icon = "edit"
        label = "Title & Text"

class CardBlock(blocks.StructBlock):
    """Cards with image and text and buttons"""

    title = blocks.CharBlock(required=True, help_text='Add your title') # This is Struct

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
              ("image", ImageChooserBlock(require=True)),
              ("title", blocks.CharBlock(required=True, max_length=40)),
              ("text", blocks.TextBlock(required=True, max_length=200)),
              ("button_page", blocks.PageChooserBlock(required=False)),
              ("button_url", blocks.URLBlock(required=False, help_text="If page is not selected above"))
            ]
        )
    )

    class Meta: # noqa
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Boss Cards"

class RichTextBlock(blocks.RichTextBlock):
    """Richtext with all the features."""
    # No Struct just RichText Block
    class Meta: # noqa
        template = "streams/richtext_block.html"
        icon = "doc-full"
        label = "Full RichText"

class SimpleRichTextBlock(blocks.RichTextBlock):
    """Richtext without (limited) all the features."""
    # No Struct just RichText Block
    # Overriding  class in .\env\Lib\site-packages\wagtail\blocks\field_block.py
    def __init__(self, required=True, help_text=None, editor="default", features=None, max_length=None, validators=(), search_index=True, **kwargs,):
        super().__init__(**kwargs)
        self.features = [
            "bold",
            "italic",
            "link",
        ]

    class Meta: # noqa
        template = "streams/richtext_block.html"
        icon = "edit"
        label = "Simple RichText"

class CTABlock(blocks.StructBlock):
    """A simple call to action section"""

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, max_length=400, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(required=True, default="Learn More", max_length=40)

    class Meta: # noqa
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to Action"

class LinkStructValue(blocks.StructValue):
    """Additional logic for our URL"""
    
    # Technically more efficient than have logic in HTMl template
    # no extra parsing from html to python
    
    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        
        if button_page:
            return button_page.url
        elif button_url:
            return button_url
        
        return None

      
class ButtonBlock(blocks.StructBlock):
    """Add external or internal URL"""
    
    button_page = blocks.PageChooserBlock(required=False, help_text="If selected this url will be used first")
    button_url = blocks.URLBlock(required=False, help_text="This url will be used secondary")
    
    class Meta: # noqa
        template = "streams/button_block.html"
        icon = "edit"
        label = "Single Button"
        value_class = LinkStructValue
    