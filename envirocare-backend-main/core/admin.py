from django.contrib import admin
from .models.envirocare import Organisation, Complaint, Comment

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'approved', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('approved', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('approved',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('ref', 'description', 'severity', 'is_resolved', 'reported_by_name', 'created_at')
    search_fields = ('ref', 'description', 'reported_by_name')
    list_filter = ('severity', 'is_resolved', 'created_at')
    ordering = ('-created_at',)
    list_editable = ('is_resolved',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ref', 'description', 'commented_by_name', 'created_at')
    search_fields = ('ref', 'description', 'commented_by_name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)