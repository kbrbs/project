from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Article, Progress, EducationalSection
from quizzes.models import Quiz
from django.db.models import Count, Avg
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from django import forms
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token as get_csrf_token
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
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.files.storage import default_storage


def home(request):
    # Retrieve featured lessons from EducationalSection
    featured = EducationalSection.objects.all().order_by('order')[:6]
    return render(request, 'core/home.html', {'featured': featured})


@login_required
def lesson_list(request, category=None):
    # Retrieve all educational sections
    qs = EducationalSection.objects.all().order_by('order')
    # Note: EducationalSection doesn't have category field, so we ignore category filter
    return render(request, 'core/lesson_list.html', {'articles': qs, 'category': category})

@login_required
def lesson_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    # try to find a related quiz
    quiz = Quiz.objects.filter(article=article).first()
    # Find related EducationalSection by matching title (as sections create articles with same title)
    section = EducationalSection.objects.filter(title=article.title).first()
    # Get all content images for the section
    section_images = []
    if section:
        section_images = section.content_images.all().order_by('order', 'created_at')
    return render(request, 'core/lesson_detail.html', {
        'article': article, 
        'quiz': quiz, 
        'section': section,
        'section_images': section_images
    })

@login_required
def festival_tour(request):
    # static structure for festival booths
    booths = [
    {'id': 'history', 'title': 'History Booth', 'summary': 'Origins and timeline'},
        {'id': 'recipe', 'title': 'Recipe Tent', 'summary': 'Step-by-step baking'},
        {'id': 'cultural', 'title': 'Cultural Stage', 'summary': 'Folk dances and songs'},
        {'id': 'farmers', 'title': "Farmer's Corner", 'summary': 'Planting & harvesting stories'},
    ]
    return render(request, 'core/festival_tour.html', {'booths': booths})

@login_required
def profile(request):
    # placeholder profile view
    return render(request, 'core/profile.html')


@login_required
@require_POST
def upload_profile_picture(request):
    """Handle AJAX upload of profile picture. Expects file field 'profile_picture'.

    Saves the uploaded file to the StudentProfile.profile_picture (using Django storage),
    and returns JSON with the public URL on success.
    """
    user = request.user
    profile, _ = StudentProfile.objects.get_or_create(user=user)
    upload = request.FILES.get('profile_picture')
    if not upload:
        return JsonResponse({'error': 'No file provided.'}, status=400)

    # Use the ImageField's save to ensure correct storage path (upload_to)
    try:
        # Optional: sanitize filename here if needed
        profile.profile_picture.save(upload.name, upload, save=True)
        url = profile.profile_picture.url
        return JsonResponse({'url': url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def update_profile(request):
    """Handle AJAX update of profile information (currently only full_name)."""
    import json
    try:
        data = json.loads(request.body)
        full_name = data.get('full_name', '').strip()
        
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        profile.full_name = full_name
        profile.save()
        
        return JsonResponse({'success': True, 'full_name': full_name})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    full_name = forms.CharField(max_length=200)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    grade = forms.ChoiceField(choices=[(str(i), f'Grade {i}') for i in range(7, 13)])

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


@csrf_protect
def login_view(request):
    """Custom login view: allow login by email or username and handle 'remember me'. If user must change password, redirect there."""
    error = None
    # Ensure CSRF cookie/token is available for the form
    if request.method == 'GET':
        try:
            get_csrf_token(request)
        except Exception:
            pass

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

            # If the account exists but is inactive, show a clear blocked message
            existing_user = User.objects.filter(username__iexact=username).first()
            if existing_user and not existing_user.is_active:
                error = 'Your account is blocked. Please contact the administrator.'
                return render(request, 'registration/login.html', {'form': form, 'error': error})

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # session expiry for remember
                if form.cleaned_data.get('remember'):
                    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days
                else:
                    request.session.set_expiry(0)  # browser session

                # Check if user needs to change password (only for regular users, not staff/admin)
                if not (user.is_staff or user.is_superuser):
                    profile = getattr(user, 'studentprofile', None)
                    if profile and profile.must_change_password:
                        return redirect('core:change_password')

                # If this is a staff/superuser account, send to the admin dashboard.
                # Regular users go to their profile page.
                if user.is_active and (user.is_staff or user.is_superuser):
                    messages.info(request, 'Logged in as admin — redirecting to admin dashboard.')
                    return redirect('core:admin_dashboard')

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
                # Redirect to profile page
                return redirect('core:profile')
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
