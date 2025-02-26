from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Modelo')))

import ipynb.fs.defs.prueba_5 as notebook_module

from .serializers import FormSerializer
from forms.models import Form


# Create your views here.

class FormViewSet(viewsets.ModelViewSet):
    permission_classes = []
    serializer_class = FormSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ['user__id']

    def get_queryset(self):
        return Form.objects.all().order_by('user__username')

    @action(detail=False, methods=['get'])
    def result(self, request, pk=None):
        # user = request.user
        # print(user)
        # user_form = Form.objects.filter(user=user).first()
        # if not user_form:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        # print(user_form)
        user_form = Form.objects.first()

        respuestas_usuario = {
            "¿Qué tan importante es para ti que los salarios en el país sean altos?": user_form.country_salary,
            "¿Qué tan importante es que sea fácil abrir un negocio o encontrar empleo?": user_form.job_security,
            "¿Qué tan importante es que haya pocas personas desempleadas?": user_form.unemployment_rate,
            "¿Qué tan importante es vivir en un país con baja corrupción?": user_form.corruption,
            "¿Qué tan importante es para ti que haya buenos médicos y hospitales accesibles?": user_form.healthcare_importance,
            "¿Qué tan importante es que la economía del país esté creciendo constantemente?": user_form.economy,
            "¿Qué tan importante es vivir en un país con más libertades personales y económicas?": user_form.freedom,
            "¿Qué tan importante es para ti vivir en un país con aire limpio?": user_form.air_pollution,
            "¿Qué tan importante es que los precios se mantengan estables y la inflación sea baja?": user_form.low_inflation,
            "¿Qué tan importante es que el país reciba inversión extranjera?": user_form.foreign_investment,
            "¿Qué tan importante es para ti vivir en una ciudad en crecimiento con nuevas oportunidades?": user_form.city_growth,
            "¿Qué tan importante es que haya muchas opciones de comercio, servicios y entretenimiento?": user_form.living_area
        }

        top_paises_df = notebook_module.recomendar_paises(respuestas_usuario)

        print(top_paises_df)

        top_paises = top_paises_df.to_dict(orient='records')

        return Response(top_paises, status=status.HTTP_200_OK)