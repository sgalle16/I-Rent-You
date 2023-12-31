from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Property, PropertyFeature, PropertyImage, PropertyComment, PropertyRating
from .forms import PropertyForm, PropertyFeatureForm, PropertyImageForm
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from Users.mixins import LessorUserMixin, TenantUserMixin
from .mixins import PropertyLessorMixin
from django.contrib import messages


class PropertySearchListView(ListView):
    model = Property
    template_name = 'property/property_list.html'
    context_object_name = 'properties'

    # Obtener el valor del parámetro 'property_type' o 'location' de la solicitud GET desde la URL

    def get_queryset(self):
        queryset = Property.objects.all()
        query = self.request.GET.get('q')
        property_type = self.request.GET.get('property_type')

        if query:
            keywords = query.split()
            # Búsqueda por palabras clave; título, ubicación y descripción
            keyword_queries = Q()
            for keyword in keywords:
                keyword_queries |= Q(title__icontains=keyword) | Q(
                    location__icontains=keyword) | Q(description__icontains=keyword)
            queryset = queryset.filter(keyword_queries)

        # Si se proporciona un valor para 'property_type', filtrar los objetos de Property por ese valor
        if property_type:
            queryset = queryset.filter(type_of_property=property_type)

        return queryset


class PropertyListView(ListView):
    model = Property
    template_name = 'property/property_list.html'
    context_object_name = 'properties'
    paginate_by = 9

    def get_queryset(self):
        # Obtener todos los objetos de Property
        queryset = Property.objects.all().order_by("published_date")

        return queryset

    def get_context_data(self, **kwargs):
        property_list = list(Property.objects.all())
        # Establece la cantidad de elementos por página
        paginator = Paginator(property_list, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            properties = paginator.page(page)
        except PageNotAnInteger:
            properties = paginator.page(1)
        except EmptyPage:
            properties = paginator.page(paginator.num_pages)

        context = {
            'properties': properties
        }
        return context


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'property/property_detail.html'
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Utiliza el atributo 'features' para acceder a las características de la propiedad
        property_details = self.object.features

        context['property_details'] = property_details
        return context


class PropertyCreateView(LessorUserMixin, CreateView):
    form_class = PropertyForm
    model = Property
    template_name = 'property/property_create.html'
    success_url = reverse_lazy('user:lessor-properties')

    def form_valid(self, form):
        # Verifica si el usuario actual no tiene permisos para crear una propiedad
        if not self.can_create_property():
            # Redirige al usuario a la página de inicio de sesión si no está logeado
            return redirect(reverse('login'))
        # Asigna el usuario(lessor) actual como propietario al crear la propiedad
        form.instance.owner = self.request.user
        # Validación de campos requeridos
        if form.is_valid():
            # Guarda la propiedad
            response = super().form_valid(form)
            # Si el formulario de características es válido, guarda las características de la propiedad
            feature_form = PropertyFeatureForm(self.request.POST)
            if feature_form.is_valid():
                feature = feature_form.save(commit=False)
                feature.property = self.object  # 'self.object' contiene la propiedad recién creada
                feature.save()

            # Guarda y procesa el formulario de imágenes
            images_form = PropertyImageForm(
                self.request.POST, self.request.FILES)
            if images_form.is_valid():
                images = [PropertyImage(property=self.object, images=image)
                          for image in images_form.cleaned_data['images'] if image]
                PropertyImage.objects.bulk_create(images)

                messages.success(
                    self.request, 'La propiedad se ha creado exitosamente.')
            return response

        else:
            messages.error(
                self.request, 'Hubo un error al procesar el formulario.')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'view_type': 'Crear',
            # Agrega un formulario de características vacío al contexto
            'feature_form': PropertyFeatureForm(),
            # Agregar un formulario para cargar imágenes
            'images_form': PropertyImageForm(),
        })
        return context


class PropertyUpdateView(PropertyLessorMixin, UpdateView):
    form_class = PropertyForm
    model = Property
    template_name = 'property/property_update.html'
    success_url = reverse_lazy('user:lessor-properties')

    def dispatch(self, request, *args, **kwargs):
        # Comprueba si el usuario actual es un "lessor" o administrador
        if not self.can_create_property():
            raise Http404("No tiene permisos para actualizar esta propiedad.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Llama al método form_valid de la clase base
        response = super().form_valid(form)

        # Guarda las características de la propiedad
        self.save_property_features()

        # Elimina imágenes marcadas para eliminación
        self.delete_marked_images()

        # Guarda y procesa las nuevas imágenes de la propiedad
        self.save_property_images()

        # Muestra un mensaje de éxito
        messages.success(
            self.request, 'La propiedad se ha actualizado exitosamente.')

        return response

    def save_property_features(self):
        # Obtiene el formulario de características y lo guarda
        feature_form = PropertyFeatureForm(
            self.request.POST, instance=self.object.features)
        if feature_form.is_valid():
            feature_form.save()

    def delete_marked_images(self):
        # Obtiene las imágenes marcadas para eliminación y las elimina
        images_to_delete = self.request.POST.getlist('images_to_delete')
        if images_to_delete:
            self.object.images.filter(id__in=images_to_delete).delete()

    def save_property_images(self):
        # Guarda y procesa las nuevas imágenes de la propiedad
        images_form = PropertyImageForm(self.request.POST, self.request.FILES)
        if images_form.is_valid():
            images = self.request.FILES.getlist('images')
            for image in images:
                PropertyImage.objects.create(
                    property=self.object, images=image)
        else:
            # Muestra un mensaje de error si hay problemas con las imágenes
            messages.error(
                self.request, 'Hubo un problema al cargar las imágenes. Por favor, verifica los archivos.')

    def get_context_data(self, **kwargs):
        # Obtiene el contexto de la superclase
        context = super().get_context_data(**kwargs)
        # Agrega información adicional al contexto
        context.update({
            'view_type': 'Editar',
            'feature_form': PropertyFeatureForm(instance=self.object.features),
            'images_form': PropertyImageForm(),
        })
        # Si estás editando una propiedad existente, pasa las imágenes existentes al contexto
        if self.object:
            context['property_images'] = self.object.images.all()

        return context


class LessorPropertyListView(LessorUserMixin, ListView):
    model = Property
    template_name = "lessor/index.html"
    context_object_name = 'properties'  # Nombre de la variable en la plantilla
    paginate_by = 9

    def get_queryset(self, *args, **kwargs):
        # Filtrar y ordenar las propiedades por fecha de publicación
        queryset = super(LessorPropertyListView, self).get_queryset(**kwargs)
        queryset = queryset.filter(owner=self.get_lessor())
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(
                description__icontains=query))
        return queryset.order_by("published_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lessor_properties = self.get_properties().order_by("published_date")

        # Establece la cantidad de elementos por página
        paginator = Paginator(lessor_properties, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            properties = paginator.page(page)
        except PageNotAnInteger:
            properties = paginator.page(1)
        except EmptyPage:
            properties = paginator.page(paginator.num_pages)

        context.update({
            'properties': properties
        })
        return context


class PropertyDeleteView(PropertyLessorMixin, DeleteView):
    model = Property
    template_name = 'property/property_delete.html'
    success_url = reverse_lazy('property:list')

    def dispatch(self, request, *args, **kwargs):
        # Comprueba si el usuario actual es un "lessor" o administrador
        if not self.can_create_property():
            raise Http404("No tiene permisos para eliminar esta propiedad.")
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.info(self.request, 'La propiedad se ha eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)
