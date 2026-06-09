from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product, Review


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, min_length=1, max_length=100)

    def validate_name(self, name):
        if not name or name.strip() == '':
            raise ValidationError('Название категории не может быть пустым!')
        return name


class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# ============= PRODUCT SERIALIZERS =============

class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=1, max_length=200)
    description = serializers.CharField(required=True, min_length=1)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField(required=True)

    def validate_title(self, title):
        if not title or title.strip() == '':
            raise ValidationError('Название товара не может быть пустым!')
        return title

    def validate_description(self, description):
        if not description or description.strip() == '':
            raise ValidationError('Описание товара не может быть пустым!')
        return description

    def validate_price(self, price):
        if price <= 0:
            raise ValidationError('Цена должна быть больше нуля!')
        return price

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError('Категория с таким ID не существует!')
        return category_id


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# ============= REVIEW SERIALIZERS =============

class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=1)
    stars = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)

    def validate_text(self, text):
        if not text or text.strip() == '':
            raise ValidationError('Текст отзыва не может быть пустым!')
        return text

    def validate_stars(self, stars):
        # Проверка диапазона оценки (обычно 1-5)
        if stars < 1 or stars > 5:
            raise ValidationError('Оценка должна быть от 1 до 5!')
        return stars

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('Товар с таким ID не существует!')
        return product_id


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0.0
        total_stars = sum([review.stars for review in reviews])
        return round(total_stars / len(reviews), 2)