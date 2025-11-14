from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Education, PersonalInfo, Project, Skill, Experience

class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:3]
        context['skills'] = Skill.objects.all()
        context['experiences'] = Experience.objects.all()[:2]
        context['personal_info'] = PersonalInfo.objects.first()
        return context

class ProjectListView(ListView):
    model = Project
    template_name = 'core/projects.html'
    context_object_name = 'projects'
    paginate_by = 6

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'

class AboutView(TemplateView):
    template_name = 'core/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()
        context['experiences'] = Experience.objects.all()
        context['educations'] = Education.objects.all()
        context['personal_info'] = PersonalInfo.objects.first()
        return context