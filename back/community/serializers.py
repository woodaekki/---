from rest_framework import serializers
from .models import Community, Review, FixedCommunity


# community/serializers.py
class CommunityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ('id', 'title', 'content', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    # 유저 id가 아니라 유저명이 뜨도록 하는 함수 !!!
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'community', 'created_at', 'updated_at')

# community/serializers.py
class CommunitySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Community
        fields = '__all__'
        read_only_fields = ('user',)

class FixedCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedCommunity
        fields = '__all__'