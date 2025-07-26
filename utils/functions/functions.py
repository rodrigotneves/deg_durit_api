import os
import re


def anexo_upload_path(instance, filename):
    """
    Salva o arquivo na pasta: solicitacoes/<numero da SO>/<nome do arquivo>
    Ex: solicitacoes/25-00001/orcamento.pdf
    """
    numero_so = instance.solicitacao.numero or "sem-numero"
    numero_so = numero_so.replace("/", "-")  # Ex: 25/00001 → 25-00001
    return os.path.join("solicitacoes", numero_so, filename)


def normalizar_telefone(phone: str) -> str:
    phone = phone.strip()
    digitos = re.sub(r"\D", "", phone)

    # Se já começa com "+", apenas limpa o restante
    if phone.startswith("+"):
        return "+" + digitos
    # Caso contrário, adiciona o "+" na frente
    return "+" + digitos
