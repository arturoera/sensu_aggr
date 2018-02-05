from django.conf.urls import url
from sensu_aggr_app import views

urlpatterns = [
    # The home page
    url(r'^$', views.index, name='index'),
    # url(r'^cluster_capacity/(?P<login>.*)/$', views.cluster_capacity, name='cluster_capacity'),
    # url(r'^brick_capacity/(?P<login>.*)/$', views.brick_capacity, name='brick_capacity'),
    # url(r'^instance_matrix/(?P<login>.*)/$', views.instance_matrix, name='instance_matrix'),
    # url(r'^audit_report/(?P<login>.*)/$', views.audit_report, name='audit_report'),
    # url(r'^recycled_shards/(?P<login>.*)/$', views.recycled_shards, name='recycled_shards'),
    # url(r'^form_search_instance/$', views.form_search_instance, name='form_search_instance'),
    # url(r'^customer_dashboard/$', views.customer_dashboard, name='customer_dashboard'),

]
