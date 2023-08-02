from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import Player, UserProfile

# Create your views here.
class IndexView(TemplateView):
    template_name = 'pages/index.html'

def example_view(request):
    return render(request, 'pages/example.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verify the username and password using Django's authenticate method
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # If the user is authenticated, log them in
            login(request, user)
            return render(request, 'game.html', {'username': username})
        else:
            # If the user is not authenticated, show an error message
            error_message = 'Invalid username or password.'
            return render(request, 'index.html', {'error_message': error_message})
    else:
        return render(request, 'index.html')

def game_view(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        player_name = request.POST['player_name'].upper()

        try:
            player = Player.objects.get(name=player_name)
        except Player.DoesNotExist:
            player = None

        if player:
            user_profile, created = UserProfile.objects.get_or_create(user=user_name)
            user_profile.pontuation += 5
            user_profile.save()
            return render(request, 'pages/game.html', {'player': player, 'correct': True})
        else:
            user_profile, created = UserProfile.objects.get_or_create(user=user_name)
            user_profile.pontuation -= 1
            user_profile.save()
            return render(request, 'pages/game.html', {'correct': False})

    players = Player.objects.all()
    return render(request, 'pages/game.html', {'players': players})
