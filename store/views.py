from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        """
        All authenticated users can list/retrieve products
        Only staff and owners can create/update/delete products
        """
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # Only staff and owners can create products
        if request.user.role not in ['staff', 'owner']:
            return Response(
                {'detail': 'Only staff and owners can create products'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Only staff and owners can update products
        if request.user.role not in ['staff', 'owner']:
            return Response(
                {'detail': 'Only staff and owners can update products'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        # Only staff and owners can partially update products
        if request.user.role not in ['staff', 'owner']:
            return Response(
                {'detail': 'Only staff and owners can update products'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Only staff and owners can delete products
        if request.user.role not in ['staff', 'owner']:
            return Response(
                {'detail': 'Only staff and owners can delete products'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        # Only return products for the current user's tenant
        return Product.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Set the tenant automatically based on the current user
        serializer.save(tenant=self.request.user.tenant)


class CustomerOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_permissions(self):
        """
        Customer-specific permissions for orders
        """
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Customers can only see their own orders
        return Order.objects.filter(tenant=self.request.user.tenant, customer=self.request.user)

    def perform_create(self, serializer):
        # Set the tenant and customer automatically
        serializer.save(tenant=self.request.user.tenant, customer=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        """
        Order permissions:
        - Customers can create orders
        - Staff/Owners can update orders
        - All authenticated users can view orders
        """
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # Only customers can create orders
        if request.user.role != 'customer':
            return Response(
                {'detail': 'Only customers can place orders'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        # Only staff and owners can update orders
        if request.user.role not in ['staff', 'owner']:
            return Response(
                {'detail': 'Only staff and owners can update orders'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        # Only staff and owners can partially update orders
        if request.user.role not in ['staff', 'owner']:
            return Response(
                {'detail': 'Only staff and owners can update orders'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        # Only staff and owners can delete orders
        if request.user.role not in ['staff', 'owner']:
            return Response(
                {'detail': 'Only staff and owners can delete orders'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            # Customers can only see their own orders
            return Order.objects.filter(tenant=user.tenant, customer=user)
        else:
            # Staff and owners can see all orders for their tenant
            return Order.objects.filter(tenant=user.tenant)

    def perform_create(self, serializer):
        # Set the tenant and customer automatically based on the current user
        serializer.save(tenant=self.request.user.tenant, customer=self.request.user)