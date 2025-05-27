from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import UserProfile
from .serializers import UserProfileSerializer

from finance.models import DepositProducts, SavingProducts


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_profile(request):
    if UserProfile.objects.filter(user=request.user).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    serializer = UserProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if not profile:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(profile, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if profile is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def like_deposit(request, product_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    try:
        product = DepositProducts.objects.get(fin_prdt_cd=product_id)
    except DepositProducts.DoesNotExist:
        try:
            product = DepositProducts.objects.get(fin_prdt_nm=product_id)
        except DepositProducts.DoesNotExist:
            return Response({'error': '예금 상품을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        user_profile.liked_deposits.add(product)
        return Response({'message': '예금 상품이 관심 목록에 추가되었습니다.'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user_profile.liked_deposits.remove(product)
        return Response({'message': '예금 상품이 관심 목록에서 삭제되었습니다.'}, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def like_saving(request, product_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    try:
        product = SavingProducts.objects.get(fin_prdt_cd=product_id)
    except SavingProducts.DoesNotExist:
        try:
            product = SavingProducts.objects.get(fin_prdt_nm=product_id)
        except SavingProducts.DoesNotExist:
            return Response({'error': '적금 상품을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        user_profile.liked_savings.add(product)
        return Response({'message': '적금 상품이 관심 목록에 추가되었습니다.'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user_profile.liked_savings.remove(product)
        return Response({'message': '적금 상품이 관심 목록에서 삭제되었습니다.'}, status=status.HTTP_200_OK)
