from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/
    # url(r'^$', views.TitleView.as_view(), name='title'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/detail$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/outVote$', views.outVote, name='outVote'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/inVote$', views.inVote, name='inVote'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/sort_by_heat', views.sort_by_heat, name='sort_by_heat'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/sort_by_time', views.sort_by_time, name='sort_by_time'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleView.as_view(), name='article'),


    # ex:/polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex:/polls/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'test/$', views.test, name='test'),

    url(r'^buildings/$', views.BuildingView.as_view(), name='building'),
    url(r'^(?P<building_id>[0-9]+)/options/$', views.OptionListView.as_view(), name='option_list'),
    # url(r'^(?P<building_id>[0-9]+)/options/$', views.OptionListView.as_view(), name='option_list'),

]