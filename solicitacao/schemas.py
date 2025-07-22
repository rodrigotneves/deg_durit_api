from datetime import datetime
from typing import List, Optional

from ninja import Schema
from ninja.files import UploadedFile


class AnexoOut(Schema):
    id: int
    arquivo: str  # URL para o download
    enviado_em: datetime


class SolicitacaoOrcamentoOut(Schema):
    id: int
    numero: str
    vendedor_id: int
    cliente: str
    descricao: str
    status: str
    observacoes: Optional[str]
    criado_em: datetime
    atualizado_em: datetime
    anexos: List[AnexoOut] = []


class SolicitacaoOrcamentoIn(Schema):
    cliente: str
    descricao: str
    observacoes: Optional[str] = None


class AnexoIn(Schema):
    solicitacao_id: int
    arquivo: UploadedFile
