from django.urls import path
from . import views

urlpatterns = [
    path("blogposts/", views.BlogPostListCreate.as_view(), name="blogpost-view-create"),
    path(
        "blogposts/<int:pk>/",
        views.BlogPostRetrieveUpdateDestory.as_view(),
        name="update",
    ),
    path("aiAddress/",views.fetch_data, name="views-gpt"),
    path("aiJob/",views.SearchJobData, name="views-gpt-job"),
    path("chatgpttest/",views.CreateBotAddress.as_view(), name="views-gpt-chat"),
    path('chat/',views.my_view,name="my view")
]