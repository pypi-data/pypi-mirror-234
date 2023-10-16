import asyncio
from typing import List, Union

from fastapi import HTTPException
from openpyxl import Workbook
from pydantic.error_wrappers import ValidationError

from src.app.config import Settings, get_settings
from src.epona.auth.schemas import UserSchema

from .models import InfoContato, Pessoa
from .schemas import (InfoContatoPayloadSchema, InfoContatoResponseSchema,
                      PessoaPayloadSchema, PessoaResponseSchema, PessoaSchema)

settings: Settings = get_settings()
limit = settings.limit
env = settings.environment


async def post(payload: PessoaPayloadSchema, user: UserSchema) -> int:
    """Cria e salva uma pessoa ou empresa no banco de dados e retorna seu id"""
    pessoa = Pessoa(
        client_id=user.client_id,
        pessoa_id=payload.pai,
        cpf_cnpj=payload.cpf_cnpj,
        email=payload.email,
        nome=payload.nome,
        tipo=payload.tipo,
        tipo_documento=payload.tipo_documento,
        documento=payload.documento,
        nome_fantasia=payload.nome_fantasia,
    )
    if env == "prod" and not validate_cpf_cnpj(pessoa):
        cpf_cnpj = "CPF" if pessoa.tipo == "FISICA" else "CNPJ"
        raise HTTPException(422, f"{cpf_cnpj} inválido")
    if payload.licenciavel and payload.tipo == "JURIDICA":
        pessoa.licenciavel = payload.licenciavel
    if payload.principal and payload.tipo == "JURIDICA":
        pessoa.principal = payload.principal
    try:
        await pessoa.save()
    except Exception as err:
        print(err)
    return pessoa.id


async def update(payload: PessoaPayloadSchema, user: UserSchema) -> Union[int, None]:
    """Altera as informações de uma pessoa ou empresa e retorna seu id"""
    pessoa = await Pessoa.filter(
        cpf_cnpj=payload.cpf_cnpj, client_id=user.client_id
    ).first()
    if not pessoa:
        return None
    pessoa.nome = payload.nome if payload.nome else pessoa.nome
    pessoa.cpf_cnpj = payload.cpf_cnpj if payload.cpf_cnpj else pessoa.cpf_cnpj
    pessoa.email = payload.email if payload.email else pessoa.email
    pessoa.documento = payload.documento if payload.documento else pessoa.documento
    pessoa.tipo_documento = (
        payload.tipo_documento if payload.tipo_documento else pessoa.tipo_documento
    )
    pessoa.nome_fantasia = (
        payload.nome_fantasia if payload.nome_fantasia else pessoa.nome_fantasia
    )
    if payload.tipo == "JURIDICA":
        if payload.licenciavel is True:
            pessoa.licenciavel = True
        if payload.principal is True:
            pessoa.principal = True

    await pessoa.save()
    return pessoa.id


async def save_xlsx(wb: Workbook, user: UserSchema) -> List[PessoaResponseSchema]:
    """Salva pessoas a partir de uma planilha xlsx"""
    await asyncio.sleep(0)
    pessoas = []
    try:
        for i, line in enumerate(wb["Pessoas"].iter_rows()):
            if i == 0 or not line[0].value:
                continue
            payload = PessoaPayloadSchema(
                **{
                    "cpf_cnpj": str(line[0].value).strip(),
                    "nome": line[1].value.strip(),
                    "tipo_documento": line[2].value,
                    "documento": line[3].value,
                    "tipo": line[4].value,
                    "email": line[5].value,
                    "nome_fantasia": line[6].value,
                    "licenciavel": line[7].value,
                    "principal": line[8].value,
                }
            )
            if env == "prod" and not validate_cpf_cnpj(payload):
                raise ValueError
            pessoas.append(payload)
    except (ValueError, KeyError, ValidationError):
        raise ValueError(
            f"Erro na linha {i+1}. Verifique se todas a colunas estão"
            f"preenchidas e com valores válidos, inclusive CPF/CNPJ"
        )
    except IndexError:
        raise ValueError(
            "Número de colunas na planilha é menor que o esperado. "
            "Utilize o arquivo modelo."
        )
    armazenadas = []
    for pessoa in pessoas:
        result = await post(pessoa, user)
        if result:
            armazenadas.append(PessoaResponseSchema(**{"id": result, **pessoa.dict()}))
    return armazenadas


async def get(pk: int, user: UserSchema) -> Union[PessoaSchema, None]:
    """retorna informações de uma pessoa ou empresa filtrada por id"""
    pessoa = await Pessoa.filter(id=pk, client_id=user.client_id).first()
    if not pessoa:
        return None
    return PessoaSchema(**dict(pessoa))


async def get_all(user: UserSchema) -> List:
    """retorna todas as pessoas e empresas vinculádas a um client_id"""
    pessoas = (
        await Pessoa.filter(client_id=user.client_id)
        .all()
        .order_by("-created_at")
        .limit(limit)
        .values()
    )
    pessoas_list = [pessoa for pessoa in pessoas]
    return pessoas_list


async def delete(pk: int, user: UserSchema) -> bool:
    """apaga uma pessoa ou empresa do banco por id"""
    pessoa = await Pessoa.filter(id=pk, client_id=user.client_id).first()
    if pessoa:
        await pessoa.delete()
        return True
    return False


async def by_name(nome: str, user: UserSchema) -> List:
    """Filtra pessoas por nome"""
    pessoas = await Pessoa.filter(nome__icontains=nome, client_id=user.client_id).all()
    pessoas_list = [pessoa for pessoa in pessoas]

    return pessoas_list


async def by_cpf_cnpj(cpf_cnpj: str, user: UserSchema) -> Union[Pessoa, None]:
    """Filtra pessoas ou empresas pelo cpf ou cnpj"""
    pessoa = await Pessoa.filter(cpf_cnpj=cpf_cnpj, client_id=user.client_id).first()
    if not pessoa:
        return None
    return pessoa


async def find_principal(
    empresa_id: int, user: UserSchema
) -> Union[PessoaResponseSchema, None]:
    """Filtra empresas e retorna sua principal"""
    empresa = await Pessoa.filter(id=empresa_id, client_id=user.client_id).first()
    if not empresa:
        return None
    if empresa.principal:
        return PessoaResponseSchema(**dict(empresa))
    return await find_principal(empresa.pessoa_id, user)


async def save_contato(
    pk: int, payload: InfoContatoPayloadSchema, user: UserSchema
) -> Union[InfoContatoResponseSchema, None]:
    """Salva e atualiza informações de contato de uma pessoa"""
    if pk > 0:
        info_contato = await InfoContato.filter(id=pk, client_id=user.client_id).first()
        if not info_contato:
            return None
        info_contato.email = payload.email
        info_contato.telefone = payload.telefone
        info_contato.tipo = payload.tipo
    else:
        info_contato = InfoContato(
            client_id=user.client_id,
            email=payload.email,
            pessoa_id=payload.pessoa_id,
            telefone=payload.telefone,
            tipo=payload.tipo,
        )
    await info_contato.save()
    if not info_contato.id > 0:
        return None
    return InfoContatoResponseSchema(**dict(info_contato))


async def get_contato(
    pk: int, user: UserSchema
) -> Union[InfoContatoResponseSchema, None]:
    """Retorna as informççoes de contato de uma pessoa por id"""
    info_contato = await InfoContato.filter(id=pk, client_id=user.client_id).first()
    if not info_contato:
        return None
    return InfoContatoResponseSchema(**dict(info_contato))


async def get_contato_all(
    pessoa_id: int, user: UserSchema
) -> Union[List[InfoContatoResponseSchema], None]:
    """Retorna todas os contatos vinculados a uma pessoa"""
    infos_contato = await InfoContato.filter(
        pessoa_id=pessoa_id, client_id=user.client_id
    ).all()
    if not infos_contato:
        return None
    return [InfoContatoResponseSchema(**dict(info)) for info in infos_contato]


async def delete_contato(pk: int, user: UserSchema) -> bool:
    """Apaga as informações de contato de uma pessoa por id"""
    info_contato = await InfoContato.filter(id=pk, client_id=user.client_id).first()
    if not info_contato:
        return False
    result = await info_contato.delete()
    if result:
        return False
    return True


def validate_cpf_cnpj(pessoa: Pessoa) -> bool:
    """Filtra cpf ou cnpf e valida o número"""
    if pessoa.tipo == "FISICA":
        return validate_cpf(pessoa.cpf_cnpj)
    return validate_cnpj(pessoa.cpf_cnpj)


def validate_cpf(cpf: str) -> bool:
    """Verifica se a string é um cpf válido"""
    try:
        if len(cpf) != 11:
            return False
        base = cpf[:9]
        dv = cpf[9:]
        same_digit = True
        for i, digit in enumerate(base):
            if i < len(base) - 1 and digit != base[i + 1]:
                same_digit = False
                break
        if same_digit:
            return False
        dv1_sum = 0
        for i in range(len(base)):
            dv1_sum += int(base[i]) * (10 - i)
        dv1_mod = dv1_sum % 11
        dv1 = str(11 - dv1_mod) if 11 - dv1_mod < 10 else "0"
        base2 = base + dv1
        dv2_sum = 0
        for i in range(len(base2)):
            dv2_sum += int(base2[i]) * (11 - i)
        dv2_mod = dv2_sum % 11
        dv2 = str(11 - dv2_mod) if 11 - dv2_mod < 10 else "0"
        return dv[0] == dv1 and dv[1] == dv2
    except (IndexError, ValueError):
        return False


def validate_cnpj(cnpj: str) -> bool:
    """Verifica se a string é um cnpj válido"""
    try:
        if len(cnpj) != 14:
            return False
        base = cnpj[:12]
        dv = cnpj[12:]
        # cada digito do cnpj tem um peso
        weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        dv1_sum = 0
        for i in range(len(weights)):
            dv1_sum += int(base[i]) * weights[i]
        dv1_mod = dv1_sum % 11
        dv1 = str(11 - dv1_mod) if 11 - dv1_mod < 10 else "0"
        # como mais um digito vai ser validado, eh incluido mais um peso a lista
        weights.insert(0, 6)  #
        base2 = base + dv1
        dv2_sum = 0
        for i in range(len(weights)):
            dv2_sum += int(base2[i]) * weights[i]
        dv2_mod = dv2_sum % 11
        dv2 = str(11 - dv2_mod) if 11 - dv2_mod < 10 else "0"
        return dv[0] == dv1 and dv[1] == dv2
    except (IndexError, ValueError):
        return False
