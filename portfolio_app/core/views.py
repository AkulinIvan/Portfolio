from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Education, PersonalInfo, Skill, Experience, Technology


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['skills'] = Skill.objects.all().order_by('category', 'order')[:8]
        context['experiences'] = Experience.objects.all().order_by('-start_date')[:2]
        context['personal_info'] = PersonalInfo.objects.first()
        
        # Получаем статистику для главной страницы
        context['technologies_by_category'] = Technology.get_by_category()
        
        context['years_experience'] = self.calculate_years_experience()
        
        return context
    
    def calculate_years_experience(self):
        """Рассчитывает общий опыт работы в годах"""
        from datetime import date
        
        experiences = Experience.objects.all()
        total_days = 0
        
        for exp in experiences:
            if exp.current:
                end_date = date.today()
            elif exp.end_date:
                end_date = exp.end_date
            else:
                continue
                
            days = (end_date - exp.start_date).days
            total_days += max(days, 0)  # На случай если даты перепутаны
        
        return round(total_days / 365.25, 1)  # Примерно 4.3 года







class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Группируем навыки по категориям
        skills = Skill.objects.all().order_by('category', 'order')
        skill_categories = {}
        
        for skill in skills:
            if skill.category not in skill_categories:
                skill_categories[skill.category] = []
            skill_categories[skill.category].append(skill)
        
        context['skill_categories'] = skill_categories
        context['experiences'] = Experience.objects.all().order_by('-start_date')
        context['educations'] = Education.objects.all().order_by('-end_year')
        context['personal_info'] = PersonalInfo.objects.first()
        
        # Рассчитываем опыт
        context['years_experience'] = self.calculate_years_experience()
        
        
        # Технологии по категориям
        context['technologies_by_category'] = Technology.get_by_category()
        
        return context
    
    def calculate_years_experience(self):
        """Рассчитывает общий опыт работы в годах"""
        from datetime import date
        
        experiences = Experience.objects.all()
        total_days = 0
        
        for exp in experiences:
            if exp.current:
                end_date = date.today()
            elif exp.end_date:
                end_date = exp.end_date
            else:
                continue
                
            days = (end_date - exp.start_date).days
            total_days += max(days, 0)
        
        return round(total_days / 365.25, 1)


class ContactView(FormView):
    template_name = 'core/contact.html'
    success_url = reverse_lazy('contact')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['personal_info'] = PersonalInfo.objects.first()
        return context
    
    def get_form(self):
        # Создаем простую форму
        from django import forms
        
        class ContactForm(forms.Form):
            name = forms.CharField(
                label='Ваше имя',
                max_length=100,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Иван Иванов'
                })
            )
            email = forms.EmailField(
                label='Email',
                widget=forms.EmailInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'example@domain.com'
                })
            )
            subject = forms.CharField(
                label='Тема сообщения',
                max_length=200,
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Например: Разработка API для моего проекта'
                })
            )
            project_type = forms.ChoiceField(
                label='Тип проекта',
                choices=[
                    ('', 'Выберите тип проекта'),
                    ('web', 'Веб-разработка'),
                    ('api', 'API разработка'),
                    ('microservices', 'Микросервисная архитектура'),
                    ('database', 'Базы данных'),
                    ('devops', 'DevOps'),
                    ('consultation', 'Консультация'),
                    ('other', 'Другое'),
                ],
                required=False,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            budget = forms.ChoiceField(
                label='Бюджет проекта',
                choices=[
                    ('', 'Выберите бюджет'),
                    ('small', 'До 50,000 руб.'),
                    ('medium', '50,000 - 200,000 руб.'),
                    ('large', '200,000 - 500,000 руб.'),
                    ('enterprise', 'Свыше 500,000 руб.'),
                    ('discuss', 'Требует обсуждения'),
                ],
                required=False,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
            message = forms.CharField(
                label='Сообщение',
                widget=forms.Textarea(attrs={
                    'class': 'form-control',
                    'rows': 6,
                    'placeholder': 'Опишите ваш проект, задачи, требования и цели...'
                })
            )
            privacy = forms.BooleanField(
                label='Я соглашаюсь с обработкой персональных данных',
                widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
            )
        
        return ContactForm(**self.get_form_kwargs())
    
    def form_valid(self, form):
        # Обработка успешной отправки формы
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        project_type = form.cleaned_data['project_type']
        budget = form.cleaned_data['budget']
        
        # Отправка email
        email_subject = f"Новая заявка от {name}: {subject}"
        email_message = f"""
        Имя: {name}
        Email: {email}
        Тема: {subject}
        Тип проекта: {project_type}
        Бюджет: {budget}
        
        Сообщение:
        {message}
        
        ---
        Это сообщение отправлено через форму обратной связи с сайта.
        """
        
        try:
            # Отправляем email себе
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # Отправляем подтверждение пользователю
            send_mail(
                "Ваше сообщение получено",
                f"""Здравствуйте, {name}!

Спасибо за ваше сообщение по теме "{subject}".
Я получил вашу заявку и свяжусь с вами в ближайшее время (обычно в течение 4-8 рабочих часов).

С уважением,
ACTIOS TECH""",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            
            messages.success(self.request, 'Сообщение успешно отправлено! Я свяжусь с вами в ближайшее время.')
            
        except Exception as e:
            messages.error(self.request, f'Произошла ошибка при отправке: {str(e)}')
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


# from django.views.generic import TemplateView
# from django.contrib import messages
# from django.shortcuts import redirect

# class ContactView(TemplateView):
#     template_name = 'core/contact.html'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['personal_info'] = PersonalInfo.objects.first()
#         return context
    
#     def post(self, request, *args, **kwargs):
#         # Обработка POST запроса
#         name = request.POST.get('name', '').strip()
#         email = request.POST.get('email', '').strip()
#         subject = request.POST.get('subject', '').strip()
#         message = request.POST.get('message', '').strip()
#         privacy = request.POST.get('privacy', False)
        
#         # Простая валидация
#         if not name or not email or not subject or not message or not privacy:
#             messages.error(request, 'Пожалуйста, заполните все обязательные поля')
#         else:
#             # Логируем полученные данные
#             print(f"Получена заявка от {name} ({email}): {subject}")
#             print(f"Сообщение: {message[:100]}...")
            
#             messages.success(request, 'Сообщение успешно отправлено! Я свяжусь с вами в ближайшее время.')
        
#         return redirect('contact')