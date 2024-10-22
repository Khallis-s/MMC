from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('create-event/', views.create_event, name='create_event'),
    path('manage_events/', views.manage_events, name='manage_events'),
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('profile/', views.user_profile, name='user_profile'),
    path('logout/', views.logout, name='logout'),
    path('book-ticket/<int:event_id>/', views.book_ticket, name='book_ticket'),
    path('recent_books/', views.recent_books, name='recent_books'),
    path('booking/update/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
