from django.contrib import admin

from .models import ApprovalCodeEmailLog


@admin.register(ApprovalCodeEmailLog)
class ApprovalCodeEmailLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'credit_id', 'approval_code', 'credit_value', 'email_to', 'sent_at', 'success')
    list_filter = ('success', 'sent_at')
    search_fields = ('email_to', 'approval_code', 'user__first_name', 'user__document_number')
    readonly_fields = ('user', 'credit_id', 'approval_code', 'credit_value', 'email_to', 'sent_at', 'success')
    date_hierarchy = 'sent_at'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
