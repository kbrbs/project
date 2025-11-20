from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Article, Progress, EducationalSection, ActivityLog, FestivalDate
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
from .utils import log_activity
from .access_control import get_public_access_context


def home(request):
    """Homepage - fully public with featured lessons and call-to-action."""
    # Retrieve featured lessons from EducationalSection (show all 6 on homepage)
    featured = EducationalSection.objects.all().order_by('order')[:6]
    
    context = {
        'featured': featured,
    }
    context.update(get_public_access_context(request.user))
    return render(request, 'core/home.html', context)


def lesson_list(request, category=None):
    """Lesson list - fully public access to view all lessons."""
    # Retrieve all educational sections
    qs = EducationalSection.objects.all().order_by('order')
    
    # Handle category filtering from GET parameter
    category_filter = request.GET.get('category', '')
    if category_filter and category_filter in ['planting', 'cultural', 'historical', 'economic']:
        qs = qs.filter(category=category_filter)
    
    # Handle search query from GET parameter
    search_query = request.GET.get('q', '')
    if search_query:
        qs = qs.filter(title__icontains=search_query)
    
    total_lessons = qs.count()
    
    # Public users can see and access all lessons
    context = {
        'articles': qs,
        'category': category,
        'category_filter': category_filter,
        'search_query': search_query,
        'total_lessons': total_lessons,
    }
    context.update(get_public_access_context(request.user))
    
    return render(request, 'core/lesson_list.html', context)


def lesson_detail(request, slug):
    """Lesson detail - fully public access to view lessons."""
    section = get_object_or_404(EducationalSection, slug=slug)
    # Get all content images for the section
    section_images = section.content_images.all().order_by('order', 'created_at')
    # Get all content videos for the section
    section_videos = section.content_videos.all().order_by('order', 'created_at')
    
    # Try to find a related quiz (look for quiz linked to article with same title, if any)
    quiz = None
    article = Article.objects.filter(title=section.title).first()
    if article:
        quiz = Quiz.objects.filter(article=article).first()
    
    # Log activity (only for authenticated users)
    if request.user.is_authenticated:
        log_activity(
            user=request.user,
            category='progress',
            action='lesson_viewed',
            description=f'Viewed lesson: {section.title}',
            request=request,
            article=article
        )
    
    return render(request, 'core/lesson_detail.html', {
        'section': section,
        'quiz': quiz,
        'section_images': section_images,
        'section_videos': section_videos
    })

def festival_tour(request):
    """Festival tour - public can view, downloads require login."""
    # static structure for festival booths
    booths = [
        {'id': 'history', 'title': 'History Booth', 'summary': 'Origins and timeline'},
        {'id': 'recipe', 'title': 'Recipe Tent', 'summary': 'Step-by-step baking'},
        {'id': 'cultural', 'title': 'Cultural Stage', 'summary': 'Folk dances and songs'},
        {'id': 'farmers', 'title': "Farmer's Corner", 'summary': 'Planting & harvesting stories'},
    ]
    
    # Get festival date from database
    festival_date_obj = FestivalDate.get_instance()
    festival_date = festival_date_obj.festival_date if festival_date_obj else None
    
    # Log activity (only for authenticated users)
    if request.user.is_authenticated:
        log_activity(
            user=request.user,
            category='content',
            action='festival_tour',
            description='Visited Festival Tour',
            request=request
        )
    else:
        # Show info for public users
        messages.info(
            request,
            '🎉 Enjoying the virtual festival tour? Register FREE to access interactive features '
            'and downloadable festival materials!'
        )
    
    context = {
        'booths': booths,
        'festival_date': festival_date,
    }
    context.update(get_public_access_context(request.user))
    return render(request, 'core/festival_tour.html', context)

@login_required
def profile(request):
    from games.models import GameAttempt
    from quizzes.models import QuizAttempt
    from django.db.models import Count, Avg, Sum, F, FloatField
    from django.db.models.functions import Cast
    
    # Get recent activities for the user
    recent_activities = ActivityLog.objects.filter(user=request.user)[:10]
    
    # Get game attempts
    game_attempts = GameAttempt.objects.filter(
        user=request.user,
        completed=True
    ).select_related('game').order_by('-created_at')[:10]
    
    # Calculate game statistics
    game_stats = GameAttempt.objects.filter(
        user=request.user,
        completed=True
    ).aggregate(
        total_games=Count('id'),
        total_score=Sum('score'),
        avg_score=Avg('score'),
        avg_max_score=Avg('max_score')
    )
    
    # Calculate average percentage manually after aggregation
    if game_stats['avg_max_score'] and game_stats['avg_max_score'] > 0:
        game_stats['avg_percentage'] = (game_stats['avg_score'] / game_stats['avg_max_score']) * 100
    else:
        game_stats['avg_percentage'] = 0
    
    # Get best scores per game
    from django.db.models import Max
    best_scores = {}
    for attempt in GameAttempt.objects.filter(user=request.user, completed=True).values('game_id').annotate(best_score=Max('score')):
        best_scores[attempt['game_id']] = attempt['best_score']
    
    # Get quiz attempts
    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user,
        completed=True
    ).select_related('quiz').order_by('-created_at')[:10]
    
    # Calculate quiz statistics
    quiz_stats = QuizAttempt.objects.filter(
        user=request.user,
        completed=True
    ).aggregate(
        total_quizzes=Count('id'),
        total_score=Sum('score'),
        avg_score=Avg('score'),
        avg_total_questions=Avg('total_questions')
    )
    
    # Calculate average percentage manually after aggregation
    if quiz_stats['avg_total_questions'] and quiz_stats['avg_total_questions'] > 0:
        quiz_stats['avg_percentage'] = (quiz_stats['avg_score'] / quiz_stats['avg_total_questions']) * 100
    else:
        quiz_stats['avg_percentage'] = 0
    
    context = {
        'recent_activities': recent_activities,
        'game_attempts': game_attempts,
        'game_stats': game_stats,
        'best_scores': best_scores,
        'quiz_attempts': quiz_attempts,
        'quiz_stats': quiz_stats,
    }
    
    return render(request, 'core/profile.html', context)


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
        
        # Log activity
        log_activity(
            user=user,
            category='profile',
            action='avatar_upload',
            description='Uploaded new profile picture',
            request=request
        )
        
        return JsonResponse({'url': url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def update_profile(request):
    """Handle AJAX update of profile information (full_name, grade, birthday)."""
    import json
    from datetime import datetime
    try:
        data = json.loads(request.body)
        full_name = data.get('full_name', '').strip()
        grade = data.get('grade', '').strip()
        birthday_str = data.get('birthday', '').strip()
        
        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        
        # Track what changed for logging
        changes = []
        if full_name and full_name != profile.full_name:
            changes.append(f'name to "{full_name}"')
            profile.full_name = full_name
        
        # Update grade if provided
        if grade:
            try:
                grade_int = int(grade)
                if profile.grade != grade_int:
                    changes.append(f'grade to {grade_int}')
                    profile.grade = grade_int
            except (ValueError, TypeError):
                pass
        
        # Update birthday if provided
        if birthday_str:
            try:
                new_birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                if profile.birthday != new_birthday:
                    changes.append(f'birthday to {new_birthday}')
                    profile.birthday = new_birthday
            except (ValueError, TypeError):
                pass
        
        profile.save()
        
        # Log activity
        if changes:
            log_activity(
                user=request.user,
                category='profile',
                action='profile_update',
                description=f'Updated profile: {", ".join(changes)}',
                request=request,
                metadata={'changes': changes}
            )
        
        return JsonResponse({
            'success': True, 
            'full_name': full_name,
            'grade': profile.grade,
            'birthday': profile.birthday.strftime('%Y-%m-%d') if profile.birthday else None
        })
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

            # Log account creation
            log_activity(
                user=user,
                category='system',
                action='account_created',
                description=f'New account created: {full_name} ({username})',
                request=request,
                metadata={'grade': grade, 'email': email}
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

                # Log successful login
                log_activity(
                    user=user,
                    category='security',
                    action='login',
                    description='User logged in successfully',
                    request=request
                )

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
                # Log failed login attempt
                try:
                    user_obj = User.objects.filter(username__iexact=username).first()
                    if user_obj:
                        log_activity(
                            user=user_obj,
                            category='security',
                            action='failed_login',
                            description=f'Failed login attempt for user: {username}',
                            request=request
                        )
                except:
                    pass
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
                
                # Log password change
                log_activity(
                    user=request.user,
                    category='security',
                    action='password_change',
                    description='User changed their password',
                    request=request
                )
                
                # Redirect to profile page
                return redirect('core:profile')
    return render(request, 'registration/change_password.html', {'error': error, 'success': success})


def logout_view(request):
    """Log out the current user and redirect to homepage."""
    user = request.user
    if user.is_authenticated:
        # Log logout activity
        log_activity(
            user=user,
            category='security',
            action='logout',
            description='User logged out',
            request=request
        )
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
