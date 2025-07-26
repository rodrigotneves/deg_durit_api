import os

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

from utils.functions.functions import anexo_upload_path

User = get_user_model()


class SolicitacaoOrcamento(models.Model):
    numero = models.CharField(
        "Número da Solicitação", max_length=10, unique=True, blank=True
    )
    vendedor = models.ForeignKey(
        User,
        verbose_name="Vendedor",
        on_delete=models.PROTECT,
        related_name="solicitacoes_orcamento",
    )
    cliente = models.CharField("Nome do Cliente", max_length=100)
    descricao = models.TextField("Descrição da Solicitação")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    STATUS_CHOICES = [
        ("aberta", "Aberta"),
        ("declinada", "Declinada"),
        ("finalizada", "Finalizada"),
    ]
    status = models.CharField(
        "Status", max_length=20, choices=STATUS_CHOICES, default="aberta"
    )

    observacoes = models.TextField(
        "Observações Internas", blank=True, null=True
    )  # noqa: E501

    def __str__(self):
        return f"{self.cliente} ({self.vendedor}) - {self.status}"

    def save(self, *args, **kwargs):
        if not self.numero:
            ano = now().year % 100  # 2025 → 25
            prefixo = f"{ano:02d}"

            # Conta quantas solicitações existem com o mesmo ano
            ultimo = (
                SolicitacaoOrcamento.objects.filter(numero__startswith=prefixo)
                .order_by("-numero")
                .first()
            )

            if ultimo and "-" in ultimo.numero:
                ultimo_seq = int(ultimo.numero.split("-")[1])
            else:
                ultimo_seq = 0

            proximo_seq = ultimo_seq + 1
            self.numero = f"{prefixo}-{proximo_seq:05d}"

        super().save(*args, **kwargs)


class AnexoSolicitacao(models.Model):
    solicitacao = models.ForeignKey(
        "SolicitacaoOrcamento",
        on_delete=models.CASCADE,
        related_name="anexos",
        verbose_name="Solicitação",
    )
    arquivo = models.FileField("Arquivo", upload_to=anexo_upload_path)

    enviado_em = models.DateTimeField("Enviado em", auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.arquivo.name)
