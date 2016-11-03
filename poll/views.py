from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.core.urlresolvers import reverse
from django.views import generic
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


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice."
        })
    selected_choice.votes += 1
    selected_choice.save()
    # success deal with post data always return HttpResponseRedirect, prevent user submit twice
    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def test(request):
    context = {'days': [1,1,1,2,3,4,4,4,5,6]}
    return render(request, 'polls/test.html', context)

# ListView represent display a list of objects
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # return last five published question
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


# DetailView represent display a detail page for a particular type of object
#
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

class BuildingView(BaseView):
    def get(self, request):
        # userStr = request.session['user']
        # user = UserSerializer.parse(userStr)
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



