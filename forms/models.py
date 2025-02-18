from django.db import models
from users.models import User

class WeatherChoices(models.TextChoices):
    FRIO = "frio"
    CALIENTE = "caliente"
    MEDIO = "medio"

class WorkChoices(models.TextChoices):
    INGENIERO = "ingeniero"
    AGRICULTOR = "agricultor"
    PROFESOR = "profesor"
    ECONOMISTA = "economista"
    DEPORTISTA = "deportista"
    ARTISTA = "artista"

class GenderChoices(models.TextChoices):
    HOMBRE = "hombre"
    MUJER = "mujer"

class CountryChoices(models.TextChoices):
    ALBANIA = "albania", "Albania"
    ANDORRA = "andorra", "Andorra"
    ARMENIA = "armenia", "Armenia"
    AUSTRIA = "austria", "Austria"
    AZERBAIYAN = "azerbaiyan", "Azerbaiyan"
    BIELORRUSIA = "bielorrusia", "Bielorrusia"
    BELGICA = "belgica", "Belgica"
    BOSNIA_Y_HERZEGOVINA = "bosnia_y_herzegovina", "Bosnia y Herzegovina"
    BULGARIA = "bulgaria", "Bulgaria"
    CROACIA = "croacia", "Croacia"
    CHIPRE = "chipre", "Chipre"
    REPUBLICA_CHECA = "republica_checa", "Republica Checa"
    DINAMARCA = "dinamarca", "Dinamarca"
    ESTONIA = "estonia", "Estonia"
    FINLANDIA = "finlandia", "Finlandia"
    FRANCIA = "francia", "Francia"
    GEORGIA = "georgia", "Georgia"
    ALEMANIA = "alemania", "Alemania"
    GRECIA = "grecia", "Grecia"
    HUNGRIA = "hungria", "Hungria"
    ISLANDIA = "islandia", "Islandia"
    IRLANDA = "irlanda", "Irlanda"
    ITALIA = "italia", "Italia"
    KAZAJISTAN = "kazajistan", "Kazajistan"
    KOSOVO = "kosovo", "Kosovo"
    LETONIA = "letonia", "Letonia"
    LIECHTENSTEIN = "liechtenstein", "Liechtenstein"
    LITUANIA = "lituania", "Lituania"
    LUXEMBURGO = "luxemburgo", "Luxemburgo"
    MALTA = "malta", "Malta"
    MOLDAVIA = "moldavia", "Moldavia"
    MONACO = "monaco", "Monaco"
    MONTENEGRO = "montenegro", "Montenegro"
    PAISES_BAJOS = "paises_bajos", "Paises Bajos"
    MACEDONIA_DEL_NORTE = "macedonia_del_norte", "Macedonia del Norte"
    NORUEGA = "noruega", "Noruega"
    POLONIA = "polonia", "Polonia"
    PORTUGAL = "portugal", "Portugal"
    RUMANIA = "rumania", "Rumania"
    RUSIA = "rusia", "Rusia"
    SAN_MARINO = "san_marino", "San Marino"
    SERBIA = "serbia", "Serbia"
    ESLOVAQUIA = "eslovaquia", "Eslovaquia"
    ESLOVENIA = "eslovenia", "Eslovenia"
    ESPANA = "españa", "España"
    SUECIA = "suecia", "Suecia"
    SUIZA = "suiza", "Suiza"
    TURQUIA = "turquia", "Turquia"
    UCRANIA = "ucrania", "Ucrania"
    REINO_UNIDO = "reino_unido", "Reino Unido"
    CIUDAD_DEL_VATICANO = "ciudad_del_vaticano", "Ciudad del Vaticano"

class Form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    work = models.CharField(max_length=255, null=False, choices=WorkChoices.choices, default=WorkChoices.ARTISTA)
    salary = models.FloatField(null=False)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=255, null=False, choices=GenderChoices.choices, default=GenderChoices.HOMBRE)
    country = models.CharField(max_length=255, null=False, choices=CountryChoices.choices, default=CountryChoices.AUSTRIA)
    weather = models.CharField(max_length=255, null=False, choices=WeatherChoices.choices, default=WeatherChoices.FRIO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} {self.created_at}"

