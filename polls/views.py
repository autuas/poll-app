from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from django.db import connection
from django.db.models import Count

from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect, get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from .forms import ChoiceForm, PollForm 
from .models import Choice, Poll, Vote

@login_required
def poll_list(request):
    polls = Poll.objects.all()
    
    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    choices = poll.choices.annotate(vote_count=Count('votes'))

    user_voted = Vote.objects.filter(user=request.user, poll=poll).exists()

    max_votes = max((c.vote_count for c in choices), default=0)
    winners = [c for c in choices if c.vote_count == max_votes and max_votes > 0]

    if request.method == 'POST' and poll.active and not poll.owner == request.user:
        selected_choice_id = request.POST.get('choice')
        
        if selected_choice_id:
            selected_choice = get_object_or_404(Choice, pk=selected_choice_id, poll=poll)
            Vote.objects.update_or_create(user=request.user, poll=poll, defaults={'choice': selected_choice})
            
            return redirect('polls:poll_detail', pk=pk)

    context = {
        'poll': poll,
        'choices': choices,
        'user_voted': user_voted,
        'winners': winners,
        'max_votes': max_votes,
        'user': request.user,
        'choice_count': choices.count(),
    }
    
    return render(request, 'polls/poll_detail.html', context)

# ###
# FLAW 5: Cross-Site Request Forgery (CSRF)
# See polls/templates/polls/poll_form.html line 22 for the corresponding form
# Comment out the line below for the safe version:
# #
@csrf_exempt
# ###
@login_required
def poll_create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        
        if form.is_valid():
            poll = form.save(commit=False)
            poll.owner = request.user
            poll.save()
            
            return redirect('polls:poll_list')
    else:
        form = PollForm()
    return render(request, 'polls/poll_form.html', {'form': form})

@login_required
def poll_delete(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    
    # ###
    # FLAW 1: OWASP A01:2021-Broken Access Control
    # Vulnerable version when commented out; uncomment for safe version:
    # #
    # if poll.owner != request.user:
    #    
    #    return HttpResponseForbidden()
    # ###

    if request.method == 'POST':
        poll.delete()
        
        return redirect('polls:poll_list')
    
    return render(request, 'polls/poll_confirm_delete.html', {'poll': poll})

@login_required
def poll_end(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if poll.owner != request.user:
        
        return HttpResponseForbidden()

    if request.method == 'POST':
        poll.active = False
        poll.save()
        
        return redirect('polls:poll_list')
    
    return render(request, 'polls/poll_confirm_end.html', {'poll': poll})

@login_required
def poll_vote(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if poll.owner == request.user or not poll.active:
        
        return HttpResponseForbidden()
    
    if Vote.objects.filter(poll=poll, user=request.user).exists():
        
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        choice = get_object_or_404(Choice, id=choice_id, poll=poll)
        Vote.objects.create(poll=poll, choice=choice, user=request.user)
        
        return redirect('polls:poll_detail', pk=poll.pk)
    
    return redirect('polls:poll_detail', pk=poll.pk)

@login_required
def poll_add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id, owner=request.user)

    if not poll.active:
        
        return render(request, 'polls/poll_add_choice.html', {
            'poll': poll,
            'error': 'You cannot add choices to a poll that has ended.'
        })

    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.poll = poll
            choice.save()
            
            return redirect('polls:poll_detail', pk=poll_id)
    else:
        form = ChoiceForm()

    return render(request, 'polls/poll_add_choice.html', {'form': form, 'poll': poll})

@login_required
def poll_sql_search_form(request):
    
    return render(request, "polls/poll_search_form.html")

@login_required
def poll_search_results(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        with connection.cursor() as cursor:
            # ###
            # FLAW 2: OWASP A03:2021-Injection
            # Vulnerable version:
            # #
            cursor.execute(f"SELECT * FROM polls_poll WHERE question = '{query}'")
            # #
            # Safe version:
            # #
            # cursor.execute("SELECT * FROM polls_poll WHERE question = %s", [query])
            # ###

            results = cursor.fetchall()

    return render(request, "polls/poll_search_results.html", {"results": results, "query": query})
