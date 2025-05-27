import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions
from .serializers import (
    DepositProductsSerializer,
    DepositOptionsSerializer,
    SavingProductsSerializer,
    SavingOptionsSerializer
)
from .api import fetch_deposit_products, fetch_saving_products

class DepositProductsViewSet(viewsets.ModelViewSet):
    queryset = DepositProducts.objects.all()
    serializer_class = DepositProductsSerializer
    lookup_field = 'fin_prdt_cd'  # 반드시 명시

class DepositOptionsViewSet(viewsets.ModelViewSet):
    queryset = DepositOptions.objects.all()
    serializer_class = DepositOptionsSerializer

class SavingProductsViewSet(viewsets.ModelViewSet):
    queryset = SavingProducts.objects.all()
    serializer_class = SavingProductsSerializer
    lookup_field = 'fin_prdt_cd'  # 반드시 명시

class SavingOptionsViewSet(viewsets.ModelViewSet):
    queryset = SavingOptions.objects.all()
    serializer_class = SavingOptionsSerializer


@api_view(['GET'])
def save_products(request):
    deposit_data = fetch_deposit_products()
    saving_data = fetch_saving_products()

    # 예금 상품 저장
    if not deposit_data:
        return Response({'error': '예금상품 호출 실패'}, status=500)

    deposit_base_list = deposit_data.get('result', {}).get('baseList', [])
    deposit_option_list = deposit_data.get('result', {}).get('optionList', [])
    
    for item in deposit_base_list:
        if not DepositProducts.objects.filter(fin_prdt_cd=item['fin_prdt_cd']).exists():
            DepositProducts.objects.create(
                fin_prdt_cd=item['fin_prdt_cd'],
                dcls_month=item.get('dcls_month', ''),
                fin_co_no=item.get('fin_co_no', ''),
                kor_co_nm=item.get('kor_co_nm', ''),
                fin_prdt_nm=item.get('fin_prdt_nm', ''),
                join_way=item.get('join_way', ''),
                mtrt_int=item.get('mtrt_int', ''),
                spcl_cnd=item.get('spcl_cnd', ''),
                join_deny=int(item.get('join_deny', 1)),
                join_member=item.get('join_member', ''),
                etc_note=item.get('etc_note', ''),
                max_limit=item.get('max_limit', '없음'),
                dcls_strt_day=item.get('dcls_strt_day', ''),
                dcls_end_day=item.get('dcls_end_day', ''),
                fin_co_subm_day=item.get('fin_co_subm_day', '')
            )

    for item in deposit_option_list:
        if not DepositOptions.objects.filter(
            product__fin_prdt_cd=item['fin_prdt_cd'],
            save_trm=int(item.get('save_trm') or 0),
            intr_rate_type_nm=item.get('intr_rate_type_nm', '')
        ).exists():
            try:
                product = DepositProducts.objects.get(fin_prdt_cd=item['fin_prdt_cd'])
                DepositOptions.objects.create(
                    product=product,
                    save_trm=int(item.get('save_trm') or 0),
                    intr_rate_type_nm=item.get('intr_rate_type_nm', ''),
                    fin_prdt_cd=item.get('fin_prdt_cd', ''),
                    intr_rate_type=item.get('intr_rate_type', ''),
                    intr_rate=float(item.get('intr_rate') or -1),
                    intr_rate2=float(item.get('intr_rate2') or -1),
                )
            except DepositProducts.DoesNotExist:
                continue

    # 적금 상품 저장
    if not saving_data:
        return Response({'error': '적금상품 호출 실패'}, status=500)

    saving_base_list = saving_data.get('result', {}).get('baseList', [])
    saving_option_list = saving_data.get('result', {}).get('optionList', [])

    for item in saving_base_list:
        if not SavingProducts.objects.filter(fin_prdt_cd=item['fin_prdt_cd']).exists():
            SavingProducts.objects.create(
                fin_prdt_cd=item['fin_prdt_cd'],
                dcls_month=item.get('dcls_month', ''),
                fin_co_no=item.get('fin_co_no', ''),
                kor_co_nm=item.get('kor_co_nm', ''),
                fin_prdt_nm=item.get('fin_prdt_nm', ''),
                join_way=item.get('join_way', ''),
                mtrt_int=item.get('mtrt_int', ''),
                spcl_cnd=item.get('spcl_cnd', ''),
                join_deny=int(item.get('join_deny', 1)),
                join_member=item.get('join_member', ''),
                etc_note=item.get('etc_note', ''),
                max_limit=item.get('max_limit', '없음'),
                dcls_strt_day=item.get('dcls_strt_day', ''),
                dcls_end_day=item.get('dcls_end_day', ''),
                fin_co_subm_day=item.get('fin_co_subm_day', '')
            )

    for item in saving_option_list:
        if not SavingOptions.objects.filter(
            product__fin_prdt_cd=item['fin_prdt_cd'],
            save_trm=int(item.get('save_trm') or 0),
            intr_rate_type_nm=item.get('intr_rate_type_nm', ''),
            rsrv_type=item.get('rsrv_type', '')
        ).exists():
            try:
                product = SavingProducts.objects.get(fin_prdt_cd=item['fin_prdt_cd'])
                SavingOptions.objects.create(
                    product=product,
                    save_trm=int(item.get('save_trm') or 0),
                    intr_rate_type_nm=item.get('intr_rate_type_nm', ''),
                    fin_prdt_cd=item.get('fin_prdt_cd', ''),
                    intr_rate_type=item.get('intr_rate_type', ''),
                    rsrv_type=item.get('rsrv_type', ''),
                    rsrv_type_nm=item.get('rsrv_type_nm', ''),
                    intr_rate=float(item.get('intr_rate') or -1),
                    intr_rate2=float(item.get('intr_rate2') or -1),
                )
            except SavingProducts.DoesNotExist:
                continue

    return Response({'message': '예금 및 적금 상품과 옵션이 성공적으로 저장되었습니다.'})


# ✅ 기존 리스트 API 유지 (프론트 리스트 출력용)
@api_view(['GET', 'POST'])
def deposit_products(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def all_deposit_options(request):
    options = DepositOptions.objects.all()
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
    options = DepositOptions.objects.filter(product__fin_prdt_cd=fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def saving_products(request):
    if request.method == 'GET':
        products = SavingProducts.objects.all()
        serializer = SavingProductsSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SavingProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def all_saving_options(request):
    options = SavingOptions.objects.all()
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def saving_product_options(request, fin_prdt_cd):
    options = SavingOptions.objects.filter(product__fin_prdt_cd=fin_prdt_cd)
    serializer = SavingOptionsSerializer(options, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product_code(request):
    product_name = request.GET.get('product_name')
    product_type = request.GET.get('type')  # 'deposit' 또는 'saving'

    if not product_name or not product_type:
        return Response({'error': '필수 파라미터가 부족합니다.'}, status=400)

    # 모델 선택
    model = DepositProducts if product_type == 'deposit' else SavingProducts

    # 상품명으로 검색
    product = model.objects.filter(fin_prdt_nm=product_name).first()

    if product:
        return Response({'fin_prdt_cd': product.fin_prdt_cd})
    else:
        return Response({'error': '상품을 찾을 수 없습니다.'}, status=404)
