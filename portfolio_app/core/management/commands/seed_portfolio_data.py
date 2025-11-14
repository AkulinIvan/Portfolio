from django.core.management.base import BaseCommand
from core.models import (
    PersonalInfo, Skill, Experience, Project, Education
)

class Command(BaseCommand):
    help = 'Заполняет базу данных персональной информацией и проектами'
    
    def handle(self, *args, **options):
        # Персональная информация
        personal_info, created = PersonalInfo.objects.get_or_create(
            name="Акулин Иван",
            defaults={
                'title': 'Backend Developer (Golang/Python)',
                'about': '''Занимаюсь разработкой высоконагруженных микросервисных архитектур, монолитов и оптимизацией производительности. Легко и быстро нахожу общий язык с командой, добиваюсь максимальной эффективности. Уверен, что чистый и качественный код и внимание к деталям - основа успеха проекта.

Сейчас ищу интересный проект, на котором буду применять свой профессионализм на благо компании.''',
                'email': 'ivanakulin175@gmail.com',
                'location': 'Красноярск',
                'github': 'https://github.com/AkulinIvan',
                'telegram': '@Akula_Iv'
            }
        )
        
        # Образование
        Education.objects.get_or_create(
            institution='Сибирский федеральный университет',
            faculty='Институт космических и информационных технологий',
            start_year=2010,
            end_year=2014,
            description='Высшее техническое образование'
        )
        
        # Навыки - Языки программирования
        programming_skills = [
            ('Golang', 'backend', 70, '3 года опыта', 1),
            ('Python', 'backend', 75, '4 года опыта', 2),
        ]
        
        # Технологии
        tech_skills = [
            ('gRPC', 'backend', 65, '1 год опыта', 3),
            ('Protobuf', 'backend', 65, '1 год опыта', 4),
            ('REST API', 'backend', 75, '2 года опыта', 5),
            ('Git', 'other', 75, '2 года опыта', 6),
            ('Docker', 'devops', 75, '2 года опыта', 7),
            ('Docker Compose', 'devops', 60, '2 года опыта', 8),
            ('JSON', 'backend', 75, '2 года опыта', 9),
            ('Kafka', 'backend', 65, '1 год опыта', 10),
        ]
        
        # Базы данных
        db_skills = [
            ('PostgreSQL', 'database', 75, '3 года опыта', 11),
            ('Redis', 'database', 65, '1 год опыта', 12),
            ('ClickHouse', 'database', 60, '1 год опыта', 13),
            ('MongoDB', 'database', 60, '1 год опыта', 14),
        ]
        
        # Операционные системы
        os_skills = [
            ('Windows', 'other', 80, '10+ лет опыта', 15),
            ('Linux', 'other', 70, '3 года опыта', 16),
        ]
        
        all_skills = programming_skills + tech_skills + db_skills + os_skills
        
        for name, category, proficiency, description, order in all_skills:
            Skill.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'proficiency': proficiency,
                    'description': description,
                    'order': order
                }
            )
        
        # Опыт работы
        experiences = [
            {
                'title': 'Golang Developer',
                'company': 'Платформа (Красноярск)',
                'start_date': '2024-03-01',
                'current': True,
                'description': '''Проект: CRM система приема заявок в сфере ЖКХ

Обязанности:
• Поддержка CRM системы диспетчерской службы для сферы ЖКХ
• Распил монолита на PHP на микросервисы на Go
• Разработка новых модулей и функций для повышения удобства пользователей и автоматизации процессов
• Организация мониторинга за сервером (Grafana, Prometheus)
• Помощь сотрудникам в решении инфраструктурных задач, настройке окружений и устранении проблем

Достижения:
• Настроил интеграцию с внешними системами: интеграция сервиса с внешними API (Asterisk)
• Реализовал аутентификацию пользователей OAuth 2 и механизмы шифрования (TLS)
• Настроил мониторинг сервиса (Grafana, Prometheus), что позволило сократить время простоя на 30%
• Реализовал сервис уведомлений пользователей о новых заявках через SMS
• Оптимизировал работу базы данных, что привело к уменьшению времени отклика на запросы на 25%''',
                'technologies': 'Golang, Gorm, gRPC, Redis, Kafka, Asterisk, PostgreSQL, Grafana, Prometheus'
            },
            {
                'title': 'Python Developer',
                'company': 'Интелком (Красноярск)',
                'start_date': '2022-07-01',
                'end_date': '2024-02-01',
                'current': False,
                'description': '''Проект: Платформа для мониторинга сети

Обязанности:
• Разработка и поддержка платформы для мониторинга сети интернет провайдера
• Интеграция с внешними системами: Интеграция сервисов с внешними API
• Документирование кода и процессов: Создание технической документации, описание API, схем архитектуры и поддержание стандартов кодирования
• Работа в команде: Участие в agile-процессах, проведение code review, обмен знаниями и менторство коллег
• Мониторинг и логирование: Настройка логирования для оперативного обнаружения и устранения проблем

Достижения:
• Разработал архитектуру для высоконагруженной системы, которая обрабатывает 1000 запросов в день
• Автоматизировал рутинные задачи с использованием скриптов Python
• Реализовал систему мониторинга, которая снизила количество инцидентов на 50%
• Внедрил систему уведомлений о состоянии серверов, интегрировал с telegram bot API''',
                'technologies': 'Python, PostgreSQL, REST API, Telegram API, Zabbix'
            }
        ]
        
        for exp_data in experiences:
            Experience.objects.get_or_create(
                title=exp_data['title'],
                company=exp_data['company'],
                defaults=exp_data
            )
        
        # Проекты
        projects = [
            {
                'title': 'CRM система для ЖКХ',
                'description': 'Разработка микросервисной CRM системы для диспетчерской службы в сфере ЖКХ. Система обрабатывает заявки, управляет задачами и обеспечивает коммуникацию между сотрудниками и клиентами.',
                'project_type': 'web',
                'technologies': 'Python, Redis, PostgreSQL, Docker',
                'github_url': 'https://github.com/AkulinIvan/ADS',
                'is_featured': True,
                'order': 1
            },
            {
                'title': 'Платформа мониторинга сети',
                'description': 'Разработка высоконагруженной платформы для мониторинга сети интернет-провайдера. Система собирает метрики, генерирует отчеты и отправляет уведомления о проблемах.',
                'project_type': 'web',
                'technologies': 'Python, Django, PostgreSQL, REST API, Telegram API, Zabbix',
                'github_url': 'https://github.com/yourusername/network-monitoring',
                'is_featured': True,
                'order': 2
            },
            {
                'title': 'Микросервис аутентификации',
                'description': 'Разработка микросервиса аутентификации с поддержкой OAuth 2.0 и JWT токенов. Интегрирован с основной CRM системой.',
                'project_type': 'web',
                'technologies': 'Golang, gRPC, Redis, JWT, OAuth2, PostgreSQL',
                'github_url': 'https://github.com/yourusername/auth-service',
                'is_featured': True,
                'order': 3
            },
            {
                'title': 'Сервис уведомлений',
                'description': 'Разработка сервиса для отправки SMS и email уведомлений. Интеграция с внешними провайдерами и Asterisk для голосовых уведомлений.',
                'project_type': 'web',
                'technologies': 'Golang, Kafka, Redis, SMS API, Asterisk, PostgreSQL',
                'github_url': 'https://github.com/yourusername/notification-service',
                'is_featured': False,
                'order': 4
            },
            {
                'title': 'API для интеграции с Asterisk',
                'description': 'REST API для интеграции CRM системы с Asterisk PBX. Обеспечивает управление звонками и голосовыми уведомлениями.',
                'project_type': 'web',
                'technologies': 'Golang, REST API, Asterisk, PostgreSQL',
                'github_url': 'https://github.com/yourusername/asterisk-api',
                'is_featured': False,
                'order': 5
            },
            {
                'title': 'Система сбора метрик',
                'description': 'Система для сбора и анализа метрик производительности. Интеграция с Prometheus и Grafana для визуализации данных.',
                'project_type': 'web',
                'technologies': 'Python, Prometheus, Grafana, PostgreSQL, Docker',
                'github_url': 'https://github.com/yourusername/metrics-collector',
                'is_featured': False,
                'order': 6
            }
        ]
        
        for project_data in projects:
            Project.objects.get_or_create(
                title=project_data['title'],
                defaults=project_data
            )
        
        self.stdout.write(
            self.style.SUCCESS('Данные портфолио успешно созданы!')
        )