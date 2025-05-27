from rest_framework import serializers
from .models import DepositProducts, DepositOptions, SavingProducts, SavingOptions

class DepositProductsSerializer(serializers.ModelSerializer):
    highest_rate = serializers.SerializerMethodField()

    class Meta:
        model = DepositProducts
        fields = '__all__'  # 또는 필요한 필드만 명시
        read_only_fields = ['product']

    def get_highest_rate(self, obj):
        options = obj.depositoptions_set.all()
        if not options:
            return None
        return max(
            (opt.intr_rate2 for opt in options if opt.intr_rate2 is not None),
            default=None
        )


class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptions
        fields = '__all__'


class SavingProductsSerializer(serializers.ModelSerializer):
    highest_rate = serializers.SerializerMethodField()

    class Meta:
        model = SavingProducts
        fields = '__all__'
        read_only_fields = ['product']

    def get_highest_rate(self, obj):
        options = obj.savingoptions_set.all()
        if not options:
            return None
        return max(
            (opt.intr_rate2 for opt in options if opt.intr_rate2 is not None),
            default=None
        )


class SavingOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptions
        fields = '__all__'
