from django.shortcuts import get_object_or_404,render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question

class IndexView(generic.ListView):
   template_name = 'polls/index.html'
   context_object_name = 'latest_question_list'
   
   def get_queryset(self):
      """
         Returns the last 5 published questions
         (not including those set to be published
         in the future).
      """
      return Question.objects.filter(
        pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
   model = Question
   template_name = 'polls/detail.html'
   question_choice_set = []
   def get_queryset(self):
     """
     Excludes any questions that aren't published yet or do not have choices.
     choice_set = Choice.objects.all()
     for c in choice_set:
       if (c.question.pub_date <= timezone.now()):
          question_choice_set.append(c.question)
     return set(question_choice_set)

     """
     return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
   model = Question
   template_name = 'polls/results.html'

   def get_queryset(self):
     """
     Excludes any questions that aren't published yet.
     """
     return Question.objects.filter(pub_date__lte = timezone.now())

def get_questions_with_choices(self):
   q_list = []
   choice_set = Choice_objects_all()
   for c in choice_set:
      if (c.question.pub_date <= timezone.now()):
         q_list.append(c.question)
   return set(q_list)

def vote(request, question_id):
   p= get_object_or_404(Question, pk=question_id)
   try:
      selected_choice = p.choice_set.get(pk=request.POST['choice'])
   except (KeyError, Choice.DoesNotExist):
      # Redisplay the question voting form.
      return render(request, 'polls/detail.html', {
         'question':p,
         'error_message': "You didn't select a choice.",
      })
   else:
      selected_choice.votes += 1
      selected_choice.save()
      # Always return an HttpResponseRedirect after successfully dealing
      # with POST data.  This prevents from being posted twice if a user
      # hits the Back button.
      return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
