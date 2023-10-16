from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditModelMixin(models.Model):
    """
    Mixin that provides fields created and modified at and by fields
    """

    UserModel = get_user_model()
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    created_by = models.ForeignKey(
        UserModel,
        verbose_name=_("Created By"),
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
    )
    modified = models.DateTimeField(_("Modified"), blank=True, null=True)
    modified_by = models.ForeignKey(
        UserModel,
        blank=True,
        null=True,
        verbose_name=_("Modified By"),
        on_delete=models.CASCADE,
        related_name="%(class)s_modified_by",
    )

    class Meta:
        abstract = True


class PublishModelMixin(models.Model):
    """
    Mixin that provides fields publish at and by fields
    """

    UserModel = get_user_model()
    publish = models.DateTimeField(_("Published"), blank=True, null=True)
    publish_by = models.ForeignKey(
        UserModel,
        blank=True,
        null=True,
        verbose_name=_("Published By"),
        on_delete=models.CASCADE,
        related_name="%(class)s_publish_by",
    )
    published = models.BooleanField(_("Publish"), default=False)

    class Meta:
        abstract = True
