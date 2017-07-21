from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from thinc.forms import IdeaForm, VoteForm, ContactForm
from thinc.models import Idea
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.contrib import messages

def browse_by_name(request, initial=None):
	if initial: 
		ideas = Idea.objects.filter(name__istartswith=initial)
		ideas = ideas.order_by('name')
	else:
		ideas = Idea.objects.all().order_by('name')

	return render(request, 'search/search_by_name.html', {
			'ideas': ideas,
			'initial': initial,
		})

def browse_by_votes(request):
	ideas = Idea.objects.all().order_by('-votes')

	return render(request, 'search/browse_by_votes.html', {
			'ideas': ideas,
		})

def contact(request): 
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = form.cleaned_data['contact_name'] 
            contact_email = form.cleaned_data['contact_email'] 
            form_content = form.cleaned_data['content']

            # email the profile with the contact info 
            template = get_template('contact_template.txt')

            context = Context({ 
                'contact_name': contact_name, 
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                'New contact form submission',
                content,
                'Your website <hi@weddinglovely.com>',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            messages.success(request, 'Email Sent!')
            return redirect('contact')

    return render(request, 'contact.html', { 
        'form': form_class,
    })

def create_idea(request):
	form_class = IdeaForm

	if not request.user.is_authenticated():
		return redirect('login')

	# if we're coming from a submitted form, do this
	if request.method == 'POST':
		# grab the date from the submitted form and apply to the form
		form = form_class(request.POST)
		if form.is_valid():
			# create an instance but don't save yet
			idea = form.save(commit=False)

			# set the additional details
			idea.user = request.user
			idea.slug = slugify(idea.name)

			# save the object
			idea.save()

			# redirect to our newly created idea
			return redirect('idea_detail', slug=idea.slug)

	# otherwise just create the form
	else:
		form = form_class()

	return render(request, 'ideas/create_idea.html', {
			'form': form,
		})

@login_required
def edit_idea(request, slug):
	# grab the object 
	idea = Idea.objects.get(slug=slug)

	# make sure the logged in user is the onwer of the idea
	if idea.user != request.user:
		raise Http404

	# set the form we're using 
	form_class = IdeaForm

	# if we're coming to this view from a submitted form
	if request.method == 'POST':
		# grab the data from the submitted form and apply to the form
		form = form_class(data=request.POST, instance=idea)
		if form.is_valid():
			# save the new data
			idea.votes += 1
			form.save()
			return redirect('idea_detail', slug=idea.slug)
	# otherwise just create the form
	else:
		form = form_class(instance=idea)

	# and render the template
	return render(request, 'ideas/edit_idea.html', {
			'idea': idea,
			'form': form,
	})

def index(request):
    ideas = Idea.objects.order_by('-published_date')
    top_ideas = Idea.objects.order_by('-votes')

    return render(request, 'index.html', {
        'ideas': ideas,
        'top_ideas': top_ideas,
    })
	

def idea_detail(request, slug):
	# grab the object...
	idea = Idea.objects.get(slug=slug)

	# and pass to the template
	return render(request, 'ideas/idea_detail.html', {
			'idea': idea,
	})

def my_ideas(request):
	logged_in_user = request.user
	ideas = Idea.objects.filter(user = logged_in_user)
	ideas = ideas.order_by("-votes")

	return render(request, 'ideas/my_ideas.html', {
			'ideas': ideas
		})

def upvote(request, idea_id):
	idea = Idea.objects.get(pk=idea_id)
	idea.votes += 1
	idea.save()
	return render(request, 'index.html')


