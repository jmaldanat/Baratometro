from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Task
from product.models import Product
from django.contrib import messages
import re
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone

class TaskView(LoginRequiredMixin, TemplateView):
    template_name = 'task/task.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Get all tasks for the current user
        context['tasks'] = Task.objects.filter(user=user).order_by('-created_on')
        # Agrega can_save_more al contexto
        can_save_more = True
        if user.is_authenticated and hasattr(user, 'perfil'):
            can_save_more = user.perfil.can_save_more_products()
        context['can_save_more'] = can_save_more
        return context

@login_required
def create_task_from_url(request):
    if request.method == 'POST':
        url = request.POST.get('search_url', '')
        
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Create a basic title from the URL
        domain = re.search(r'://([^/]+)', url)
        title = f"Track product on {domain.group(1) if domain else url}"
        
        # Create the task without specifying a product
        task = Task.objects.create(
            title=title,
            url=url,
            content=f"Task created to track product at {url}",
            user=request.user,
            status='pending'
        )
        
        messages.success(request, f"New tracking task created for: {url}")
        return redirect('task')
    
    # If not POST, redirect to home
    return redirect('home')
