from tortoise import fields, models


class Pessoa(models.Model):
    id = fields.IntField(pk=True)
    client_id = fields.CharField(max_length=50, null=True)
    pessoa_id = fields.IntField(null=True)
    cpf_cnpj = fields.CharField(max_length=15)
    email = fields.CharField(max_length=100, null=True)
    nome = fields.CharField(max_length=100)
    tipo = fields.CharField(max_length=20)
    licenciavel = fields.BooleanField(default=False)
    principal = fields.BooleanField(default=False)
    tipo_documento = fields.CharField(max_length=20, null=True)
    documento = fields.CharField(max_length=20, null=True)
    nome_fantasia = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(null=True)

    def __str__(self):
        return self.cpf_cnpj

    class Meta:
        table = "pessoas"


class InfoContato(models.Model):
    id = fields.IntField(pk=True)
    client_id = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, null=True)
    pessoa_id = fields.IntField()
    telefone = fields.CharField(max_length=50, null=True)
    tipo = fields.CharField(max_length=20, null=True)

    class Meta:
        table = "info_contatos"
