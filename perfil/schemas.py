from typing import Optional

from ninja import Schema


class PerfilOut(Schema):
    codigo_vendedor: str
    phone_number: Optional[str]


class UsuarioOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    perfil: PerfilOut
