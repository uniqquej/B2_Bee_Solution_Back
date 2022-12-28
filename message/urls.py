from django.urls import path
from message import views

urlpatterns = [
    path('<int:check>/', views.MessageView.as_view(), name='message_view'),
    path('detail/<int:message_id>/',views.DetailMessageView.as_view(), name='detail_message_view')
]