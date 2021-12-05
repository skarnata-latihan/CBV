from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('templateview.urls')),
    path('books/', include('books.urls', namespace='books')),
]
