from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Article, Progress
from quizzes.models import Quiz
from django.db.models import Count, Avg
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.password_validation import validate_password, ValidationError as PasswordValidationError
import secrets
from .models import StudentProfile
from django.contrib.auth import logout as auth_logout


def home(request):
    # sample hero articles and categories
    featured = Article.objects.all()[:4]
    return render(request, 'core/home.html', {'featured': featured})


def lesson_list(request, category=None):
    qs = Article.objects.all()
    if category:
        qs = qs.filter(category=category)
    return render(request, 'core/lesson_list.html', {'articles': qs, 'category': category})


def lesson_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    # try to find a related quiz
    quiz = Quiz.objects.filter(article=article).first()
    return render(request, 'core/lesson_detail.html', {'article': article, 'quiz': quiz})


def festival_tour(request):
    # static structure for festival booths
    booths = [
    {'id': 'history', 'title': 'History Booth', 'summary': 'Origins and timeline'},
        {'id': 'recipe', 'title': 'Recipe Tent', 'summary': 'Step-by-step baking'},
        {'id': 'cultural', 'title': 'Cultural Stage', 'summary': 'Folk dances and songs'},
        {'id': 'farmers', 'title': "Farmer's Corner", 'summary': 'Planting & harvesting stories'},
    ]
    return render(request, 'core/festival_tour.html', {'booths': booths})


def profile(request):
    # placeholder profile view
    return render(request, 'core/profile.html')


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    full_name = forms.CharField(max_length=200)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    grade = forms.ChoiceField(choices=[(str(i), f'Grade {i}') for i in range(1, 13)])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Enter a valid email address.')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken.')
        return username


def signup(request):
    """Signup: collect profile info, create user with temporary password and email it."""
    success = None
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            birthday = form.cleaned_data['birthday']
            grade = int(form.cleaned_data['grade'])

            # generate a temporary password
            temp_password = secrets.token_urlsafe(8)

            user = User.objects.create_user(username=username, email=email)
            user.set_password(temp_password)
            user.save()

            profile = StudentProfile.objects.create(
                user=user,
                full_name=full_name,
                birthday=birthday,
                grade=grade,
                must_change_password=True,
            )

            # send the temporary password via email (console backend in dev)
            subject = 'Your temporary password for Rooted in Knowledge'
            message = (
                f'Hello {full_name},\n\n'
                f'Your account has been created. Use the temporary password below to log in for the first time:\n\n'
                f'Username: {username}\n'
                f'Temporary password: {temp_password}\n\n'
                'After logging in you will be prompted to set a new password.'
            )
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'katrinamicaellabarbosa@gmail.com')
            sent = send_mail(subject, message, from_email, [email])

            if sent:
                # Inform the user (via messages) that an email was sent to their address.
                messages.success(request, f'A temporary password was sent to {email}. Please check your inbox.')
            else:
                messages.error(request, 'Account created but we could not send the temporary password by email. Please contact the administrator.')

            # After successful registration, redirect to the login page so the user
            # can sign in using the temporary password sent to their email.
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form, 'success': success})


class LoginForm(forms.Form):
    username = forms.CharField(label='Email or Username')
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField(required=False)


def login_view(request):
    """Custom login view: allow login by email or username and handle 'remember me'. If user must change password, redirect there."""
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # resolve email to username if necessary
            user_obj = None
            if '@' in identifier:
                user_obj = User.objects.filter(email__iexact=identifier).first()
            if user_obj:
                username = user_obj.username
            else:
                username = identifier

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # session expiry for remember
                if form.cleaned_data.get('remember'):
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
                else:
                    request.session.set_expiry(0)  # browser session

                # check if user needs to change password
                profile = getattr(user, 'studentprofile', None)
                if profile and profile.must_change_password:
                    return redirect('core:change_password')

                return redirect('core:profile')
            else:
                error = 'Invalid credentials. Please check your username/email and password.'
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'error': error})


@login_required
def change_password(request):
    """Allow a logged-in user to set a new password (used after first-login temporary password)."""
    error = None
    success = None
    if request.method == 'POST':
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        if not p1 or not p2:
            error = 'Please enter and confirm your new password.'
        elif p1 != p2:
            error = 'Passwords do not match.'
        else:
            try:
                validate_password(p1, user=request.user)
            except PasswordValidationError as e:
                error = ' '.join(e.messages)
            else:
                request.user.set_password(p1)
                request.user.save()
                # clear the must_change_password flag
                profile = getattr(request.user, 'studentprofile', None)
                if profile:
                    profile.must_change_password = False
                    profile.save()
                # keep the user logged in after password change
                update_session_auth_hash(request, request.user)
                # Redirect to homepage for learning
                return redirect('core:home')
    return render(request, 'registration/change_password.html', {'error': error, 'success': success})


def logout_view(request):
    """Log out the current user and redirect to homepage."""
    auth_logout(request)
    return redirect('core:home')


@staff_member_required
def teacher_dashboard(request):
    """Teacher dashboard page. Charts will fetch data from analytics_api."""
    return render(request, 'core/teacher_dashboard.html')


@staff_member_required
def analytics_api(request):
    # simple analytics: top visited lessons (by progress entries), quiz averages
    top_lessons = (
        Progress.objects.values('article__id', 'article__title')
        .annotate(visits=Count('id'))
        .order_by('-visits')[:10]
    )

    quiz_avg = (
        Progress.objects.exclude(score__isnull=True)
        .values('quiz_id')
        .annotate(avg_score=Avg('score'), attempts=Count('id'))
        .order_by('-attempts')
    )

    data = {
        'top_lessons': list(top_lessons),
        'quiz_avg': list(quiz_avg),
    }
    return JsonResponse(data)
