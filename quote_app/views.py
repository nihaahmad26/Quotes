from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect ('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request,e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/quotes')


def show_all(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        logged_in_user = User.objects.get(id=request.session['user_id'])
        context = {
            'all_quotes': Quote.objects.all(),
            'my_fav': Quote.objects.filter(Q(creator=logged_in_user) | Q(favorited_by = logged_in_user)),
            'not_my_fav': Quote.objects.exclude(Q(creator=logged_in_user) | Q(favorited_by = logged_in_user)),
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'show_all.html', context)

def show_page(request):
    return render(request,"add_quote.html")

def add_quote(request):
    if request.method=="GET":
        return redirect("/quotes/page")
        # return render(request,"add_quote.html")
    else:
        print(request.POST)
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes/page')
        else:
            user = User.objects.get(id=request.session["user_id"])
            quote = Quote.objects.create(
            author = request.POST['author'],
            description = request.POST['description'],
            creator = user
        )
            user.favorited_quotes.add(quote)
            # return render(request, 'add_quote.html')
            return redirect("/quotes")

        # return redirect(f'/quotes/{quote.id}')

def count(request, user_id):
    context ={
        'user': User.objects.get(id=user_id),
        # 'quote': Quote.objects.get(id = 'quote_id')
        # 'user': User.objects.get(id=request.session['user_id'])
        # quote = Quote.objects.get(id=quote_id) trying to get the total count for user
    }
    return render(request, 'user.html', context)

def show_one(request, quote_id):
    context = {
        'quote': Quote.objects.get(id=quote_id),
        'current_user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "show_one.html", context)



def update(request, quote_id):
    if request.method=="GET":
        context = {
            'quote' : Quote.objects.get(id=quote_id),
        }
        return render(request,"show_one.html", context)
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/quotes/{quote_id}")
    else:
        quote = Quote.objects.get(id=quote_id)
        quote.author = request.POST['author']
        quote.description = request.POST['description']
        quote.save()
        return redirect(f"/quotes")
    
def delete(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.delete()

    return redirect('/quotes')

def favorite(request, quote_id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=quote_id)
    user.favorited_quotes.add(quote)

    return redirect(f'/quotes/{quote_id}')

def unfavorite(request, quote_id):
    user = User.objects.get(id=request.session["user_id"])
    quote = Quote.objects.get(id=quote_id)
    # user.my_fav.remove(quote)
    user.favorited_quotes.remove(quote)

    return redirect(f'/quotes/{quote_id}')


def logout(request):
    request.session.clear()
    return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    
    return render(request, 'success.html', context)

