from django.shortcuts import render, redirect, get_object_or_404
from .models import TicTacToe
from django.http import JsonResponse
import time
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

# Create your views here.

def home(request):
    try:
        game = TicTacToe.objects.get(creator=request.user)
        game.delete()
    except:
        pass
    return render(request, 'game\home.html')


@login_required
def creategame(request):
    try:
        game = TicTacToe.objects.get(creator=request.user)
        game.delete()
    except TicTacToe.DoesNotExist:
        pass

    game = TicTacToe(
        creator=request.user,
        player = ''
    )
    game.save()
    return render(request, 'game\waiting.html')


@login_required
def game(request):
    #game = get_object_or_404(TicTacToe, creator=request.user)
    games = TicTacToe.objects.all()
    for game in games:
        if game.creator == request.user or game.player == request.user.username:
            return render(request, 'game\game.html', {"game": game, "player":game.get_current_player()})
    else:
        return redirect('home')


@login_required
def make_move(request, position):
    games = TicTacToe.objects.all()
    for game in games:
        if game.creator == request.user or game.player == request.user.username:
            break
    if game.get_current_player() == request.user.username:
        game.make_move(int(position))
    return redirect('game:game')


@login_required
def waitingplayer(request):
    game = get_object_or_404(TicTacToe, creator=request.user)
    while not game.player:
        game = get_object_or_404(TicTacToe, creator=request.user)
        time.sleep(1)  # Приостановка выполнения на 1 секунду
    return HttpResponse('Player field is filled')

@login_required
def waitingmove(request):
    game = TicTacToe.objects.filter(Q(creator=request.user) | Q(player=request.user.username))[0]
    board = game.board
    while game.board == board:
        game1 = TicTacToe.objects.filter(Q(creator=request.user) | Q(player=request.user.username))[0]
        board = game1.board
        time.sleep(1)  # Приостановка выполнения на 1 секунду
    return HttpResponse('Player field is filled')


@login_required
def servers(request):
    try:
        game = TicTacToe.objects.get(creator=request.user)
        game.delete()
    except TicTacToe.DoesNotExist:
        pass
    games = TicTacToe.objects.filter(Q(player='') | Q(player=request.user.username))
    return render(request, "game\servers.html", {'games':games, "user":request.user})


@login_required
def serverjoin(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    game = get_object_or_404(TicTacToe, creator=user)
    game.player = request.user.username
    game.save()
    return redirect('game:game')


def singupuser(request):
    if request.method == "GET":
        return render(request, 'game\singupuser.html', {"form": UserCreationForm()})
    elif request.method == "POST":
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect("home")
            except IntegrityError:
                return render(request, 'game/singupuser.html', {"form": UserCreationForm(), 'error': "That username has been taken"})
        else:
            return render(request, 'game/singupuser.html', {"form": UserCreationForm(), 'error': "Passwords didn't match"})


def loginuser(request):
    if request.method == "GET":
        return render(request, 'game/loginuser.html', {"form": AuthenticationForm()})
    elif request.method == "POST":
        user = authenticate(request, username= request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'game/loginuser.html', {"form": AuthenticationForm(), 'error': "Username or password didn't match"})
        else:
            login(request, user)
            return redirect("home")


@login_required
def logoutuser(request):
    if request.method == "POST":
        try:
            game = TicTacToe.objects.get(creator=request.user)
            game.delete()
        except:
            pass
        logout(request)
        return redirect('home')
