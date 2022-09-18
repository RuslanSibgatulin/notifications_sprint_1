from django.contrib import admin

from .models import NoticeTemplate, Notice, NoticeTrigger


@admin.register(NoticeTemplate)
class NoticeTemplateAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', )

    # Поиск по полям
    search_fields = ('name', )


@admin.register(NoticeTrigger)
class NoticeTriggerAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', )

    # Поиск по полям
    search_fields = ('name', )


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ('name', 'description', 'enabled')

    # Поиск по полям
    search_fields = ('id', 'name', 'description', )

    # Фильтрация в списке
    list_filter = ('trigger', 'enabled', )
