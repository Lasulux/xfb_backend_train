# Basic packages
import os
from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# SWAGGER-related imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from .OpenAPISchemaGenerator_local import OpenAPISchemaGenerator_local

app_name = "API"

openapi_info = openapi.Info(title="Backend tutorial API documentation", default_version="v1")
schema_view = get_schema_view(
    info=openapi_info, public=True, permission_classes=(AllowAny,), generator_class=OpenAPISchemaGenerator_local
)
#############################################
#               Define URLs
#############################################
urlpatterns = [
    # re_path(r"^POST/ErrorGen/$", views.ErrorGen, name="ErrorGen"),
    re_path(r"^POST/SearchPlayers/$", views.SearchPlayers, name="SearchPlayers"),
    re_path(r"^POST/AddPlayer/$", views.AddPlayer, name="AddPlayer"),
    re_path(r"^POST/RemovePlayer/$", views.RemovePlayer, name="RemovePlayer"),
    re_path(r"^POST/UpdatePlayer/$", views.UpdatePlayer, name="UpdatePlayer"),
]


if os.environ.get("DEBUG").upper() == "TRUE":
    urlpatterns.append(re_path(r"^SWAGGER/documentation/$", schema_view.with_ui(renderer="swagger"), name="swagger"))

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
