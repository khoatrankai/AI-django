from django.urls import path
from . import views

urlpatterns = [
    # path("blogposts/", views.BlogPostListCreate.as_view(), name="blogpost-view-create"),
    # path(
    #     "blogposts/<int:pk>/",
    #     views.BlogPostRetrieveUpdateDestory.as_view(),
    #     name="update",
    # ),
    path("aiAddress/",views.fetch_data, name="views-gpt"),
    path("aiJob/",views.SearchJobData, name="views-gpt-job"),
    path("chatgpttest/",views.CreateBotAddress.as_view(), name="views-gpt-chat"),
    path('chat/',views.my_view,name="my view"),
    path('jobFit/',views.SearchJobFit,name="job fit"),
    path('checkWar/',views.CheckWar,name="check fit"),
    path('aiChat/',views.ChatAi,name="chatbot"),
    path('aiChat22/',views.ChatAi22,name="chatbot22"),
    path('aiStartChat/',views.GenerateChatAi,name="generateBot"),
    path('aiFilterCV/',views.FilterCVPost,name="filterPost"),
    path('aiFilterPOST/',views.FilterPostCV,name="filterPost"),
]