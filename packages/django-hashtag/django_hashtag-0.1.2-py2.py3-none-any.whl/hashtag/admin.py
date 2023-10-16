from django.contrib import admin
from taggit.admin import Tag

from .models import MyTag, MyTaggedItem, MyTagGroup

admin.site.unregister(Tag)


@admin.register(MyTagGroup)
class MyTagGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "active"]
    list_display_links = ["name"]
    ordering = (
        "active",
        "name",
        "slug",
    )
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ["name"]}


class TaggedItemInline(admin.StackedInline):
    model = MyTaggedItem


@admin.register(MyTag)
class MyTagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["group", "name", "active", "last_used", "count"]
    list_display_links = ("group", "name")
    list_filter = ("group", "active")
    ordering = (
        "-count",
        "-last_used",
        "active",
        "group",
        "name",
        "slug",
    )
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}
    readonly_fields = ["count", "last_used"]
