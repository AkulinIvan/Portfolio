from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from .models import (
    Technology, Skill, Experience, 
    Education, PersonalInfo
)





# ========== CUSTOM FILTERS ==========
class CategoryFilter(SimpleListFilter):
    """Кастомный фильтр по категориям"""
    title = 'Категория'
    parameter_name = 'category'
    
    def lookups(self, request, model_admin):
        return model_admin.model.CATEGORY_CHOICES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category=self.value())


class LevelFilter(SimpleListFilter):
    """Кастомный фильтр по уровню владения"""
    title = 'Уровень владения'
    parameter_name = 'level'
    
    def lookups(self, request, model_admin):
        return model_admin.model.LEVEL_CHOICES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(level=self.value())


class ProjectTypeFilter(SimpleListFilter):
    """Кастомный фильтр по типу проекта"""
    title = 'Тип проекта'
    parameter_name = 'project_type'
    
    def lookups(self, request, model_admin):
        return model_admin.model.PROJECT_TYPES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project_type=self.value())


class IsActiveFilter(SimpleListFilter):
    """Фильтр активности"""
    title = 'Активность'
    parameter_name = 'is_active'
    
    def lookups(self, request, model_admin):
        return (
            ('1', 'Активные'),
            ('0', 'Неактивные'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(is_active=True)
        elif self.value() == '0':
            return queryset.filter(is_active=False)


# ========== CUSTOM ACTIONS ==========
@admin.action(description='Активировать выбранные')
def activate_technologies(modeladmin, request, queryset):
    queryset.update(is_active=True)
    modeladmin.message_user(request, f'{queryset.count()} технологий активировано')


@admin.action(description='Деактивировать выбранные')
def deactivate_technologies(modeladmin, request, queryset):
    queryset.update(is_active=False)
    modeladmin.message_user(request, f'{queryset.count()} технологий деактивировано')


@admin.action(description='Сделать избранными')
def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)
    modeladmin.message_user(request, f'{queryset.count()} проектов добавлено в избранное')


@admin.action(description='Убрать из избранного')
def remove_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)
    modeladmin.message_user(request, f'{queryset.count()} проектов убрано из избранного')


# ========== TECHNOLOGY ADMIN ==========
@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Админка для технологий"""
    list_display = [
        'name', 
        'category_display', 
        'level_display', 
        'projects_count', 
        'is_active_icon',
        'order',
        'updated_at'
    ]
    list_display_links = ['name']
    list_filter = [CategoryFilter, LevelFilter, IsActiveFilter, 'created_at']
    search_fields = ['name', 'description', 'icon_class']
    list_editable = ['order']
    list_per_page = 25
    actions = [activate_technologies, deactivate_technologies]
    
    # ОБНОВЛЕННЫЙ FIELDSETS - УБРАЛИ SLUG
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name', 
                # 'slug',  # Убрали отсюда
                'category', 
                'level',
                'description'
            )
        }),
        ('Визуальное отображение', {
            'fields': (
                'icon_class', 
                'icon_color', 
                'bg_color',
                'icon_preview'
            ),
            'classes': ('collapse', 'wide')
        }),
        ('Дополнительная информация', {
            'fields': (
                'experience_years',
                'last_used',
                'order',
                'is_active'
            )
        }),
        ('Метаданные', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'created_at', 
        'updated_at',
        'icon_preview'
    ]
    
    
    
    # Кастомные методы для отображения в списке
    def category_display(self, obj):
        return obj.get_category_display()
    category_display.short_description = 'Категория'
    category_display.admin_order_field = 'category'
    
    def level_display(self, obj):
        stars = '★' * obj.level + '☆' * (5 - obj.level)
        return stars
    level_display.short_description = 'Уровень'
    level_display.admin_order_field = 'level'
    
    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Проектов'
    projects_count.admin_order_field = '_projects_count'
    
    def is_active_icon(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: green;">✓</span> Активна')
        return mark_safe('<span style="color: red;">✗</span> Неактивна')
    is_active_icon.short_description = 'Статус'
    is_active_icon.admin_order_field = 'is_active'
    
    def icon_preview(self, obj):
        if obj.icon_class:
            return format_html(
                '<div style="display: inline-flex; align-items: center; gap: 10px; padding: 10px; '
                'background-color: {}; border-radius: 5px;">'
                '<i class="bi {}" style="font-size: 24px; color: {};"></i>'
                '<span style="font-family: monospace;">{}</span>'
                '</div>',
                obj.bg_color or '#e9f0e8',
                obj.icon_class,
                obj.icon_color or '#3a6656',
                obj.icon_class
            )
        return "Иконка не указана"
    icon_preview.short_description = 'Предпросмотр иконки'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_projects_count=Count('projects'))
        return queryset




# ========== SKILL ADMIN ==========
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """Админка для навыков"""
    list_display = [
        'name',
        'category_display',
        'technology_link',
        'proficiency_bar',
        'order'
    ]
    list_display_links = ['name']
    list_filter = ['category', 'technology']
    search_fields = ['name', 'description', 'technology__name']
    list_editable = ['order']
    list_per_page = 30
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'name',
                'category',
                'technology',
                'description'
            )
        }),
        ('Уровень владения', {
            'fields': (
                'proficiency',
                'proficiency_display'
            )
        }),
        ('Визуальное отображение', {
            'fields': (
                'icon',
                'order'
            )
        }),
    )
    
    readonly_fields = ['proficiency_display']
    
    # Кастомные методы для отображения
    def category_display(self, obj):
        category_icons = {
            'backend': '⚙️',
            'frontend': '🎨',
            'devops': '🚀',
            'database': '🗄️',
            'other': '📦'
        }
        icon = category_icons.get(obj.category, '📦')
        return f"{icon} {obj.get_category_display()}"
    category_display.short_description = 'Категория'
    category_display.admin_order_field = 'category'
    
    def technology_link(self, obj):
        if obj.technology:
            url = f"/admin/core/technology/{obj.technology.id}/change/"
            return format_html(
                '<a href="{}">{}</a>',
                url,
                obj.technology.name
            )
        return "—"
    technology_link.short_description = 'Технология'
    technology_link.admin_order_field = 'technology__name'
    
    def proficiency_bar(self, obj):
        color = "#28a745" if obj.proficiency >= 70 else \
                "#17a2b8" if obj.proficiency >= 50 else \
                "#ffc107" if obj.proficiency >= 30 else \
                "#dc3545"
        
        return format_html(
            '<div style="display: flex; align-items: center; gap: 10px;">'
            '<div style="width: 100px; background: #e9ecef; border-radius: 3px; overflow: hidden;">'
            '<div style="width: {}%; height: 20px; background: {};"></div>'
            '</div>'
            '<span>{}%</span>'
            '</div>',
            obj.proficiency,
            color,
            obj.proficiency
        )
    proficiency_bar.short_description = 'Уровень'
    proficiency_bar.admin_order_field = 'proficiency'


# ========== EXPERIENCE ADMIN ==========
@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """Админка для опыта работы"""
    list_display = [
        'title',
        'company',
        'duration',
        'current_display',
        'technologies'
    ]
    list_display_links = ['title']
    list_filter = ['current', 'start_date']
    search_fields = ['title', 'company', 'description', 'technologies']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Информация о работе', {
            'fields': (
                'title',
                'company',
                'start_date',
                'end_date',
                'current'
            )
        }),
        ('Детали', {
            'fields': (
                'description',
                'technologies'
            )
        }),
    )
    
    # Кастомные методы для отображения
    def duration(self, obj):
        return obj.duration_display()
    duration.short_description = 'Период работы'
    
    def current_display(self, obj):
        if obj.current:
            return mark_safe('<span style="color: green;">✓</span> Текущая')
        return ""
    current_display.short_description = 'Статус'
    current_display.admin_order_field = 'current'


# ========== EDUCATION ADMIN ==========
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """Админка для образования"""
    list_display = [
        'institution',
        'faculty',
        'years',
        'description_short'
    ]
    list_display_links = ['institution']
    search_fields = ['institution', 'faculty', 'description']
    
    fieldsets = (
        ('Основная информация', {
            'fields': (
                'institution',
                'faculty',
                'start_year',
                'end_year'
            )
        }),
        ('Дополнительно', {
            'fields': (
                'description',
            )
        }),
    )
    
    # Кастомные методы для отображения
    def years(self, obj):
        return f"{obj.start_year} - {obj.end_year}"
    years.short_description = 'Годы обучения'
    years.admin_order_field = 'end_year'
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description
        return ""
    description_short.short_description = 'Описание'


# ========== PERSONAL INFO ADMIN ==========
@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    """Админка для персональной информации"""
    list_display = [
        'name',
        'title',
        'email',
        'location'
    ]
    list_display_links = ['name']
    search_fields = ['name', 'title', 'email', 'location']
    
    fieldsets = (
        ('Персональные данные', {
            'fields': (
                'name',
                'title',
                'about'
            )
        }),
        ('Контакты', {
            'fields': (
                'email',
                'phone',
                'location'
            )
        }),
        ('Социальные сети', {
            'fields': (
                'linkedin',
                'github',
                'telegram'
            )
        }),
    )
    
    def has_add_permission(self, request):
        # Разрешаем создание только одной записи
        return not PersonalInfo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление, если это единственная запись
        count = PersonalInfo.objects.count()
        if count == 1:
            return False
        return super().has_delete_permission(request, obj)


# ========== ADMIN SITE CUSTOMIZATION ==========
# Кастомизация админ-сайта
admin.site.site_header = "Администрирование портфолио"
admin.site.site_title = "Портфолио"
admin.site.index_title = "Управление контентом портфолио"

# Группировка моделей в админке
def get_app_list(self, request, app_label=None):
    """
    Переопределение порядка приложений в админке
    """
    app_dict = self._build_app_dict(request, app_label)
    
    # Список приложений в нужном порядке
    custom_order = [
        'core',  # Основное приложение
        'auth',  # Пользователи и группы
    ]
    
    app_list = []
    
    for app_name in custom_order:
        if app_name in app_dict:
            app_list.append(app_dict[app_name])
    
    # Добавляем остальные приложения
    for app_name, app in app_dict.items():
        if app_name not in custom_order:
            app_list.append(app)
    
    return app_list

# Применяем кастомизацию
admin.AdminSite.get_app_list = get_app_list