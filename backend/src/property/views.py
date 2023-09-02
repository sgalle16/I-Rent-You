from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Property, PropertyComment, PropertyRating

class PropertyListView(ListView):
    model = Property


class PropertyDetailView(DetailView):
    model = Property


class PropertyCreateView(CreateView):
    model = Property


class PropertyUpdateView(UpdateView):
    model = Property

class PropertyDeleteView(DeleteView):
    model = Property

