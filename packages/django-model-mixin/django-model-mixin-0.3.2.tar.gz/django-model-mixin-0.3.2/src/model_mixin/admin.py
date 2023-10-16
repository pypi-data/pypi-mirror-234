from django.contrib import admin, messages
from django.contrib.auth import get_permission_codename
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


# TODO: check if update can be managed by save_model or clear cache key directly
class ModelAdminPublishFieldsMixin(admin.ModelAdmin):
    """Custom model mixin for Publish Date and Publish By information"""

    actions = ["make_published", "make_unpublished"]

    @admin.action(
        permissions=["publish"], description=_("Mark selected object as published")
    )
    def make_published(self, request, queryset):
        """Action to update selected object as published"""
        updated = queryset.update(published=True)
        self.message_user(
            request,
            ngettext(
                "%d object was successfully marked as published.",
                "%d objects were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def has_publish_permission(self, request):
        """Does the user have the publish permission?"""
        opts = self.opts
        codename = get_permission_codename("publish", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    @admin.action(
        permissions=["unpublish"], description=_("Mark selected object as unpublished")
    )
    def make_unpublished(self, request, queryset):
        """Action to update selected object as unpublished"""
        updated = queryset.update(published=False)
        self.message_user(
            request,
            ngettext(
                "%d object was successfully marked as unpublished.",
                "%d objects were successfully marked as unpublished.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    def has_unpublish_permission(self, request):
        """Does the user have the unpublish permission?"""
        opts = self.opts
        codename = get_permission_codename("unpublish", opts)
        return request.user.has_perm(f"{opts.app_label}.{codename}")

    def save_model(self, request, obj, form, change) -> None:
        """Update publish fields from request object before save."""
        current_now = timezone.now()
        if obj.published and not obj.publish:
            obj.publish = current_now
            obj.publish_by = request.user
        if not obj.published and obj.publish:
            obj.publish = None
            obj.publish_by = None
        super().save_model(request, obj, form, change)


class ModelAdminAuditFieldsMixin(admin.ModelAdmin):
    """Custom model mixin for Create/Modify Date and Create/Modify By information"""

    def save_model(self, request, obj, form, change) -> None:
        """Update audit fields from request object before save."""
        current_now = timezone.now()
        if not change:
            obj.created = current_now
            obj.created_by = request.user
        else:
            obj.modified = current_now
            obj.modified_by = request.user
        super().save_model(request, obj, form, change)
