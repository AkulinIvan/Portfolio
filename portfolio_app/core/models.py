from django.db import models
from django.urls import reverse

class Project(models.Model):
    PROJECT_TYPES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('desktop', 'Desktop Application'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    project_type = models.CharField(
        max_length=20, 
        choices=PROJECT_TYPES, 
        default='web',
        verbose_name='Тип проекта'
    )
    technologies = models.CharField(max_length=300, verbose_name='Технологии')
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name='Изображение')
    github_url = models.URLField(blank=True, verbose_name='GitHub ссылка')
    live_url = models.URLField(blank=True, verbose_name='Демо ссылка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_featured = models.BooleanField(default=False, verbose_name='В избранном')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

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
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.CharField(max_length=100, blank=True, verbose_name='Иконка')
    order = models.IntegerField(default=0, verbose_name='Порядок отображения')
    
    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.name

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