from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Property, PropertyFeature, PropertyComment, PropertyRating
from .forms import PropertyForm, PropertyFeatureForm
from django.urls import reverse, reverse_lazy


class PropertyListView(ListView):
    model = Property
    template_name = 'property/property_list.html'
    context_object_name = 'properties'

    # Obtener el valor del parámetro 'property_type' de la solicitud GET desde la URL
    def get_queryset(self):
        property_type = self.request.GET.get('property_type')
        # Obtener todos los objetos de Property
        queryset = Property.objects.all()

        # Si se proporciona un valor para 'property_type', filtrar los objetos de Property por ese valor
        if property_type:
            queryset = queryset.filter(type_of_property=property_type)
        return queryset


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property/property_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener los detalles de la propiedad (PropertyFeature) relacionados con esta propiedad
        property_details = PropertyFeature.objects.get(property=self.object)

        context['property_details'] = property_details
        return context


class PropertyFeatureCreateView(CreateView):
    model = Property
    form_class = PropertyFeatureForm  # Formulario
    template_name = 'property/propertyfeature_form.html'
    # Redirigir a la página de inicio después de crear una característica
    success_url = '/'

    def form_valid(self, form):
        # Obtener la propiedad actual desde el ID de la URL
        property_id = self.kwargs['pk']
        property = get_object_or_404(Property, pk=property_id)

        # Asignar la propiedad actual a la característica antes de guardarla
        form.instance.property = property
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener la propiedad actual desde el ID de la URL y pasarla al contexto
        property_id = self.kwargs['pk']
        property = get_object_or_404(Property, pk=property_id)
        context['property'] = property
        return context


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
