from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Vote
from .forms import UserProfileForm
from django.shortcuts import render, get_object_or_404
from .models import Poll
from .forms import PollVoteForm

def index(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            # Сохраняем пользователя
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Хэшируем пароль
            user.save()

            # Создаём профиль пользователя с аватаром
            profile = profile_form.save(commit=False)
            profile.user = user  # Связываем профиль с пользователем
            profile.save()

            login(request, user)  # Логиним пользователя после регистрации
            return redirect('home')  # Перенаправляем на главную страницу после регистрации
    else:
        form = RegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'registration/register.html', {'form': form, 'profile_form': profile_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Аутентификация успешна, получаем пользователя и логиним его
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Перенаправляем на домашнюю страницу после успешного входа
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('registration/login')  # Перенаправляем на страницу логина после выхода


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)  # Получаем профиль пользователя
    return render(request, 'registration/profile.html', {'profile': user_profile})


@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)  # Получаем профиль пользователя
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправляем на страницу профиля
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'registration/edit_profile.html', {'form': form})

@login_required
def delete_profile(request):
    user = request.user

    if request.method == 'POST':
        # Удаляем профиль пользователя
        user.delete()
        return redirect('home')  # Перенаправляем на главную страницу после удаления

    # Если это GET-запрос, то показываем страницу с подтверждением
    return render(request, 'registration/delete_profile.html')

def poll_list(request):
    polls = Poll.objects.filter(is_active=True)  # Показываем только активные голосования
    return render(request, 'main/poll_list.html', {'polls': polls})

@login_required
def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    # Проверяем, голосовал ли уже пользователь
    user_vote = Vote.objects.filter(user=request.user, poll=poll).first()

    if request.method == 'POST' and not user_vote:
        form = PollVoteForm(request.POST, poll=poll)
        if form.is_valid():
            # Сохраняем голос пользователя для выбранных вариантов
            for option in poll.options.all():
                if form.cleaned_data.get(f'option_{option.id}'):
                    Vote.objects.create(user=request.user, poll=poll, option=option)
                    option.votes += 1
                    option.save()

            # После голосования мы обновляем переменную user_vote, чтобы показать результаты
            user_vote = Vote.objects.filter(user=request.user, poll=poll).first()

            return redirect('poll_detail', poll_id=poll.id)  # Перенаправляем обратно на страницу голосования
    else:
        form = PollVoteForm(poll=poll)

    # Рассчитываем процент голосов для каждого варианта только если есть голоса
    total_votes = sum(option.votes for option in poll.options.all())
    if total_votes > 0:
        for option in poll.options.all():
            option.vote_percentage = (option.votes / total_votes) * 100
    else:
        for option in poll.options.all():
            option.vote_percentage = 0

    # Передаем в шаблон данные о голосах и проголосовал ли пользователь
    return render(request, 'main/poll_detail.html', {
        'poll': poll,
        'form': form,
        'user_vote': user_vote,
    })