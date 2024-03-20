from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


class Endereco(models.Model):
  id = models.AutoField(primary_key=True)
  endereco = models.CharField(max_length=200,
                              validators=[MinLengthValidator(1)])
  numero = models.CharField(max_length=10, validators=[MinLengthValidator(1)])
  complemento = models.CharField(max_length=100,
                                 validators=[MinLengthValidator(1)])
  bairro = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
  cidade = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
  estado = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
  pais = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
  cep = models.CharField(
      max_length=8,
      validators=[RegexValidator(regex=r'^\d{8}$', message='CEP inválido')])


class Pessoa(models.Model):
  id = models.AutoField(primary_key=True)
  nome = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
  mae = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
  pai = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
  telefone = models.CharField(max_length=15,
                              validators=[
                                  RegexValidator(regex=r'^\d{10,15}$',
                                                 message='Telefone inválido')
                              ])
  nascimento = models.DateField()
  cpf = models.CharField(max_length=11,
                         validators=[
                             MinLengthValidator(11),
                             RegexValidator(regex=r'^\d{11}$',
                                            message='CPF inválido')
                         ],
                         unique=True)
  enderecos = models.ForeignKey(Endereco,
                                on_delete=models.CASCADE,
                                blank=False)
  usuario = models.OneToOneField(User,
                                 related_name='pessoa',
                                 on_delete=models.CASCADE)


class Registro(models.Model):
  id = models.AutoField(primary_key=True)

  entrada = models.BooleanField()
  datahora = models.DateTimeField()

  def save(self, *args, **kwargs):
      if not self.pk:  # Se o objeto estiver sendo criado
          self.datahora = timezone.now() - timezone.timedelta(hours=4)  # Ajuste para UTC-4
      super().save(*args, **kwargs)
  pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, blank=False)

