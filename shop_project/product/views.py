from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Category, Product, Review
from .serializers import (
    CategoryListSerializer, CategoryDetailSerializer, CategoryValidateSerializer,
    ProductListSerializer, ProductDetailSerializer, ProductValidateSerializer,
    ReviewListSerializer, ReviewDetailSerializer, ReviewValidateSerializer,
    ProductReviewsSerializer
)


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryValidateSerializer
        return CategoryListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            category = serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=CategoryDetailSerializer(category).data
        )


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CategoryValidateSerializer
        return CategoryDetailSerializer

    def update(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data['name']
        category.save()
        return Response(
            status=status.HTTP_200_OK,
            data=CategoryDetailSerializer(category).data
        )

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        return Response(data=CategoryDetailSerializer(category).data)

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductValidateSerializer
        return ProductListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            product = serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ProductDetailSerializer(product).data
        )


class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ProductValidateSerializer
        return ProductDetailSerializer

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        product.title = vd['title']
        product.description = vd['description']
        product.price = vd['price']
        product.category_id = vd['category_id']
        product.save()
        return Response(
            status=status.HTTP_200_OK,
            data=ProductDetailSerializer(product).data
        )

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        return Response(data=ProductDetailSerializer(product).data)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ReviewValidateSerializer
        return ReviewListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            review = serializer.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ReviewDetailSerializer(review).data
        )


class ReviewDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ReviewValidateSerializer
        return ReviewDetailSerializer

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vd = serializer.validated_data
        review.text = vd['text']
        review.stars = vd['stars']
        review.product_id = vd['product_id']
        review.save()
        return Response(
            status=status.HTTP_200_OK,
            data=ReviewDetailSerializer(review).data
        )

    def retrieve(self, request, *args, **kwargs):
        review = self.get_object()
        return Response(data=ReviewDetailSerializer(review).data)

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductReviewsListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductReviewsSerializer
    pagination_class = CustomPagination