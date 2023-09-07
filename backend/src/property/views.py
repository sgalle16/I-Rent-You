from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Property, PropertyComment, PropertyRating
from .forms import PropertyForm


class PropertyListView(ListView):
    model = Property


class PropertyDetailView(DetailView):
    model = Property


class PropertyCreateView(CreateView):
    form_class = PropertyForm
    model = Property
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'crear'
        })
        return context


class PropertyUpdateView(UpdateView):
    form_class = PropertyForm
    model = Property
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'actualizar'
        })
        return context


class PropertyDeleteView(DeleteView):
    model = Property
    success_url = '/'
