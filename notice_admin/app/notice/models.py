from base.mixins import TimeStampedMixin, UUIDMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class NoticeMethod(models.TextChoices):
    EMAIL = 'email'
    PUSH = 'push'
    SMS = 'sms'


class NoticeTemplate(UUIDMixin, TimeStampedMixin):
    content = models.TextField(_('content'), help_text='Jinja template format')

    class Meta:
        db_table = "notice_template"
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')

    def __str__(self):
        return self.name


class NoticeTrigger(UUIDMixin):
    """Модель будет содержать Kafka-топик - источник событий
    """

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
    method = models.CharField(
        _('method'), max_length=50,
        choices=NoticeMethod.choices
    )
    enabled = models.BooleanField(_('enabled'))

    class Meta:
        db_table = "notice"
        verbose_name = _('Notice')
        verbose_name_plural = _('Notices')

    def __str__(self):
        return self.name
