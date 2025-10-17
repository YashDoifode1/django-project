from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'website', 'joined_at')
    search_fields = ('user__username', 'location', 'website')
    list_filter = ('joined_at',)
    readonly_fields = ('joined_at',)
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'profile_image', 'bio')
        }),
        ('Additional Info', {
            'fields': ('website', 'location', 'joined_at')
        }),
    )

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="60" height="60" style="border-radius:50%;" />', obj.profile_image.url)
        return "-"
    profile_image_preview.short_description = 'Profile Image'
