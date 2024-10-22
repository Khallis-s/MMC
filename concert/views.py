from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .models import CustomUser, Event, Ticket, Book
from .forms import EventForm
from django.http import HttpResponseForbidden
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .forms import LoginForm
from django.core.exceptions import ValidationError
from django.utils import timezone

CustomUser = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set password correctly
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                request.session['user_name'] = user.username
                request.session['user_email'] = user.email
                return redirect('home')  # Redirect to the home page or dashboard
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    query = request.GET.get('q')  # Get the search term from the query parameter
    if query:
        events = Event.objects.filter(event_name__icontains=query)
    else:
        events = Event.objects.all()
    return render(request, 'home.html', {'events': events, 'user': request.user, 'query': query})


def create_event(request):
    # Check if the user is logged in and is Admin (instead of MMC Staff)
    if not request.user.is_authenticated or request.user.user_type != 'Admin':
        return HttpResponseForbidden("You are not authorized to create events.")

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})

User = get_user_model() 
def user_profile(request):
    user_name = request.session.get('user_name')
    user_email = request.session.get('user_email')

    if not user_name or not user_email:
        messages.error(request, "You are not logged in.")
        return redirect('login')

    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    if request.method == 'POST':
        # Handle Update Profile
        if 'update_profile' in request.POST:
            new_name = request.POST.get('user_name')
            new_email = request.POST.get('user_email')

            if new_name and new_name != user.username:
                user.username = new_name
                request.session['user_name'] = new_name  # Update session
            if new_email and new_email != user.email:
                user.email = new_email
                request.session['user_email'] = new_email  # Update session

            user.save()
            return redirect('user_profile')

        elif 'delete_profile' in request.POST:
            user.delete()
            request.session.flush()  # Clear session after deletion
            return redirect('login')
    return render(request, 'user_profile.html', {'user': user})

def logout(request):
    request.session.flush()
    return redirect('login')    

def book_ticket(request, event_id):
    try:
        event = Event.objects.get(event_id=event_id)
        user = request.user

        if request.method == 'POST':
            ticket_type = request.POST.get('ticket_type')
            ticket_quantity = request.POST.get('ticket_quantity')

            if not ticket_type or not ticket_quantity:
                messages.error(request, 'All fields are required.')
                return render(request, 'book_ticket.html', {'event': event})

            try:
                ticket_quantity = int(ticket_quantity)
                if ticket_quantity <= 0:
                    raise ValueError
            except ValueError:
                messages.error(request, 'Invalid ticket quantity.')
                return render(request, 'book_ticket.html', {'event': event})

            # Determine ticket price based on type
            if ticket_type == 'VIP':
                ticket_price = 20
            elif ticket_type == 'Standard':
                ticket_price = 10
            else:
                messages.error(request, 'Invalid seat type.')
                return render(request, 'book_ticket.html', {'event': event})

            try:
                # Create the ticket entry
                ticket = Ticket.objects.create(
                    ticket_type=ticket_type,
                    ticket_quantity=ticket_quantity,
                    ticket_price=ticket_price * ticket_quantity,  # Total price based on quantity
                    user_id=user,
                    event_id=event
                )

                # Create the corresponding booking in the Book model
                Book.objects.create(
                    user_id=user,
                    event_id=event,
                    ticket_id=ticket,  # Link the created ticket
                    booking_date=timezone.now(),
                    quantity=ticket_quantity
                )
                return redirect('home')
            except ValidationError as e:
                messages.error(request, 'There was an error saving the ticket.')
                return render(request, 'book_ticket.html', {'event': event})
        return render(request, 'book_ticket.html', {'event': event})

    except Event.DoesNotExist:
        messages.error(request, 'Event not found.')
        return redirect('home')
    
def recent_books(request):
    print(request.user)  # This should print the currently logged-in user
    if request.user.is_authenticated:
        recent_bookings = Book.objects.filter(user_id=request.user).order_by('-booking_date')[:10]
        return render(request, 'recent_books.html', {'recent_bookings': recent_bookings})
    else:
        return redirect('login')

def update_booking(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        ticket_type = request.POST.get('ticket_type')
        try:
            new_quantity = int(new_quantity)
            if new_quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")
            # Update the quantity in the Book model
            booking.quantity = new_quantity
            # Update the Ticket model
            if ticket_type in ['VIP', 'Standard']:
                booking.ticket_id.ticket_type = ticket_type
                booking.ticket_id.ticket_quantity = new_quantity  # Update ticket quantity
                booking.ticket_id.ticket_price = 20 * new_quantity if ticket_type == 'VIP' else 10 * new_quantity
                booking.ticket_id.save()
            booking.save()  # Save changes to the booking
            messages.success(request, 'Booking updated successfully.')
            return redirect('recent_books')
        except ValueError:
            messages.error(request, 'Invalid input. Please check the values.')
    return render(request, 'update_booking.html', {'booking': booking})

def delete_booking(request, booking_id):
    booking = get_object_or_404(Book, pk=booking_id)
    
    # Correct the ticket retrieval by using booking.ticket_id_id to access the ticket_id field
    ticket = Ticket.objects.get(ticket_id=booking.ticket_id.ticket_id)


    if request.method == 'POST':
        booking.delete()  # Delete the booking
        ticket.delete()
        return redirect('recent_books')
    return render(request, 'delete_booking.html', {'booking': booking})

def manage_events(request):
    events = Event.objects.all()  # Retrieve all events
    return render(request, 'manage_events.html', {'events': events})

# Update Event View
def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    if request.method == 'POST':
        event.event_name = request.POST['event_name']
        event.event_date = request.POST['event_date']
        event.event_time = request.POST['event_time']
        event.event_location = request.POST['event_location']
        event.event_description = request.POST['event_description']
        
        # Handle file upload for event poster (if provided)
        if request.FILES.get('event_poster'):
            event.event_poster = request.FILES['event_poster']

        event.save()
        return redirect('manage_events')
    return render(request, 'edit_event.html', {'event': event})

# Delete Event View
def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('manage_events')
    return redirect('manage_events')
