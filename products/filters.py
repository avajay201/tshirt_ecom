import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter()
    price_max = django_filters.NumberFilter()
    size = django_filters.CharFilter()
    color = django_filters.CharFilter()
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Product
        fields = []

    def filter_search(self, queryset, name, value):
        print(value)
        return queryset.filter(name__icontains=value)


    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)    
        size = self.form.cleaned_data.get('size')
        price_min = self.form.cleaned_data.get('price_min')
        price_max = self.form.cleaned_data.get('price_max')
        color = self.form.cleaned_data.get('color')
       

        print('Color:', color)
        print('privce_min:', price_min)
        print('price_max:', price_max)

        if size:
            queryset = queryset.filter(variants__size=size)
        if color:
            queryset = queryset.filter(variants__color_name=color)
        if price_min:
            queryset = queryset.exclude(variants__price__lte=price_min)
        if price_max:
            queryset = queryset.exclude(variants__price__gte=price_max)
        

        return queryset