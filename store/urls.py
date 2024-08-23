from django.urls import path
from . import views
from .views import add_to_wishlist, remove_from_wishlist, wishlist_view

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("update_password/", views.update_password, name="update_password"),
    path("update_user/", views.update_user, name="update_user"),
    path("update_info/", views.update_info, name="update_info"),
    path("product/<int:pk>", views.product, name="product"),
    path("category/<str:foo>", views.category, name="category"),
    path("categories/", views.category_list, name="category_list"),
    path("search/", views.search, name="search"),
    path("product/<int:product_id>/add_review/", views.add_review, name="add_review"),
    path("wishlist/", wishlist_view, name="wishlist_view"),
    path("wishlist/add/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path(
        "wishlist/remove/<int:product_id>/",
        remove_from_wishlist,
        name="remove_from_wishlist",
    ),
]
