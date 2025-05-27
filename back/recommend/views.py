from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomerRecord
from collections import Counter

# recommend/views.py
@api_view(['GET'])
def recommend_products(request):
    age_group = request.GET.get('age_group')
    income = request.GET.get('income')
    job = request.GET.get('job')
    city = request.GET.get('city')

    age_ranges = {
        'under20': (0, 19), '20s': (20, 29), '30s': (30, 39),
        '40s': (40, 49), '50s': (50, 59), '60s': (60, 69),
        '70s': (70, 79), '80plus': (80, 150)
    }

    filters = {}
    if age_group in age_ranges:
        min_age, max_age = age_ranges[age_group]
        filters['age__gte'] = min_age
        filters['age__lte'] = max_age
    if income and income != '0':
        filters['income'] = income
    if job and job != '선택 안함':
        filters['jobs'] = job
    if city:
        filters['city'] = city

    filtered = CustomerRecord.objects.filter(**filters)

    # 상품 카운팅
    deposit_counter = Counter()
    saving_counter = Counter()

    for entry in filtered:
        key = (entry.product_name, entry.bank_name)
        if entry.product_type == "예금":
            deposit_counter[key] += 1
        elif entry.product_type == "적금":
            saving_counter[key] += 1

    def format_counter(counter):
        return [
            {"product_name": name, "bank_name": bank, "count": count}
            for (name, bank), count in counter.most_common()
        ]

    return Response({
        "deposits": format_counter(deposit_counter),
        "savings": format_counter(saving_counter),
    })
