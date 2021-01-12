from django.db.models.deletion import ProtectedError
from django.db.models.fields import FloatField
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from .forms import *
# Create your views here.


def index(request):
    teBetalen = Leider.objects.values('naam').order_by('volgorde').\
    annotate(prijsNormaal=Coalesce(Sum(F('telling__aantalNormaal') * F('telling__prijsKlasse__normaal'), output_field=FloatField()), Value(0))).\
    annotate(prijsZwaar=Coalesce(Sum(F('telling__aantalZwaar') * F('telling__prijsKlasse__zwaar'), output_field=FloatField()), Value(0))).\
    annotate(totaal=Coalesce(F('prijsNormaal') + F('prijsZwaar'), Value(0))).\
    annotate(betaald=Coalesce(Sum('betaling__hoeveelheid'), Value(0)))

    return render(request, 'beheer/index.html', {'leiders': teBetalen})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = AuthenticationForm()
    return render(request, 'beheer/login.html', {'form': form})

@login_required
def prijsKlasse_view(request):
    if request.method == 'POST':
        form = PrijsKlasseForm(data=request.POST)
        if form.errors != True:
            form.save()
            return HttpResponseRedirect(reverse('prijsKlasse'))
    else:
        form = PrijsKlasseForm()

    return render(request, 'beheer/prijsklasse.html', {'form': form, 'prijsKlasses': PrijsKlasse.objects.all()})

@login_required
def prijsKlasse_delete(request, prijsKlasse_id):
    try:
        PrijsKlasse.objects.get(pk=prijsKlasse_id).delete()
    except ProtectedError:
        return HttpResponseRedirect(reverse('prijsKlasse')) 
    return HttpResponseRedirect(reverse('prijsKlasse'))

def telling_view(request):
    if request.method == 'POST':
        form = TellingForm(data=request.POST)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect(reverse('tellen'))
    else:
        form = TellingForm
    
    leiders = Leider.objects.all()
    return render(request, 'beheer/telling.html', {'form': form, 'leiders': leiders})

@login_required
def leider_view(request):
    if request.method == 'POST':
        volgordeForm = LeiderVolgordeForm()
        Nieuweform = NewLeiderForm(data=request.POST)
        if Nieuweform.is_valid():
            Nieuweform.save()
            return HttpResponseRedirect(reverse('leiders'))
    else:
        Nieuweform = NewLeiderForm()
        volgordeForm = LeiderVolgordeForm()

    return render(request, 'beheer/leiders.html', {'newForm': Nieuweform, 'volgordeForm': volgordeForm})

@login_required
def leider_volgorde(request):
    if request.method == 'POST':
        form = LeiderVolgordeForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('leiders'))
    else:
        return HttpResponseRedirect(reverse('leiders'))

@login_required
def betalingView(request):
    if request.method == 'POST':
        form = BetalingForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('betaling'))
    else:
        form = BetalingForm()
    return render(request, 'beheer/betaling.html', {'form': form})