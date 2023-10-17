from django.core.exceptions import ValidationError
from django.template import Context, Template
from wagtail.test.utils import WagtailPageTests
from wagtail.models import Page
from unittest.mock import patch
from .models import Link


class WagtailLinksTest(WagtailPageTests):
    def test_get_link(self):
        link = Link.objects.create(link_external="https://example.com")
        self.assertEqual(link.url, "https://example.com")

        link = Link.objects.create(link_relative="/example.com")
        self.assertEqual(link.url, "/example.com")

        page = Page.objects.first()
        link = Link.objects.create(link_page=page)
        self.assertEqual(link.url, "")

        link = Link.objects.create(django_view_name="admin:index")
        self.assertEqual(link.url, "/admin/")

    def test_link_validation(self):
        link = Link(
            link_external="https://example.com",
            link_relative="/foo",
        )
        with self.assertRaises(ValidationError):
            link.clean()

        link = Link()
        with self.assertRaises(ValidationError):
            link.clean()

        link = Link(django_view_name="doesnotexist")
        with self.assertRaises(ValidationError):
            link.full_clean()

    @patch("wagtail_links.models.logger")
    def test_log_broken_links(self, mock_logger):
        link = Link.objects.create(django_view_name="doesnotexist")
        link.url
        mock_logger.warning.assert_called_with(
            "Unable to reverse Django URL for Link[id=%s]", link.pk
        )

    def test_cast_link_to_string(self):
        link = Link.objects.create(name="example", link_external="https://example.com")
        self.assertEqual("{}".format(link), "Link[name=example]: https://example.com")

        link = Link.objects.create(link_external="https://example.com")
        self.assertEqual(
            "{}".format(link),
            "Link[link_external=https://example.com]: https://example.com",
        )

        link = Link.objects.create(link_relative="/example.com")
        self.assertEqual(
            "{}".format(link), "Link[link_relative=/example.com]: /example.com"
        )

        page = Page.objects.first()
        link = Link.objects.create(link_page=page)
        self.assertEqual("{}".format(link), "Link[link_page=Root]: No Link URL")

        link = Link.objects.create(django_view_name="admin:index")
        self.assertEqual(
            "{}".format(link), "Link[django_view_name=admin:index]: /admin/"
        )

    def test_multiple_blank_link_names(self):
        link1 = Link.objects.create(name="", link_external="https://example.com/1")
        link2 = Link.objects.create(name="", link_external="https://example.com/2")
        self.assertEqual(link1.name, "")
        self.assertEqual(link2.name, "")


class WagtailLinksTagsTest(WagtailPageTests):
    def test_get_wagtail_link(self):
        Link.objects.create(name="example", link_external="https://example.com")
        context = Context({})
        template = Template(
            """
            {% load wagtail_links %}
            {% get_wagtail_link 'example' as my_link %}
            <a href="{{ my_link.url }}">Testing</a>
            """
        )
        rendered_template = template.render(context)
        self.assertInHTML(
            '<a href="https://example.com">Testing</a>', rendered_template
        )

    def test_get_wagtail_link_url(self):
        Link.objects.create(name="example", link_external="https://example.com/test2/")
        context = Context({})
        template = Template(
            """
            {% load wagtail_links %}
            <a href="{% get_wagtail_link_url 'example' %}">Testing</a>
            """
        )
        rendered_template = template.render(context)
        self.assertInHTML(
            '<a href="https://example.com/test2/">Testing</a>', rendered_template
        )
