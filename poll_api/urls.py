from django.urls import path, include

api_urls = [
    path('', include('user.urls')),
    path('', include('poll.urls')),
]

urlpatterns = [
    path('v1/', include((api_urls, 'v1'), namespace='v1')),
]
