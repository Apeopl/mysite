from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Question,Choice
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
# Create your views here.


class IndexView(generic.ListView):
    # model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/result.html'


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # out_put = ', '.join([q.question_text for q in latest_question_list])
    # template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}

    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """"
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist!')
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(question)
    try:
        print(request.POST['choice'])
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

        print(selected_choice)
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'You did not select a choice.'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
