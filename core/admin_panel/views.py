from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django import forms
from django.db.models import Count

from core.models import Article, EducationalSection, MediaAsset, ContentModeration, Visit, Download
from django.http import JsonResponse, HttpResponse, FileResponse, HttpResponseRedirect
from django.conf import settings
import os
import csv
from django.forms import inlineformset_factory
from quizzes.models import Quiz, Question
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django import forms


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'core/admin_panel/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_articles'] = Article.objects.count()
        ctx['total_sections'] = EducationalSection.objects.count()
        ctx['total_media'] = MediaAsset.objects.count()
        ctx['total_users'] = 0
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            ctx['total_users'] = User.objects.count()
        except Exception:
            ctx['total_users'] = 0

        ctx['visits_last_7'] = Visit.objects.filter().count()
        ctx['downloads'] = Download.objects.count()
        # moderation stats
        ctx['moderation'] = ContentModeration.objects.values('status').annotate(count=Count('id'))
        return ctx


@staff_member_required
def visits_json(request):
    # Return visits per day for the last 14 days
    from django.utils import timezone
    from django.db.models.functions import TruncDate
    from django.db.models import Count
    try:
        end = timezone.now()
        start = end - timezone.timedelta(days=13)
        qs = Visit.objects.filter(created_at__date__gte=start.date()).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('day')
        data = {'labels': [], 'data': []}
        
        # Fill in missing dates with 0
        current = start.date()
        visit_dict = {r['day']: r['count'] for r in qs}
        while current <= end.date():
            data['labels'].append(current.isoformat())
            data['data'].append(visit_dict.get(current, 0))
            current += timezone.timedelta(days=1)
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'labels': [], 'data': [], 'error': str(e)})


@staff_member_required
def top_pages_json(request):
    from django.db.models import Count
    try:
        qs = Visit.objects.values('path').annotate(count=Count('id')).order_by('-count')[:10]
        data = {'labels': [r['path'] for r in qs], 'data': [r['count'] for r in qs]}
        
        # If no data, return sample data
        if not data['labels']:
            data = {
                'labels': ['No visits yet'],
                'data': [0]
            }
        
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'labels': ['Error'], 'data': [0], 'error': str(e)})


# Generic CRUD views for EducationalSection
class SectionForm(forms.ModelForm):
    class Meta:
        model = EducationalSection
        fields = ['title', 'slug', 'description', 'content', 'order']


@method_decorator(staff_member_required, name='dispatch')
class SectionListView(ListView):
    model = EducationalSection
    template_name = 'core/admin_panel/section_list.html'
    context_object_name = 'sections'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


@method_decorator(staff_member_required, name='dispatch')
class SectionCreateView(CreateView):
    model = EducationalSection
    form_class = SectionForm
    template_name = 'core/admin_panel/section_form.html'
    success_url = reverse_lazy('core:admin_dashboard')


@method_decorator(staff_member_required, name='dispatch')
class SectionUpdateView(UpdateView):
    model = EducationalSection
    form_class = SectionForm
    template_name = 'core/admin_panel/section_form.html'
    success_url = reverse_lazy('core:admin_dashboard')


@method_decorator(staff_member_required, name='dispatch')
class SectionDeleteView(DeleteView):
    model = EducationalSection
    template_name = 'core/admin_panel/confirm_delete.html'
    success_url = reverse_lazy('core:admin_dashboard')


# Media CRUD
class MediaForm(forms.ModelForm):
    class Meta:
        model = MediaAsset
        fields = ['title', 'asset_type', 'file', 'url', 'article']


@method_decorator(staff_member_required, name='dispatch')
class MediaListView(ListView):
    model = MediaAsset
    template_name = 'core/admin_panel/media_list.html'
    context_object_name = 'media_list'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


@method_decorator(staff_member_required, name='dispatch')
class MediaCreateView(CreateView):
    model = MediaAsset
    form_class = MediaForm
    template_name = 'core/admin_panel/media_form.html'
    success_url = reverse_lazy('core:admin_dashboard')


@method_decorator(staff_member_required, name='dispatch')
class MediaUpdateView(UpdateView):
    model = MediaAsset
    form_class = MediaForm
    template_name = 'core/admin_panel/media_form.html'
    success_url = reverse_lazy('core:admin_dashboard')


@method_decorator(staff_member_required, name='dispatch')
class MediaDeleteView(DeleteView):
    model = MediaAsset
    template_name = 'core/admin_panel/confirm_delete.html'
    success_url = reverse_lazy('core:admin_dashboard')


# Moderation list and update
@method_decorator(staff_member_required, name='dispatch')
class ModerationListView(ListView):
    model = ContentModeration
    template_name = 'core/admin_panel/moderation_list.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        if q:
            qs = qs.filter(notes__icontains=q)
        if status:
            qs = qs.filter(status=status)
        return qs


@staff_member_required
def download_media(request, pk):
    asset = get_object_or_404(MediaAsset, pk=pk)
    # Log download
    Download.objects.create(user=request.user if request.user.is_authenticated else None, media=asset)
    # Serve file if stored locally
    if asset.file:
        path = asset.file.path
        if os.path.exists(path):
            return FileResponse(open(path, 'rb'), as_attachment=True, filename=os.path.basename(path))
    # Fallback to redirecting to URL field or media URL
    if asset.url:
        return HttpResponseRedirect(asset.url)
    if asset.file:
        return HttpResponseRedirect(settings.MEDIA_URL + str(asset.file))
    return HttpResponse('File not available', status=404)


@staff_member_required
def export_visits_csv(request):
    qs = Visit.objects.all().order_by('-created_at')
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="visits.csv"'
    writer = csv.writer(resp)
    writer.writerow(['timestamp', 'path', 'user', 'ip', 'user_agent'])
    for v in qs:
        writer.writerow([v.created_at.isoformat(), v.path, v.user.username if v.user else '', v.ip_address, v.user_agent])
    return resp


@staff_member_required
def export_moderation_csv(request):
    qs = ContentModeration.objects.all().order_by('-created_at')
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="moderation.csv"'
    writer = csv.writer(resp)
    writer.writerow(['timestamp', 'target', 'status', 'moderator', 'notes'])
    for m in qs:
        target = m.article.title if m.article else (m.media.title if m.media else '')
        writer.writerow([m.created_at.isoformat(), target, m.status, m.moderator.username if m.moderator else '', m.notes])
    return resp


# Quiz CRUD with question formset
QuizFormSet = inlineformset_factory(Quiz, Question, fields=('text', 'choices'), extra=1, can_delete=True)


@method_decorator(staff_member_required, name='dispatch')
class QuizListView(ListView):
    model = Quiz
    template_name = 'core/admin_panel/quiz_list.html'
    context_object_name = 'quizzes'
    paginate_by = 12


@method_decorator(staff_member_required, name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ['title', 'article']
    template_name = 'core/admin_panel/quiz_form.html'
    success_url = reverse_lazy('core:admin_quizzes')


@method_decorator(staff_member_required, name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ['title', 'article']
    template_name = 'core/admin_panel/quiz_form.html'
    success_url = reverse_lazy('core:admin_quizzes')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = QuizFormSet(instance=self.object)
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = QuizFormSet(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            quiz = form.save()
            formset.save()
            messages.success(request, 'Quiz saved')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form, 'formset': formset})


@method_decorator(staff_member_required, name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = 'core/admin_panel/confirm_delete.html'
    success_url = reverse_lazy('core:admin_quizzes')


# User management
User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff', 'is_superuser']


@method_decorator(staff_member_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'core/admin_panel/user_list.html'
    context_object_name = 'users'
    paginate_by = 12

    def get_queryset(self):
        # Exclude superusers from the managed list
        qs = User.objects.filter(is_superuser=False).order_by('username').select_related()
        # prefetch the related StudentProfile for display
        qs = qs.prefetch_related('studentprofile')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(username__icontains=q) | qs.filter(email__icontains=q)
        return qs


@method_decorator(staff_member_required, name='dispatch')
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'core/admin_panel/user_form.html'
    success_url = reverse_lazy('core:admin_users')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(User.objects.make_random_password())
        user.save()
        # Create StudentProfile if needed
        from core.models import StudentProfile
        StudentProfile.objects.get_or_create(user=user)
        messages.success(self.request, 'User created')
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'core/admin_panel/user_form.html'
    success_url = reverse_lazy('core:admin_users')


@method_decorator(staff_member_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    template_name = 'core/admin_panel/confirm_delete.html'
    success_url = reverse_lazy('core:admin_users')


@staff_member_required
def moderation_update(request, pk):
    item = get_object_or_404(ContentModeration, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        item.status = status
        item.notes = notes
        item.moderator = request.user
        item.save()
        messages.success(request, 'Moderation updated.')
        return redirect('core:admin_moderation')
    return render(request, 'core/admin_panel/moderation_update.html', {'item': item})
