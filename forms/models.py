from django.db import models
from users.models import User

class GenderChoices(models.TextChoices):
    MALE = 'Hombre'
    FEMALE = 'Mujer'

class AgricultureEconomyChoices(models.TextChoices):
    SI = 'Sí, prefiero un país con oportunidades en agricultura.'
    NO = 'No, prefiero un país con una economía diversificada.'
    NO_IMPORTA = 'No me importa.'

class EaseOfBusinessChoices(models.TextChoices):
    MUY_IMPORTANTE = 'Muy importante (Quiero emprender o invertir).'
    MODERADO = 'Moderadamente importante (Podría considerar oportunidades).'
    NO_IMPORTANTE = 'No es importante para mí.'

class ExportEconomyChoices(models.TextChoices):
    SI = 'Sí, quiero un país con un alto nivel de comercio internacional.'
    NO_IMPORTA = 'No es relevante para mí.'

class WorkSectorChoices(models.TextChoices):
    AGRICULTURA_PESCA = 'Agricultura / Pesca'
    TECNOLOGIA_INNOVACION = 'Tecnología / Innovación'
    NEGOCIOS_EMPRENDIMIENTO = 'Negocios / Emprendimiento'
    EDUCACION_SALUD = 'Educación / Salud'
    INDUSTRIA_MANUFACTURA = 'Industria / Manufactura'
    OTROS = 'Otros'

class UnemploymentRateChoices(models.TextChoices):
    BAJA_TASA = 'Quiero un país con muy baja tasa de desempleo.'
    NO_IMPORTA = 'No me importa mucho la tasa de desempleo.'

class JobSecurityChoices(models.TextChoices):
    EMPLEOS_ESTABLES = 'Prefiero un país con empleos estables y buenos contratos.'
    INFORMAL = 'No me importa si el empleo es informal o vulnerable.'

class MobileAccessChoices(models.TextChoices):
    MUY_IMPORTANTE = 'Muy importante.'
    NO_IMPORTA = 'No me importa.'

class AirPollutionChoices(models.TextChoices):
    MUY_IMPORTANTE = 'Muy importante, quiero vivir en un país con baja contaminación.'
    NO_IMPORTA = 'No me importa mucho.'

class LivingAreaChoices(models.TextChoices):
    CIUDAD = 'Ciudad'
    RURAL = 'Rural'
    NO_IMPORTA = 'No me importa'

class HealthcareImportanceChoices(models.TextChoices):
    MUY_IMPORTANTE = 'Muy importante, quiero un país con buena atención médica.'
    NO_IMPORTA = 'No me importa mucho.'

class ResearchDevelopmentChoices(models.TextChoices):
    SI = 'Sí, prefiero un país innovador.'
    NO = 'No es una prioridad para mí.'

class LowTaxesChoices(models.TextChoices):
    SI = 'Sí, quiero un país con menor carga impositiva.'
    NO = 'No me importa.'

class CompanyRegistrationChoices(models.TextChoices):
    SI = 'Sí, quiero facilidades para emprender.'
    NO = 'No me importa.'

class PovertyReductionChoices(models.TextChoices):
    MUY_IMPORTANTE = 'Muy importante, quiero un país con menos desigualdad.'
    NO_IMPORTA = 'No es una prioridad.'

class UnemploymentSupportChoices(models.TextChoices):
    SI = 'Sí, quiero un país con apoyo social.'
    NO = 'No me importa.'

class Form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, unique=True)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=255, null=False, choices=GenderChoices.choices, default=GenderChoices.MALE)
    salary = models.FloatField(null=False)
    agriculture_economy = models.CharField(max_length=255, null=False, choices=AgricultureEconomyChoices.choices, default=AgricultureEconomyChoices.SI)
    ease_of_business = models.CharField(max_length=255, null=False, choices=EaseOfBusinessChoices.choices, default=EaseOfBusinessChoices.MUY_IMPORTANTE)
    foreign_investment = models.CharField(max_length=255, null=False, choices=MobileAccessChoices.choices, default=MobileAccessChoices.MUY_IMPORTANTE)
    export_economy = models.CharField(max_length=255, null=False, choices=ExportEconomyChoices.choices, default=ExportEconomyChoices.SI)
    work_sector = models.CharField(max_length=255, null=False, choices=WorkSectorChoices.choices, default=WorkSectorChoices.TECNOLOGIA_INNOVACION)
    unemployment_rate = models.CharField(max_length=255, null=False, choices=UnemploymentRateChoices.choices, default=UnemploymentRateChoices.BAJA_TASA)
    job_security = models.CharField(max_length=255, null=False, choices=JobSecurityChoices.choices, default=JobSecurityChoices.EMPLEOS_ESTABLES)
    electricity_access = models.CharField(max_length=255, null=False, choices=MobileAccessChoices.choices, default=MobileAccessChoices.MUY_IMPORTANTE)
    air_pollution = models.CharField(max_length=255, null=False, choices=AirPollutionChoices.choices, default=AirPollutionChoices.MUY_IMPORTANTE)
    living_area = models.CharField(max_length=255, null=False, choices=LivingAreaChoices.choices, default=LivingAreaChoices.CIUDAD)
    healthcare_importance = models.CharField(max_length=255, null=False, choices=HealthcareImportanceChoices.choices, default=HealthcareImportanceChoices.MUY_IMPORTANTE)
    mobile_access = models.CharField(max_length=255, null=False, choices=MobileAccessChoices.choices, default=MobileAccessChoices.MUY_IMPORTANTE)
    research_development = models.CharField(max_length=255, null=False, choices=ResearchDevelopmentChoices.choices, default=ResearchDevelopmentChoices.SI)
    low_taxes = models.CharField(max_length=255, null=False, choices=LowTaxesChoices.choices, default=LowTaxesChoices.SI)
    company_registration = models.CharField(max_length=255, null=False, choices=CompanyRegistrationChoices.choices, default=CompanyRegistrationChoices.SI)
    poverty_reduction = models.CharField(max_length=255, null=False, choices=PovertyReductionChoices.choices, default=PovertyReductionChoices.MUY_IMPORTANTE)
    unemployment_support = models.CharField(max_length=255, null=False, choices=UnemploymentSupportChoices.choices, default=UnemploymentSupportChoices.SI)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} {self.created_at}"

