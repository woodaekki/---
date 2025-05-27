from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import GoldPrice, SilverPrice
from .serializers import GoldPriceSerializer, SilverPriceSerializer

# Create your views here.
@api_view(['GET'])
def gold_prices(request):
    gold_data = GoldPrice.objects.order_by('date')
    serializer = GoldPriceSerializer(gold_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def silver_prices(request):
    silver_data = SilverPrice.objects.order_by('date')
    serializer = SilverPriceSerializer(silver_data, many=True)
    return Response(serializer.data)
