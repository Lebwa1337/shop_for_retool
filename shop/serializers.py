from rest_framework import serializers

from shop.models import Product, Characteristic, ProductCharacteristic, Order


class CharacteristicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Characteristic
        fields = ['id', 'name']


class ProductCharacteristicSerializer(serializers.ModelSerializer):
    characteristic = CharacteristicSerializer()

    class Meta:
        model = ProductCharacteristic
        fields = ['id', 'characteristic', 'value']


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    product_characteristics = ProductCharacteristicSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand', 'category', 'price', 'product_characteristics']

    def create(self, validated_data):
        characteristics_data = validated_data.pop('product_characteristics')
        product = Product.objects.create(**validated_data)
        for characteristic_data in characteristics_data:
            characteristic, created = Characteristic.objects.get_or_create(name=characteristic_data['characteristic']['name'])
            ProductCharacteristic.objects.create(product=product, characteristic=characteristic, value=characteristic_data['value'])
        return product

    def update(self, instance, validated_data):
        characteristics_data = validated_data.pop('product_characteristics')
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.category = validated_data.get('category', instance.category)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        for characteristic_data in characteristics_data:
            characteristic, created = Characteristic.objects.get_or_create(name=characteristic_data['characteristic']['name'])
            product_characteristic, created = ProductCharacteristic.objects.update_or_create(
                product=instance, characteristic=characteristic, defaults={'value': characteristic_data['value']}
            )
        return instance


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source='brand.name', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'brand', 'category', 'price', 'characteristics', 'image']


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'products']


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    products = ProductOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'products', 'user', 'date']


class OrderRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    products = ProductListSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'products', 'user', 'date']
