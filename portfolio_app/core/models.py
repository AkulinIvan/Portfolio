from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Technology(models.Model):
    """Модель для технологий и инструментов"""
    
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('database', 'Базы данных'),
        ('devops', 'DevOps'),
        ('mobile', 'Мобильная разработка'),
        ('cloud', 'Облачные технологии'),
        ('other', 'Другое'),
    ]
    
    LEVEL_CHOICES = [
        (1, 'Начальный'),
        (2, 'Базовый'),
        (3, 'Средний'),
        (4, 'Продвинутый'),
        (5, 'Эксперт'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='Название технологии'
    )
    
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True,
        verbose_name='URL-имя'
    )
    
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Категория'
    )
    
    level = models.IntegerField(
        choices=LEVEL_CHOICES,
        default=3,
        verbose_name='Уровень владения'
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    
    icon_class = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Класс иконки (Bootstrap Icons)',
        help_text='Например: bi-github, bi-python, bi-react'
    )
    
    icon_color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Цвет иконки',
        default='#3a6656',
        help_text='HEX код цвета, например: #3a6656'
    )
    
    bg_color = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Цвет фона',
        default='#e9f0e8',
        help_text='HEX код цвета фона'
    )
    
    order = models.IntegerField(
        default=0,
        verbose_name='Порядок сортировки'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    
    experience_years = models.FloatField(
        default=0,
        verbose_name='Лет опыта'
    )
    
    last_used = models.DateField(
        blank=True,
        null=True,
        verbose_name='Последнее использование'
    )
    
    # Метаданные
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'
        ordering = ['order', 'category', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['is_active']),
        ]
    
    def save(self, *args, **kwargs):
        """Автоматическое создание slug при сохранении"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_level_display_with_stars(self):
        """Отображение уровня в виде звездочек"""
        stars = '★' * self.level + '☆' * (5 - self.level)
        return f"{self.get_level_display()} {stars}"
    
    def get_icon_html(self):
        """Получение HTML для иконки"""
        if self.icon_class:
            return f'<i class="bi {self.icon_class}" style="color: {self.icon_color or "#3a6656"};"></i>'
        return ''
    
    @property
    def level_percentage(self):
        """Уровень в процентах (для прогресс-баров)"""
        return self.level * 20  # 1-5 в 20-100%
    
    @classmethod
    def get_by_category(cls):
        """Получение технологий, сгруппированных по категориям"""
        categories = {}
        for tech in cls.objects.filter(is_active=True).order_by('order', 'name'):
            if tech.category not in categories:
                categories[tech.category] = []
            categories[tech.category].append(tech)
        return categories


class Skill(models.Model):
    SKILL_CATEGORIES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('devops', 'DevOps'),
        ('database', 'Database'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название')
    category = models.CharField(
        max_length=20, 
        choices=SKILL_CATEGORIES, 
        default='backend',
        verbose_name='Категория'
    )
    proficiency = models.IntegerField(
        default=50,
        verbose_name='Уровень владения (%)',
        help_text='От 0 до 100'
    )
    technology = models.ForeignKey(
        Technology,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='skills',
        verbose_name='Связанная технология'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.CharField(max_length=100, blank=True, verbose_name='Иконка')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    
    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.name
    
    @property
    def proficiency_display(self):
        """Отображение уровня в удобном виде"""
        if self.proficiency >= 80:
            return "Эксперт"
        elif self.proficiency >= 60:
            return "Продвинутый"
        elif self.proficiency >= 40:
            return "Средний"
        elif self.proficiency >= 20:
            return "Базовый"
        else:
            return "Начальный"

class Experience(models.Model):
    title = models.CharField(max_length=200, verbose_name='Должность')
    company = models.CharField(max_length=200, verbose_name='Компания')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    current = models.BooleanField(default=False, verbose_name='Текущее место работы')
    description = models.TextField(verbose_name='Описание')
    technologies = models.CharField(max_length=300, blank=True, verbose_name='Технологии')
    
    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    def duration_display(self):
        """Отображение длительности работы"""
        if self.current:
            return f"{self.start_date.strftime('%Y')} - настоящее время"
        elif self.end_date:
            return f"{self.start_date.strftime('%Y')} - {self.end_date.strftime('%Y')}"
        return self.start_date.strftime('%Y')

class Education(models.Model):
    institution = models.CharField(max_length=200, verbose_name='Учебное заведение')
    faculty = models.CharField(max_length=200, verbose_name='Факультет/Специальность')
    start_year = models.IntegerField(verbose_name='Год начала')
    end_year = models.IntegerField(verbose_name='Год окончания')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'
        ordering = ['-end_year']
    
    def __str__(self):
        return f"{self.institution} ({self.start_year}-{self.end_year})"

class PersonalInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя')
    title = models.CharField(max_length=200, verbose_name='Должность/Специализация')
    about = models.TextField(verbose_name='О себе')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    location = models.CharField(max_length=100, blank=True, verbose_name='Местоположение')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn')
    github = models.URLField(blank=True, verbose_name='GitHub')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Telegram')
    
    class Meta:
        verbose_name = 'Персональная информация'
        verbose_name_plural = 'Персональная информация'
    
    def __str__(self):
        return self.name
