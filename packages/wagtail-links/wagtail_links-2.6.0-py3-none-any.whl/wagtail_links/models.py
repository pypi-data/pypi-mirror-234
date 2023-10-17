from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse, NoReverseMatch
from wagtail.admin.panels import PageChooserPanel, FieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from .fields import NullSlugField
import logging

logger = logging.getLogger(__name__)


def validate_django_reverse(view_name):
    try:
        reverse(view_name)
    except NoReverseMatch:
        # Translators: CMS error message
        raise ValidationError(_("Invalid Django view name"))


class LinkManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


@register_snippet
class Link(index.Indexed, models.Model):
    """
    A generic link that points somewhere else using various methods
    """

    title = models.CharField(
        _("Title"),
        max_length=200,
        blank=True,
        help_text=_("Description of link for use in ARIA compliance"),
    )
    name = NullSlugField(
        _("Name"),
        unique=True,
        help_text=_("Unique name for this link (for use by Django templates)."),
    )
    link_external = models.URLField(
        _("External Link"), blank=True, help_text=_("Absolute URL Link")
    )
    link_relative = models.CharField(
        _("Relative Link"),
        max_length=200,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^(?!www\.|(?:http|ftp)s?://|[A-Za-z]:\\|//).*",
                message="Not valid relative url",
            )
        ],
        help_text=_("Relative URL Link"),
    )
    link_page = models.ForeignKey(
        "wagtailcore.Page",
        verbose_name=_("Wagtail Page Link"),
        null=True,
        blank=True,
        related_name="+",
        on_delete=models.CASCADE,
        help_text=_("Wagtail Page Link"),
    )
    django_view_name = models.CharField(
        _("Django View Link"),
        max_length=255,
        blank=True,
        validators=[validate_django_reverse],
        help_text=_("Name of Django view for reverse lookup"),
    )

    objects = LinkManager()

    panels = [
        FieldPanel("title"),
        FieldPanel("name"),
        FieldPanel("link_external"),
        FieldPanel("link_relative"),
        PageChooserPanel("link_page"),
        FieldPanel("django_view_name"),
    ]

    search_fields = [
        index.RelatedFields(
            "link_page", [index.SearchField("title", partial_match=True)]
        ),
        index.SearchField("title", partial_match=True),
    ]

    class Meta:
        # Translators: Internal Model Name (singular)
        verbose_name = _("Link")
        # Translators: Internal Model Name (plural)
        verbose_name_plural = _("Links")

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        url = self.url
        if not url:
            url = _("No Link URL")
        ctx = {
            "name": self.name,
            "link_external": self.link_external,
            "link_relative": self.link_relative,
            "link_page": self.link_page,
            "django_view_name": self.django_view_name,
            "url": url,
        }
        if self.name:
            return _("Link[name=%(name)s]: %(url)s") % ctx
        if self.link_external:
            return _("Link[link_external=%(link_external)s]: %(url)s") % ctx
        if self.link_relative:
            return _("Link[link_relative=%(link_relative)s]: %(url)s") % ctx
        if self.link_page:
            return _("Link[link_page=%(link_page)s]: %(url)s") % ctx
        return _("Link[django_view_name=%(django_view_name)s]: %(url)s") % ctx

    @property
    def url(self):
        """Get URL for use in template"""
        # 1. External Links
        if self.link_external:
            return self.link_external
        # 2. Relative Links
        if self.link_relative:
            return self.link_relative
        # 3. Wagtail Page Links
        if self.link_page:
            url = self.link_page.url
            if url is None:
                return ""
            return url
        # 4. Django View Links
        try:
            return reverse(self.django_view_name)
        except NoReverseMatch:
            logger.warning("Unable to reverse Django URL for Link[id=%s]", self.id)
        # 5. Error Fallback
        return ""

    def clean(self):
        # Don't allow multiple link types to be used
        number_used = (
            bool(self.link_external)
            + bool(self.link_relative)
            + bool(self.link_page)
            + bool(self.django_view_name)
        )
        if number_used > 1:
            raise ValidationError(_("You may only use one link type"))
        if number_used == 0:
            raise ValidationError(_("You must use exactly one link type"))
