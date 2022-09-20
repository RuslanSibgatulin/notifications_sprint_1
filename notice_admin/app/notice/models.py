import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        abstract = True


class NoticeMethod(UUIDMixin):

    class Meta:
        db_table = "notice_method"
        verbose_name = _('Method')
        verbose_name_plural = _('Methods')

    def __str__(self):
        return self.name


class NoticeTemplate(UUIDMixin, TimeStampedMixin):
    content = models.TextField(_('content'), help_text='Jinja template format')

    class Meta:
        db_table = "notice_template"
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return self.name


class NoticeTrigger(UUIDMixin):

    class Meta:
        db_table = "notice_trigger"
        verbose_name = _('Trigger')
        verbose_name_plural = _('Triggers')

    def __str__(self):
        return self.name


class Notice(UUIDMixin, TimeStampedMixin):
    description = models.TextField(_('description'), blank=True, null=True)
    template = models.ForeignKey(
        NoticeTemplate,
        on_delete=models.PROTECT,
        verbose_name=_('template'),
    )
    trigger = models.ForeignKey(
        NoticeTrigger,
        on_delete=models.PROTECT,
        verbose_name=_('trigger')
    )
    method = models.ForeignKey(
        NoticeMethod,
        verbose_name=_('method'),
        on_delete=models.PROTECT
    )
    enabled = models.BooleanField(_('enabled'))

    class Meta:
        db_table = "notice"
        verbose_name = _('Notice')
        verbose_name_plural = _('Notices')

    def __str__(self):
        return self.name
