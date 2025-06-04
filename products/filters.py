import django_filters
from django.conf import settings
import google.generativeai as genai
from django.db.models import Q
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='variants__price', lookup_expr='gt')
    price_max = django_filters.NumberFilter(field_name='variants__price', lookup_expr='lt')
    size = django_filters.CharFilter(field_name='variants__size', lookup_expr='iexact')
    color = django_filters.CharFilter(field_name='variants__color_name', lookup_expr='iexact')
    search = django_filters.CharFilter(method='filter_search', label='Search')

    class Meta:
        model = Product
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        search_query = self.data.get('search')
        if search_query:
            parsed_params = self.parse_search_query(search_query)
            print(f"Parsed parameters: {parsed_params}")
            self.form.data = {
                **self.form.data,
                'price_min': parsed_params.get('price_min'),
                'price_max': parsed_params.get('price_max'),
                'size': parsed_params.get('size'),
                'color': parsed_params.get('color'),
                'search': search_query
            }

    def parse_search_query(self, query):
        """Parse search query using Gemini API."""
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Parse the following search query to extract product filter parameters: price_min, price_max, size, and color.
        Return the result as a JSON object with these fields. If a parameter is not found, set it to null.
        For price, interpret terms like 'under' or 'below' as price_max, and 'above' or 'over' as price_min.
        For size, look for common clothing sizes (e.g., S, M, L, XL, XXL).
        For color, look for common color names (e.g., red, blue, black, white).
        Query: "{query}"
        Example output: {{"price_min": null, "price_max": 500, "size": null, "color": "Red"}}
        """
        response = model.generate_content(prompt)
        try:
            import json
            parsed_params = json.loads(response.text.strip('```json\n').strip('```'))
            return {
                'price_min': parsed_params.get('price_min'),
                'price_max': parsed_params.get('price_max'),
                'size': parsed_params.get('size'),
                'color': parsed_params.get('color')
            }
        except (json.JSONDecodeError, AttributeError):
            print(f"Failed to parse Gemini response: {response.text}")
            return {
                'price_min': None,
                'price_max': None,
                'size': None,
                'color': None
            }

    def filter_search(self, queryset, name, value):
        print(f"Search query: {value}")
        if value:
            words = value.split()
            query = Q()
            for word in words:
                query |= Q(name__icontains=word)
            return queryset.filter(query)
        return queryset

    def filter_queryset(self, queryset):
        print(f"Initial queryset count: {queryset.count()}")
        queryset = super().filter_queryset(queryset)
        print(f"After super().filter_queryset: {queryset.count()}")
        
        size = self.form.cleaned_data.get('size')
        price_min = self.form.cleaned_data.get('price_min')
        price_max = self.form.cleaned_data.get('price_max')
        color = self.form.cleaned_data.get('color')

        print('Color:', color)
        print('price_min:', price_min)
        print('price_max:', price_max)

        if size:
            queryset = queryset.filter(variants__size__iexact=size)
            print(f"After size filter: {queryset.count()}")
        if color:
            queryset = queryset.filter(variants__color_name__iexact=color)
            print(f"After color filter: {queryset.count()}")
        if price_min:
            queryset = queryset.filter(variants__price__gt=price_min)
            print(f"After price_min filter: {queryset.count()}")
        if price_max:
            queryset = queryset.filter(variants__price__lt=price_max)
            print(f"After price_max filter: {queryset.count()}")

        return queryset.distinct()