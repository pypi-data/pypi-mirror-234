from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from .models import Pessoa

PessoaSchema = pydantic_model_creator(Pessoa)


class TipoEnum(str, Enum):
    FISICA = "FISICA"
    JURIDICA = "JURIDICA"


class TipoDocumentoEnum(str, Enum):
    REGISTRO_GERAL = "REGISTRO_GERAL"
    INSCRICAO_ESTADUAL = "INSCRICAO_ESTADUAL"


class PessoaPayloadSchema(BaseModel):
    pai: Optional[int]
    cpf_cnpj: str
    documento: str = None
    email: Optional[str]
    nome: str
    nome_fantasia: str = None
    licenciavel: Optional[bool] = False
    principal: Optional[bool] = False
    tipo: TipoEnum
    tipo_documento: TipoDocumentoEnum = None


class PessoaResponseSchema(PessoaPayloadSchema):
    id: int


class TipoTelefoneEnum(str, Enum):
    RESIDENCIAL = "RESIDENCIAL"
    COMERCIAL = "COMERCIAL"
    CELULAR_PESSOAL = "CELULAR_PESSOAL"
    CELULAR_TRABALHO = "CELULAR_TRABALHO"


class InfoContatoPayloadSchema(BaseModel):
    email: Optional[str]
    pessoa_id: int
    telefone: Optional[str]
    tipo: Optional[TipoTelefoneEnum]


class InfoContatoResponseSchema(InfoContatoPayloadSchema):
    id: int


class PessoaMatrizSchema(PessoaResponseSchema):
    responsavel: str
    contatos: Optional[List[InfoContatoResponseSchema]]
