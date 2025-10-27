from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tenant
from .serializers import TenantSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def current(self, request):
        """Get current tenant information"""
        if hasattr(request, 'tenant'):
            serializer = self.get_serializer(request.tenant)
            return Response(serializer.data)
        return Response({'error': 'No tenant found'}, status=404)
