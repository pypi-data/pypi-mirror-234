from django.urls import path

from example.views import CreateOrUpdateTranslatableView, TranslatableListView

app_name = 'example'
urlpatterns = [
    path('create/', CreateOrUpdateTranslatableView.as_view(), name="create"),
    path('<int:pk>/edit/', CreateOrUpdateTranslatableView.as_view(), name="edit"),
    path('', TranslatableListView.as_view(), name="listing"),
]
