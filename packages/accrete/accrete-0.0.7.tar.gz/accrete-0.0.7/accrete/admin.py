from django.contrib import admin
from . import models


class MemberInLine(admin.TabularInline):

    model = models.Member


class TenantAccessGroupInLine(admin.TabularInline):

    model = models.TenantAccessGroup


class AccessGroupMemberInLine(admin.TabularInline):

    model = models.AccessGroupMember


class TenantAdmin(admin.ModelAdmin):

    model = models.Tenant
    list_display = ('name', 'is_active', 'pk')
    search_fields = ('pk', 'name')
    list_filter = ['is_active']
    inlines = [MemberInLine, TenantAccessGroupInLine]


class MemberAdmin(admin.ModelAdmin):

    model = models.Member
    list_display = ('user', 'tenant', 'is_active')
    search_fields = ('user__email', 'tenant__name')
    list_filter = ['is_active']
    inlines = [AccessGroupMemberInLine]


class AccessGroupAdmin(admin.ModelAdmin):

    model = models.AccessGroup
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    inlines = [AccessGroupMemberInLine]


admin.site.register(models.Tenant, TenantAdmin)
admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.AccessGroup, AccessGroupAdmin)
admin.site.register(models.AccessGroupMember)
