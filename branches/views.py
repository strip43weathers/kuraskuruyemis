# branches/views.py
from django.views.generic import ListView, DetailView
from .models import Branch


class BranchListView(ListView):
    model = Branch
    template_name = 'branches/branch_list.html'
    context_object_name = 'branches'

    def get_queryset(self):
        return Branch.objects.filter(is_active=True)  # Sadece aktif şubeleri listele


class BranchDetailView(DetailView):
    model = Branch
    template_name = 'branches/branch_detail.html'
    context_object_name = 'branch'
