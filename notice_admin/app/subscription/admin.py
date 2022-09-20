from django.contrib import admin
from .models import Subscription, UserSubscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'enabled', 'frequency')

    # Поиск по полям
    search_fields = ('name', )

    # Фильтрация в списке
    list_filter = ('enabled', )


@admin.register(UserSubscription)
class NoticeTriggerAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('user_id', 'enabled', 'subscription')

    # Поиск по полям
    search_fields = ('user_id', )

    # Фильтрация в списке
    list_filter = ('enabled', )
