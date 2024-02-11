from django.db import models
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


class Clientes(models.Model):
    
    nome = models.CharField(max_length=50, null=False)
    limite = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = 'clientes'


class Saldos(models.Model):
    cliente = models.OneToOneField(Clientes, models.CASCADE)
    valor = models.IntegerField(null=False)

    class Meta:
        managed = False
        db_table = 'saldos'


class Transacoes(models.Model):
    tipoChoices=[
        ("C", "Crédito"), 
        ("D", "Débito")]
    cliente = models.ForeignKey(Clientes, models.DO_NOTHING)
    valor = models.IntegerField(null=False)
    tipo = models.CharField(max_length=1, null=False, choices=tipoChoices)
    descricao = models.CharField(max_length=10, null=False)
    realizada_em = models.DateTimeField.auto_now_add

    class Meta:
        managed = False
        db_table = 'transacoes'
