from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
from django.views import generic
from django.views import View
from django.utils import timezone
from wx.base_view import InterceptorView as BaseView
from .serializer import UserSerializer


# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def article(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/article.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/no_results.html', {'question': question})


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/no_detail.html', {
            'question': p,
            'error_message': "You didn't select a choice."
        })
    selected_choice.votes += 1
    selected_choice.save()
    # success deal with post data always return HttpResponseRedirect, prevent user submit twice
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def sort_by_heat(request, pk):
    userStr = request.session['user']
    user = UserSerializer.parse(userStr)
    building = Building.objects.filter(is_online=True, id=pk)[0]
    articles = Option.objects.filter(building__id=building.id).order_by('count')
    isVotedList = []
    for article in articles:
        isVotedList.append(True if article.votes.exists(user.id) else False)
    activity = ActivityDetail.objects.filter().order_by('-id')[0]
    return render(request, 'polls/detail.html', {
        'user': user,
        'building': building,  # 返回指定的建筑
        'articles': zip(articles, isVotedList),
        'activity': activity
    })


def sort_by_time(request, pk):
    userStr = request.session['user']
    user = UserSerializer.parse(userStr)
    building = Building.objects.filter(is_online=True, id=pk)[0]
    articles = Option.objects.filter(building__id=building.id).order_by('-pub_time')
    isVotedList = []
    for article in articles:
        isVotedList.append(True if article.votes.exists(user.id) else False)
    activity = ActivityDetail.objects.filter().order_by('-id')[0]
    return render(request, 'polls/detail.html', {
        'user': user,
        'building': building,  # 返回指定的建筑
        'articles': zip(articles, isVotedList),
        'activity': activity
    })


def outVote(request, pk):
    userStr = request.session['user']
    user = UserSerializer.parse(userStr)
    article = Option.objects.get(id=pk)
    if not article.votes.exists(user.id):
        article.votes.up(user.id)
    return HttpResponse(article.votes.count(), content_type='text/html')


def inVote(request, pk):
    userStr = request.session['user']
    user = UserSerializer.parse(userStr)
    article = Option.objects.get(id=pk)
    if not article.votes.exists(user.id):
        article.votes.up(user.id)
    return HttpResponse(article.votes.count(), content_type='text/html')


def test(request):
    context = {'days': [1,1,1,2,3,4,4,4,5,6]}
    return render(request, 'polls/test.html', context)


# ListView represent display a list of objects
class IndexView(BaseView):
    def get(self, request):
        userStr = request.session['user']
        user = UserSerializer.parse(userStr)
        buildings = Building.objects.filter(is_online=True)
        #articles = Option.objects.all()
        activity = ActivityDetail.objects.filter().order_by('-id')[0]
        return render(request, 'polls/index.html', {
            'buildings': buildings,
            'activity': activity
            #,'articles': articles
        })


class TitleView(generic.ListView):
    template_name = 'polls/no_index.html'
    context_object_name = 'latest_question_list'

    def get(self, request):
        userStr = request.session['user']
        user = UserSerializer.parse(userStr)
        buildings = Building.objects.filter(is_online=True)
        activity = ActivityDetail.objects.filter().order_by('-id')[0]
        return render(request, 'polls/building.html', {
            'buildings': buildings,
            'activity': activity
        })


# DetailView represent display a detail page for a particular type of object
#
class DetailView(generic.View):

    def get(self, request, pk):
        userStr = request.session['user']
        user = UserSerializer.parse(userStr)
        building = Building.objects.filter(is_online=True, id=pk)[0]
        articles = Option.objects.filter(building__id=building.id)
        isVotedList = []
        for article in articles:
            isVotedList.append(True if article.votes.exists(user.id) else False)
        activity = ActivityDetail.objects.filter().order_by('-id')[0]
        return render(request, 'polls/detail.html', {
            'user': user,
            'building': building,#返回指定的建筑
            'articles': zip(articles, isVotedList),
            'activity': activity,
        })


class ArticleView(generic.View):
    def get(self, request, pk, ):
        userStr = request.session['user']
        user = UserSerializer.parse(userStr)
        article = Option.objects.get(id=pk)
        building = Building.objects.get(id=article.building.id)
        return render(request, 'polls/article.html', {
            'building': building,
            'article': article,#返回指定的文章
            'voteNum': article.votes.count(),
            'voted': article.votes.exists(user.id)
        })


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/no_results.html'


class BuildingView(BaseView):
    def get(self, request):
        userStr = request.session['user']
        user = UserSerializer.parse(userStr)
        buildings = Building.objects.filter(is_online=True)
        activity = ActivityDetail.objects.filter().order_by('-id')[0]
        return render(request, 'polls/building.html', {
            'buildings':buildings,
            'activity': activity
        })


class OptionListView(BaseView):
    def get(self, request, building_id):
        options = Option.objects.filter().order_by('-pub_time')
        return render(request, 'polls/option_list.html', {
            'options': options,
            'building_id': building_id
        })


class RankListView(BaseView):
    def get(self, request):
        pass


def raise_option(request, option_id):
    userStr = request.session['user']
    user = UserSerializer.parse(userStr)
    p = get_object_or_404(Option, pk=option_id)
    if p.votes.exists(user.id):
        return render(request, 'polls/building.html', {
            'building': p.building,
            'error_message': "您已经选过这个选项"
        })
    p.votes.up(user.id)
    return HttpResponseRedirect(reverse('polls:option_list', args=(p.building.id)))

def returnText(request):

    return HttpResponse('hahahah', content_type='text/html')



