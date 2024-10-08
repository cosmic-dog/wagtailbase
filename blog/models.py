"""Blog listing and Blog detail pages."""
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.fields import StreamField
from streams import blocks
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet


# Orderable -----
class BlogAuthorOrderable(Orderable):
    """This allows us select author/s to blog post from snippets."""
    
    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE
    )
    
    panels = [
        FieldPanel("author"),
    ]


# Snippets -----
# Snippets are for reusable admin code and possibility to edit from Wagtail admin
# Like Authors
class BlogAuthor(models.Model):
    """Blog author snippets for Wagtail admin."""
    
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL
    )
    
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                FieldPanel("image")
            ],
            heading="Name and Image"
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )    
    ]
    
    def __str__(self):
        """String repr of this class"""
        return self.name
    
    class Meta: # noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog snipper for blog category."""
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text="A slug to identify post by this category",
    )
    
    panels = [
        FieldPanel("name"),
        FieldPanel("slug")
    ]

    def __str__(self):
        """String repr of this class"""
        return self.name
    
    class Meta: # noqa
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]
        
register_snippet(BlogCategory) 

# Pages -----
class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all Blog detail pages."""

    template = "blog/blog_listing_page.html"

    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text="Overwrite the default title")

    content_panels= Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""

        context = super().get_context(request, *args, **kwargs)
        
        all_posts = BlogDetailPage.objects.live().public().order_by('-first_published_at')
        paginator = Paginator(all_posts, 1) 
        page = request.GET.get("page")  # returns page number - Integer
                                        # getting ?page= URL Query
        
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            
        context["posts"] = posts
            
        context["one_to_two"] = "Form one definition to another in one class"
        context["a_special_link"] = self.reverse_subpage('latest_posts')
        context["categories"] = BlogCategory.objects.all()
        return context
    
    # '?' makes in regex last symbol '/' optional
    @route(r'^latest/?$', name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["posts"] = context["posts"][:1]
        return render(request, "blog/latest_posts.html", context)
    
    def get_sitemap_urls(self, request):
        # uncomment to have no sitemap for this page
        # return []
        
        sitemap = super().get_sitemap_urls(request)
        sitemap.append(
            { # Json file structure is called Dictionary in Python
                "location": self.full_url + self.reverse_subpage("latest_posts"),
                "lastmod": (self.last_published_at or self.latest_revision_created_at),
                "priority": 0.9,
            }
        )
        return sitemap

class BlogDetailPage(Page):
    """Parent blog detail page."""

    template = "blog/blog_detail_page.html"

    custom_title = models.CharField(max_length=100, blank=False, null=False, help_text="Blog title")
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    blog_content = StreamField(
        [ 
            ("title_and_text", blocks.TitleAndTextBlock()), 
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock())
        ],
        null=True,
        blank=True,
    )

    content_panels= Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("banner_image"),
        MultiFieldPanel(
            [
                InlinePanel("blog_authors", label="Author", min_num=1, max_num=4),
                
            ],
            heading="Author(s)"
        ),
        MultiFieldPanel(
            [
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
            ],
            heading="Categories"
        ),
        FieldPanel("blog_content"),
    ]


# First subclassed blog post page -----
# Or child page of BlogDetailPage
# BlogDetailPage.objects.live().exact_type(BlogDetailPage) - to get exact type of specific class
# BlogDetailPage.objects.live().not_exact_type(BlogDetailPage) - to get other classes which are not exact type
# BlogDetailPage.objects.live().not_exact_type(BlogDetailPage).specific(defer=True)
class ArticleBlogPage(BlogDetailPage):
    """A subclassed blog post page for articles."""
    
    template = "blog/article_blog_page.html"
    
    # To get Specific property from Subclass use .specific <-( Wagtail way to get subclass property)
    # .specific is adding extra DB queries, so be careful
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text='Best size for this image is 1400x400'
    )
    
    content_panels = BlogDetailPage.content_panels + [
         MultiFieldPanel(
            [
                FieldPanel("subtitle"),
                FieldPanel("intro_image")
            ],
            heading="Article panels"
        ),
    ]