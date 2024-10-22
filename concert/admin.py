from django.contrib import admin
from .models import CustomUser,Ticket,Book,Event
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # Define which fields to display in the admin list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type') 
    
    # Define which fields can be searched
    search_fields = ('user_name', 'user_email')

    list_editable = ('user_type',)

    fields = ('user_name', 'user_email', 'user_password', 'user_type')

admin.site.register(CustomUser, UserAdmin)

class TicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'ticket_type', 'ticket_quantity', 'ticket_price', 'user_id', 'event_id')
    search_fields = ('ticket_id', 'ticket_type', 'user_id', 'event_id')
    list_editable = ('ticket_type', 'ticket_quantity', 'ticket_price')

admin.site.register(Ticket, TicketAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'user_id', 'event_id', 'ticket_id', 'booking_date', 'quantity')
    search_fields = ('book_id', 'user_id', 'event_id', 'ticket_id')
    list_editable = ('quantity',)

admin.site.register(Book, BookAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id', 'event_name', 'event_date', 'event_time', 'event_location', 'event_description')
    search_fields = ('event_name', 'event_location')
    list_editable = ('event_date', 'event_time', 'event_location', 'event_description')

admin.site.register(Event, EventAdmin)