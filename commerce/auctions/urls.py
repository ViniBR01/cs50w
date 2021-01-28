from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:item_id>", views.item, name="item"),
    path("item/<int:item_id>/watch", views.watch, name="watch"),
    path("item/<int:item_id>/close", views.close, name="close"),
    path("item/<int:item_id>/comment", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("categories/<slug:cat_id>", views.categorized, name="categorized"),
    path("watchlist", views.watchlist, name="watchlist"),
]
