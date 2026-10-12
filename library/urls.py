from django.urls import path
from . import views

urlpatterns = [
    path("", views.catalog, name="catalog"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("issue/", views.issue_book, name="issue_book"),
    path("return/<int:record_id>/", views.return_book, name="return_book"),
    path("members/", views.members, name="members"),
    path("members/add/", views.add_member, name="add_member"),
    path("members/<int:member_id>/", views.member_history, name="member_history"),
]
