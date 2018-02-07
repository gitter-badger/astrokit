from django.conf.urls import patterns, url

urlpatterns = patterns('imageflow.views',
    url(r'^upload', 'upload_image', name='upload_image'),
    url(r'^submission/(?P<subid>[0-9]+)$', 'astrometry', name='astrometry'),
    url(r'^submission/(?P<subid>[0-9]+)/set_datetime$', 'set_datetime', name='set_datetime'),
    url(r'^submission/(?P<subid>[0-9]+)/set_filter_band$', 'set_filter_band', name='set_filter_band'),
    url(r'^submission/(?P<subid>[0-9]+)/set_latitude$', 'set_latitude', name='set_latitude'),
    url(r'^submission/(?P<subid>[0-9]+)/set_longitude$', 'set_longitude', name='set_longitude'),
    url(r'^submission/(?P<subid>[0-9]+)/set_elevation$', 'set_elevation', name='set_elevation'),
    url(r'^submission/(?P<subid>[0-9]+)/set_second_order_extinction$', 'set_second_order_extinction', name='set_second_order_extinction'),
    url(r'^submission/(?P<subid>[0-9]+)/set_color_index_1$', 'set_color_index_1', name='set_color_index_1'),
    url(r'^submission/(?P<subid>[0-9]+)/set_color_index_2$', 'set_color_index_2', name='set_color_index_2'),
    url(r'^submission/(?P<subid>[0-9]+)/set_image_companion$', 'set_image_companion', name='set_image_companion'),
    url(r'^submission/(?P<subid>[0-9]+)/set_reduction_status$', 'set_reduction_status', name='set_reduction_status'),
    url(r'^submission/(?P<subid>[0-9]+)/get_reduction_status$', 'get_reduction_status', name='get_reduction_status'),
    url(r'^submission/astrometry/(?P<subid>[0-9]+)$', 'astrometry', name='astrometry'),
    url(r'^submission/point_sources/(?P<subid>[0-9]+)$', 'point_sources', name='point_sources'),
    url(r'^submission/reference_stars/(?P<subid>[0-9]+)$', 'reference_stars', name='reference_stars'),
    url(r'^submission/reduction/(?P<subid>[0-9]+)$', 'reduction', name='reduction'),
    url(r'^submission/add_to_light_curve/(?P<subid>[0-9]+)$', 'add_to_light_curve', name='add_to_light_curve'),
    url(r'^submission/light_curve/(?P<subid>[0-9]+)$', 'light_curve', name='light_curve'),
    url(r'^api/submission/(?P<subid>[0-9]+)/results$', 'api_get_submission_results', name='api_get_submission_results'),
    url(r'^$', 'index', name='index'),
)
