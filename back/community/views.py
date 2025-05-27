from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

from .models import Community, Review, FixedCommunity
from .serializers import CommunityListSerializer, CommunitySerializer, ReviewSerializer, FixedCommunitySerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = Community.objects.all().order_by('-created_at')  # 전체 게시글
        serializer = CommunityListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_pk):
    article = get_object_or_404(Community, pk=article_pk)

    if request.method == 'GET':
        serializer = CommunitySerializer(article)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if article.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = CommunitySerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        if article.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, community_pk):
    community = get_object_or_404(Community, pk=community_pk)
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, community=community)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, community_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk, community_id=community_pk)
    if review.user != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def fixed_article_list(request):
    articles = FixedCommunity.objects.all()
    serializer = FixedCommunitySerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def fixed_article_detail(request, pk):
    article = get_object_or_404(FixedCommunity, pk=pk)
    serializer = FixedCommunitySerializer(article)
    return Response(serializer.data)