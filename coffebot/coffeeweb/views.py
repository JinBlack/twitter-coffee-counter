from coffee.views import *
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import HttpResponse, render_to_response
from chartit import PivotDataPool, PivotChart
from coffee.models import *
from django.db.models import Sum, Avg

import datetime

def index(request):
    t = get_template('home.html')
    time = datetime.datetime.now()
    overall_coffees = get_overall_coffees_amount()
    today_coffees = get_todays_coffees_amount()
    month_coffees = get_month_coffees_amount()
    top_drinker_un, top_drinker_tw = get_top_drinker_names()
    c = Context({
                    'overall_coffees' : overall_coffees,
                    'total_coffees_today' : today_coffees,
                    'total_coffees_month' : month_coffees,
                    'top_drinker_twitter' : top_drinker_tw,
                    'top_drinker_user_name' : top_drinker_un,
                    'monthly_coffee_chart': monthly_coffee_chart(),
                    'last_updated' : get_last_updated(),
                })
    html = t.render(c)
    return HttpResponse(html)

def monthly_coffee_chart():
    coffee_data = \
        PivotDataPool(
            series=
                [{'options': {
                   'source': get_month_coffees(),
                   'categories' : 'coffee_date'},
                  'terms': {
                    'coffes' : Sum('amount'),
                    }}
                 ])

    coffe_pivot_chart = \
        PivotChart(
            datasource = coffee_data,
            series_options =
              [{'options':{
                  'type': 'line',},
                'terms':['coffes']}],
            chart_options =
              { 'title': {
                    'text': 'Coffees drunk this month'},
                'xAxis': {
                    'title': {
                       'text': 'Day'}},
                'yAxis': {
                    'title':{
                        'text': 'Coffees drunk'}}})

    return coffe_pivot_chart
