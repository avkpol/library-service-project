from django.urls import include, path
from rest_framework.routers import DefaultRouter
from book.views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        "create/",
        BookViewSet.as_view(actions={"book": "create"}),
        name="create_book"
    ),
]

app_name = "book"