from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.models import GenericTaggedItemBase, TagBase


class MyTagGroup(TagBase):
    name = models.CharField(verbose_name=_("Name"), unique=True, max_length=100)
    slug = models.SlugField(verbose_name=_("Slug"), unique=True, max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")


class MyTag(TagBase):
    group = models.ForeignKey(
        MyTagGroup, on_delete=models.PROTECT, verbose_name=_("Group"), default=1
    )
    active = models.BooleanField(default=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    last_used = models.DateTimeField(
        null=True,
        blank=True,
        default=timezone.make_aware(timezone.datetime(2000, 1, 1, 00, 00)),
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tagged", args=[str(self.slug)])


class MyTaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(
        MyTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )
    published = models.DateTimeField(editable=False, null=True)
