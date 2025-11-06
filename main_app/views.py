from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Car, CarTrip
from .forms import CarDateForm


# --- Home and About ---
class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


# --- Cars ---
@login_required
def car_index(request):
    cars = Car.objects.filter(user=request.user)
    return render(request, 'cars/index.html', {'cars': cars})


def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    cardate_form = CarDateForm()

    # Get all trips for this specific car
    car_trips = car.cartrip_set.all()

    if request.method == 'POST':
        cardate_form = CarDateForm(request.POST)
        if cardate_form.is_valid():
            new_cardate = cardate_form.save(commit=False)
            new_cardate.car = car
            new_cardate.save()
            return redirect('cars_detail', car_id=car_id)

    return render(request, 'cars/detail.html', {
        'car': car,
        'car_trips': car_trips,
        'cardate_form': cardate_form
    })


class CarCreate(LoginRequiredMixin,CreateView):
    model = Car
    fields = ['type', 'model', 'description', 'year', 'mileage']
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the car
        # Let the CreateView do its job as usual
        return super().form_valid(form)


class CarUpdate(LoginRequiredMixin,UpdateView):
    model = Car
    fields = ['type', 'model', 'description', 'year', 'mileage']


class CarDelete(LoginRequiredMixin,DeleteView):
    model = Car
    success_url = '/cars/'


# --- Car Trips ---
class CarTripsCreate(LoginRequiredMixin,CreateView):
    model = CarTrip
    fields = ['car', 'event_name', 'date', 'location', 'notes']


class CarTripsList(LoginRequiredMixin,ListView):
    model = CarTrip


class CarTripDetail(LoginRequiredMixin,DetailView):
    model = CarTrip


class CarTripUpdate(LoginRequiredMixin,UpdateView):
    model = CarTrip
    fields = ['car', 'event_name', 'date', 'location', 'notes']


class CarTripDelete(LoginRequiredMixin,DeleteView):
    model = CarTrip
    success_url = '/cartrips/'


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('car-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )