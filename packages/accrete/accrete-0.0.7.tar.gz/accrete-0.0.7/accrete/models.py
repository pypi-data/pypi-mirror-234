from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from accrete.tenant import get_tenant


class TenantManager(models.Manager):

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = get_tenant()
        if tenant:
            queryset = queryset.filter(tenant=tenant)
        return queryset


class TenantModel(models.Model):

    class Meta:
        abstract = True

    tenant = models.ForeignKey(
        to='accrete.Tenant',
        on_delete=models.CASCADE
    )

    objects = TenantManager()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        tenant = get_tenant()
        if tenant is not None and self.tenant != tenant:
            raise ValueError('Current tenant differs from tenant of the record!')
        self.tenant = self.tenant or tenant
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class Tenant(models.Model):

    class Meta:
        verbose_name = _('Tenant')
        verbose_name_plural = _('Tenants')
        ordering = ['-is_active', 'name']
        db_table = 'accrete_tenant'

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255
    )

    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True
    )

    access_groups = models.ManyToManyField(
        to='accrete.AccessGroup',
        through='accrete.TenantAccessGroup',
        through_fields=('tenant', 'access_group')
    )

    def __str__(self):
        return self.name


class Member(models.Model):

    class Meta:
        verbose_name = _('Member')
        verbose_name_plural = _('Members')
        ordering = ['tenant', 'user']
        db_table = 'accrete_member'

    username_validator = UnicodeUsernameValidator()

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        related_name='memberships',
        on_delete=models.PROTECT
    )

    tenant = models.ForeignKey(
        to='accrete.Tenant',
        related_name='members',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=150,
        help_text=_(
            '150 characters or fewer.'
            'Letters, digits and @/./+/-/_ only.'
        ),
        blank=True,
        null=True,
        validators=[username_validator],
    )

    is_active = models.BooleanField(
        verbose_name=_('Active'),
        default=True
    )

    access_groups = models.ManyToManyField(
        to='accrete.AccessGroup',
        through='accrete.AccessGroupMember',
        through_fields=('member', 'access_group')
    )

    objects = TenantManager()

    def __str__(self):
        return f'{self.name or self.user}'


class AccessGroup(models.Model):

    class Meta:
        verbose_name = _('Access Group')
        verbose_name_plural = _('Access Groups')
        ordering = ['name']
        db_table = 'accrete_access_group'
        constraints = [
            models.UniqueConstraint(
                name='unique_code',
                fields=['code']
            )
        ]

    name = models.CharField(
        verbose_name=_('Name'),
        max_length=255
    )

    code = models.CharField(
        verbose_name=_('Code'),
        max_length=50
    )

    is_public = models.BooleanField(
        verbose_name=_('Is Public'),
        default=True,
        help_text=_(
            'If set, members from all tenants can be assigned to this group.'
        )
    )

    def __str__(self):
        return self.name


class AccessGroupMember(models.Model):

    class Meta:
        verbose_name = _('Access Group Member')
        verbose_name_plural = _('Access Group Members')
        ordering = ['member']
        db_table = 'accrete_access_group_member_rel'
        constraints = [
            models.UniqueConstraint(
                name='unique_member_per_group',
                fields=['member', 'access_group']
            )
        ]

    member = models.ForeignKey(
        to='accrete.Member',
        on_delete=models.CASCADE
    )

    access_group = models.ForeignKey(
        to='accrete.AccessGroup',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.member} - {self.access_group}'


class TenantAccessGroup(models.Model):

    class Meta:
        verbose_name = _('Tenant Access Group')
        verbose_name_plural = _('Tenant Access Groups')
        ordering = ['tenant']
        db_table = 'accrete_tenant_access_group_rel'
        constraints = [
            models.UniqueConstraint(
                name='unique_tenant_per_group',
                fields=['tenant', 'access_group']
            )
        ]

    tenant = models.ForeignKey(
        to='accrete.Tenant',
        on_delete=models.CASCADE
    )

    access_group = models.ForeignKey(
        to='accrete.AccessGroup',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.tenant} - {self.access_group}'
