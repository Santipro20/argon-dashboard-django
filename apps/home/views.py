# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from plotly.offline import plot
from apps.home.models import Courses
import pandas as pd

#@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def chart(request):
   courses = Courses.objects.all()
   data = courses.values("id","price","cost")
   df = pd.DataFrame.from_records(data)
   data = df[["price", "cost"]]
   # Crear el objeto gráfico de plotly
   graph = plot([{"x": data["price"], "y": data["cost"], "type": "bar"}], output_type="div")
   # Pasar el objeto gráfico al contexto
   context = {"plot_div": graph}
   return render(request, 'index.html', context)

