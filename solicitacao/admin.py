from django.contrib import admin

from .models import AnexoSolicitacao, SolicitacaoOrcamento


class AnexoSolicitacaoInline(admin.TabularInline):
    model = AnexoSolicitacao
    extra = 1
    fields = ["arquivo", "enviado_em"]
    readonly_fields = ["enviado_em"]
    show_change_link = True


@admin.register(SolicitacaoOrcamento)
class SolicitacaoOrcamentoAdmin(admin.ModelAdmin):
    list_display = ["numero", "cliente", "vendedor", "status", "criado_em"]
    list_filter = ["status", "criado_em", "vendedor__username", "cliente"]
    search_fields = ["numero", "cliente", "descricao", "vendedor__username"]
    readonly_fields = ["numero", "criado_em", "atualizado_em"]
    inlines = [AnexoSolicitacaoInline]


@admin.register(AnexoSolicitacao)
class AnexoSolicitacaoAdmin(admin.ModelAdmin):
    list_display = ["__str__", "solicitacao", "enviado_em"]
    readonly_fields = ["enviado_em"]
