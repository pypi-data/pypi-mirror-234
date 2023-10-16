from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

app_name = "microbiology_app"


urlpatterns = []


urlpatterns += [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", RedirectView.as_view(url="admin/"), name="logout"),
]
