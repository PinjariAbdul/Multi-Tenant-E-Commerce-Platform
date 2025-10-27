from django.core.exceptions import ImproperlyConfigured
from .models import Tenant


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get tenant from subdomain or header
        host = request.get_host().split(':')[0]  # Remove port if present
        subdomain = host.split('.')[0] if '.' in host else None

        # Try to find tenant by subdomain
        if subdomain and subdomain != 'www':
            try:
                tenant = Tenant.objects.get(domain=subdomain)
                request.tenant = tenant
            except Tenant.DoesNotExist:
                # If subdomain doesn't match, try header
                tenant_header = request.META.get('HTTP_X_TENANT_ID')
                if tenant_header:
                    try:
                        tenant = Tenant.objects.get(id=tenant_header)
                        request.tenant = tenant
                    except (Tenant.DoesNotExist, ValueError):
                        pass
        else:
            # Try header for main domain
            tenant_header = request.META.get('HTTP_X_TENANT_ID')
            if tenant_header:
                try:
                    tenant = Tenant.objects.get(id=tenant_header)
                    request.tenant = tenant
                except (Tenant.DoesNotExist, ValueError):
                    pass

        response = self.get_response(request)
        return response
