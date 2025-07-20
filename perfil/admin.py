from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")
    search_fields = ("user__username", "user__email", "phone_number")
    list_filter = ("user__is_active", "user__is_staff")
    ordering = ("user__username",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user")
