from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# Custom error handlers
handler400 = 'core.views.bad_request'
handler403 = 'core.views.permission_denied'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

urlpatterns = [
    path("admin/dj-control-room-base/", include("dj_control_room_base.urls")),
    path("admin/dj-control-room/", include("dj_control_room.urls")),
    ##################
    path("admin/dj_urls_panel/", include("dj_urls_panel.urls")),
    path("admin/dj_signals_panel/", include("dj_signals_panel.urls")),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('purchases/', include('purchases.urls')),
    path('finance/', include('finance.urls')),
    path('', include('sales.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
