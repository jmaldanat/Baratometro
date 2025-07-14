from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Task
from django.utils import timezone

class TaskView(LoginRequiredMixin, TemplateView):
    template_name = 'task/task.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Get all tasks for the current user
        context['tasks'] = Task.objects.filter(user=user).order_by('-created_on')
        return context


