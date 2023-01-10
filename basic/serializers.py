from rest_framework import serializers

from basic import models


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    is_discountable = serializers.SerializerMethodField()

    def get_is_discountable(self, product):
        if product.price < 500000:
            return True

        return False

    class Meta:
        model = models.Product
        exclude = ('is_active', 'created_at', 'updated_at', 'amount')


class OrderLineSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = models.OrderLine
        fields = '__all__'
        read_only_fields = ('order',)


class OrderLineCreateSerializer(serializers.ModelSerializer):

    def validate(self, data):
        if data['product'].pk in self.context['exist_products']:
            raise serializers.ValidationError(
                {'product': 'This product already exist in order'}
            )

        return data

    def create(self, validated_data):
        order = self.context['order']
        validated_data['order'] = order
        order_line = super().create(validated_data)

        return order_line

    class Meta:
        model = models.OrderLine
        fields = '__all__'
        read_only_fields = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    order_lines = serializers.ListSerializer(child=OrderLineSerializer(), read_only=True)
    total = serializers.IntegerField(source='get_total_in_kzt', read_only=True)

    class Meta:
        model = models.Order
        exclude = ('currency',)
        read_only_fields = ('user',)
