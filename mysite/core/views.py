from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse

from social_django.models import UserSocialAuth

from .gbooks import search_books, get_book_info

BOOK_ENTRY = '''<span class="searchResWrapper"><span class="searchRes" id="{id}"><img class="miniAvatar" src="{thumb}">{title}</span></span>\n'''


def _parse_response(items):
    for item in items:
        try:
            id_ = item['id']
            title = item['volumeInfo']['title']
            thumb = item['volumeInfo']['imageLinks']['smallThumbnail']
        except KeyError:
            continue
        book_entry = BOOK_ENTRY.format(id=id_, title=title, thumb=thumb)
        yield book_entry


def get_books(request):
    no_result = HttpResponse('fail')

    try:
        term = request.GET.get('q')
    except:
        return no_result

    term = request.GET.get('q', '')
    books = search_books(term)
    items = books.get('items')
    if not items:
        return no_result

    data = list(_parse_response(items))

    return HttpResponse(data)


def book_page(request, bookid):
    resp = get_book_info(bookid)
    book = dict(
        id=bookid,
        title=resp['volumeInfo']['title'],
        description=resp['volumeInfo'].get('description', 'no description found'),
        authors=', '.join(resp['volumeInfo']['authors']),
        isbn=resp['volumeInfo']['industryIdentifiers'][-1]['identifier'],
        lang=resp['volumeInfo']['language'],
        pages=resp['volumeInfo']['pageCount'],
        release_date=resp['volumeInfo']['publishedDate'],
        publisher=resp['volumeInfo']['publisher'].strip('"'),
        amazon_reviews='',  # TODO
    )
    return render(request, 'core/book.html', {'book': book})



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def home(request):
    return render(request, 'core/home.html')


@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1
                      or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')  # noqa E501
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
