from base.mixins import TimeStampedMixin, UUIDMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from notice.models import NoticeTemplate


class SubscriptionFrequency(models.TextChoices):
    DAYLY = 'dayly', _('dayly')
    WEEKLY = 'weekly', _('weekly')
    MONTHLY = 'monthly', _('monthly')
    YEARLY = 'yearly', _('yearly')


class Subscription(UUIDMixin, TimeStampedMixin):
    enabled = models.BooleanField(_('enabled'))
    auto = models.BooleanField(_('auto subscription'))
    template = models.ForeignKey(
        NoticeTemplate,
        on_delete=models.PROTECT,
        verbose_name=_('template'),
    )
    frequency = models.CharField(
        _('frequency'), max_length=50,
        choices=SubscriptionFrequency.choices
    )

    class Meta:
        db_table = "notice_subscription"
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

    def __str__(self):
        return self.name


class UserSubscription(TimeStampedMixin):
    user_id = models.UUIDField(editable=False)
    enabled = models.BooleanField(_('enabled'))
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.PROTECT,
        verbose_name=_('subscription'),
    )

    class Meta:
        db_table = "notice_user_subscription"
        verbose_name = _('user subscription')
        verbose_name_plural = _('users subscriptions')
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'subscription'],
                name='user_subscription_idx')
        ]

    def __str__(self):
        return self.name
