from typing import List

from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import File, Query
from ninja.errors import HttpError
from ninja.files import UploadedFile
from ninja_extra import NinjaExtraAPI, api_controller, route

from deg.permissions import HasAPIKey
from perfil.schemas import PerfilOut, UsuarioOut
from solicitacao.models import AnexoSolicitacao, SolicitacaoOrcamento
from solicitacao.schemas import SolicitacaoOrcamentoIn, SolicitacaoOrcamentoOut

api = NinjaExtraAPI()


@api_controller("/usuarios", tags=["Usuarios"], auth=HasAPIKey())
class UsuarioController:

    @route.get("/", response=list[UsuarioOut])
    def listar_usuarios(self):
        user_model = get_user_model()
        usuarios = user_model.objects.select_related("perfil").all()
        return [
            UsuarioOut(
                id=u.id,
                username=u.username,
                email=u.email,
                first_name=u.first_name,
                last_name=u.last_name,
                perfil=PerfilOut(
                    phone_number=u.perfil.phone_number if u.perfil else None,
                    codigo_vendedor=u.perfil.codigo_vendedor if u.perfil else None,
                ),
            )
            for u in usuarios
        ]

    @route.get("/vendedor/{phone}", response=UsuarioOut)
    def listar_por_telefone(self, phone: str):

        user_model = get_user_model()
        try:
            usuario = user_model.objects.select_related("perfil").get(
                perfil__phone_number=phone
            )
        except user_model.DoesNotExist:
            raise HttpError(
                404, f"Usuário com telefone {phone} não encontrado"
            )

        return UsuarioOut(
            id=usuario.id,
            username=usuario.username,
            email=usuario.email,
            first_name=usuario.first_name,
            last_name=usuario.last_name,
            perfil=PerfilOut(
                phone_number=usuario.perfil.phone_number if usuario.perfil else None,
                codigo_vendedor=(
                    usuario.perfil.codigo_vendedor if usuario.perfil else None
                ),
            ),
        )


@api_controller("/solicitacoes", tags=["Solicitações"], auth=HasAPIKey())
class SolicitacaoOrcamentoController:

    @route.get("/", response=List[SolicitacaoOrcamentoOut])
    def listar(self):
        return (
            SolicitacaoOrcamento.objects.prefetch_related("anexos")
            .all()
            .order_by("-criado_em")
        )

    @route.get("/listar-por-vendedor", response=list[SolicitacaoOrcamentoOut])
    def listar_por_codigo_vendedor(
        self,
        codigo_vendedor: str = Query(..., description="Código do vendedor (Perfil)"),
        numero: str | None = Query(None, description="Número da solicitação"),
        cliente: str | None = Query(None, description="Nome do cliente"),
    ):
        queryset = SolicitacaoOrcamento.objects.filter(
            vendedor__perfil__codigo_vendedor=codigo_vendedor
        )

        if numero:
            queryset = queryset.filter(numero__icontains=numero)

        if cliente:
            queryset = queryset.filter(cliente__icontains=cliente)

        return queryset.select_related("vendedor", "vendedor__perfil").prefetch_related(
            "anexos"
        )

    @route.get("/{solicitacao_id}/", response=SolicitacaoOrcamentoOut)
    def obter(self, solicitacao_id: int):
        return get_object_or_404(
            SolicitacaoOrcamento.objects.prefetch_related("anexos"), pk=solicitacao_id
        )

    @route.post("/", response=SolicitacaoOrcamentoOut)
    def criar(self, request, data: SolicitacaoOrcamentoIn):
        s = SolicitacaoOrcamento.objects.create(
            vendedor=request.user,
            cliente=data.cliente,
            descricao=data.descricao,
            observacoes=data.observacoes,
        )
        return s

    @route.patch("/{solicitacao_id}/", response=SolicitacaoOrcamentoOut)
    def atualizar(self, solicitacao_id: int, data: SolicitacaoOrcamentoIn):
        s = get_object_or_404(SolicitacaoOrcamento, pk=solicitacao_id)
        for field in ["cliente", "descricao", "observacoes"]:
            value = getattr(data, field, None)
            if value is not None:
                setattr(s, field, value)
        s.save()
        return s

    @route.post("/{solicitacao_id}/anexos/")
    @transaction.atomic
    def upload_anexo(self, solicitacao_id: int, arquivo: UploadedFile = File(...)):
        s = get_object_or_404(SolicitacaoOrcamento, pk=solicitacao_id)
        anexo = AnexoSolicitacao.objects.create(solicitacao=s, arquivo=arquivo)
        return anexo


api.register_controllers(UsuarioController, SolicitacaoOrcamentoController)
