from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.forms import inlineformset_factory, modelformset_factory
from django import forms
from django.utils.http import url_has_allowed_host_and_scheme
from games.models import Game, GameQuestion, GameOption, GameAttempt
from django.db.models import Count, Avg, Q
import json


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'game_type', 'description', 'article', 'difficulty', 'time_limit', 'points_per_correct', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class GameQuestionForm(forms.ModelForm):
    class Meta:
        model = GameQuestion
        fields = [
            'order', 'question_text', 'word', 
            'sentence_template', 'correct_answers', 'extra_choices',  # Drag-drop fields
            'question_image', 'text_choices', 'correct_answer',  # Image identification fields
            'correct_sequence', 'memory_pairs', 'explanation',
            # Memory match with images fields
            'grid_size',
            'memory_image_1', 'memory_image_2', 'memory_image_3', 'memory_image_4',
            'memory_image_5', 'memory_image_6', 'memory_image_7', 'memory_image_8',
            'memory_image_9', 'memory_image_10', 'memory_image_11', 'memory_image_12',
            'memory_image_13', 'memory_image_14', 'memory_image_15', 'memory_image_16',
            'memory_image_17', 'memory_image_18',
        ]
        widgets = {
            'order': forms.NumberInput(attrs={'readonly': 'readonly', 'style': 'background-color: #F3F4F6; cursor: not-allowed;'}),
            'question_text': forms.Textarea(attrs={'rows': 2}),
            'sentence_template': forms.Textarea(attrs={'rows': 2, 'placeholder': 'The city of * is famous for *'}),
            'correct_answers': forms.TextInput(attrs={'placeholder': 'Bustos, Minasa'}),
            'extra_choices': forms.TextInput(attrs={'placeholder': 'Manila, rice cake, Bataan'}),
            'question_image': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp'}),
            'text_choices': forms.TextInput(attrs={'placeholder': 'Arrowroot leaf, Cassava root, Minasa flour, Rice grain'}),
            'correct_answer': forms.TextInput(attrs={'placeholder': 'Arrowroot leaf'}),
            'correct_sequence': forms.Textarea(attrs={'rows': 2, 'placeholder': '["Step 1", "Step 2", "Step 3"]'}),
            'memory_pairs': forms.Textarea(attrs={'rows': 2, 'placeholder': '{"Term": "Definition", "Word": "Meaning"}'}),
            'explanation': forms.Textarea(attrs={'rows': 2}),
            # Memory match images
            'memory_image_1': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_2': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_3': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_4': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_5': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_6': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_7': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_8': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_9': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_10': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_11': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_12': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_13': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_14': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_15': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_16': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_17': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
            'memory_image_18': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/jpg,image/png,image/gif,image/webp', 'class': 'memory-image-input'}),
        }


# Formset for questions
GameQuestionFormSet = inlineformset_factory(
    Game, GameQuestion,
    form=GameQuestionForm,
    extra=1,
    can_delete=True
)


# Formset for options (for image identification and MCQ games)
GameOptionFormSet = inlineformset_factory(
    GameQuestion, GameOption,
    fields=['option_text', 'option_image', 'is_correct', 'order'],
    extra=2,
    can_delete=True
)


@method_decorator(staff_member_required, name='dispatch')
class GameListView(ListView):
    model = Game
    template_name = 'core/admin_panel/game_list.html'
    context_object_name = 'games'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        game_type = self.request.GET.get('type')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if game_type:
            qs = qs.filter(game_type=game_type)
        return qs.annotate(attempts_count=Count('attempts'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['game_types'] = Game.GAME_TYPE_CHOICES
        return ctx


@method_decorator(staff_member_required, name='dispatch')
class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'core/admin_panel/game_form.html'
    success_url = reverse_lazy('core:admin_games')

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = GameQuestionFormSet()
        return render(request, self.template_name, {'form': form, 'formset': formset})

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = GameQuestionFormSet(request.POST, request.FILES)  # Added request.FILES for image uploads
        if form.is_valid() and formset.is_valid():
            game = form.save()
            formset.instance = game
            
            # Save each form individually to ensure all fields are committed
            saved_count = 0
            for form_instance in formset.forms:
                if form_instance.cleaned_data and not form_instance.cleaned_data.get('DELETE', False):
                    question = form_instance.save(commit=False)
                    question.game = game  # Ensure foreign key is set
                    question.save()
                    saved_count += 1
            
            messages.success(request, f'Game "{game.title}" created successfully with {saved_count} questions!')
            # Respect safe "next" parameter if provided
            next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)
            return redirect(self.success_url)
        else:
            if not form.is_valid():
                messages.error(request, f'Game form errors: {form.errors}')
            if not formset.is_valid():
                messages.error(request, f'Question formset errors: {formset.errors}')
        return render(request, self.template_name, {'form': form, 'formset': formset})


@method_decorator(staff_member_required, name='dispatch')
class GameUpdateView(UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'core/admin_panel/game_form.html'
    success_url = reverse_lazy('core:admin_games')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = GameQuestionFormSet(instance=self.object)
        return render(request, self.template_name, {'form': form, 'formset': formset, 'game': self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = GameQuestionFormSet(request.POST, request.FILES, instance=self.object)  # Added request.FILES for image uploads
        
        # Debug: Print POST data for drag-drop fields
        print("\n=== DEBUG: POST Data for Drag-Drop Fields ===")
        for key in request.POST:
            if 'sentence_template' in key or 'correct_answers' in key or 'extra_choices' in key:
                print(f"POST {key}: {request.POST[key]}")
        print("=== END DEBUG ===\n")
        
        if form.is_valid() and formset.is_valid():
            game = form.save()
            
            # Save each form in the formset individually to ensure all fields are saved
            print(f"\n=== Saving formset with {len(formset.forms)} forms ===")
            saved_count = 0
            deleted_count = 0
            
            for form_instance in formset.forms:
                if form_instance.cleaned_data:
                    # Check if marked for deletion
                    if form_instance.cleaned_data.get('DELETE', False):
                        # Delete the instance if it exists in DB
                        if form_instance.instance.pk:
                            print(f"Deleting Question ID={form_instance.instance.pk}")
                            form_instance.instance.delete()
                            deleted_count += 1
                    else:
                        # Save the instance
                        question = form_instance.save(commit=False)
                        question.game = game  # Ensure FK is set
                        print(f"Saving Question ID={question.id}, Order={question.order}")
                        print(f"  sentence_template: '{question.sentence_template}'")
                        print(f"  correct_answers: '{question.correct_answers}'")
                        print(f"  extra_choices: '{question.extra_choices}'")
                        print(f"  question_image: '{question.question_image}'")
                        print(f"  text_choices: '{question.text_choices}'")
                        print(f"  correct_answer: '{question.correct_answer}'")
                        question.save()
                        saved_count += 1
            
            print(f"=== Completed: Saved {saved_count} questions, deleted {deleted_count} ===\n")
            messages.success(request, f'Game "{game.title}" updated successfully! Saved {saved_count} questions.')
            # Respect safe "next" parameter if provided
            next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                return redirect(next_url)
            return redirect(self.success_url)
        else:
            # Add error messages for debugging
            if not form.is_valid():
                messages.error(request, f'Game form errors: {form.errors}')
            if not formset.is_valid():
                messages.error(request, f'Question formset errors: {formset.errors}')
                print(f"\n=== FORMSET ERRORS ===")
                for i, form_errors in enumerate(formset.errors):
                    if form_errors:
                        print(f"Form {i} errors: {form_errors}")
                print("=== END FORMSET ERRORS ===\n")
        return render(request, self.template_name, {'form': form, 'formset': formset, 'game': self.object})


@method_decorator(staff_member_required, name='dispatch')
class GameDeleteView(DeleteView):
    model = Game
    template_name = 'core/admin_panel/confirm_delete.html'
    success_url = reverse_lazy('core:admin_games')

    def delete(self, request, *args, **kwargs):
        game = self.get_object()
        messages.success(request, f'Game "{game.title}" has been permanently deleted.')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next') or self.request.META.get('HTTP_REFERER')
        if next_url:
            return next_url
        return super().get_success_url()


@staff_member_required
def game_question_options(request, pk):
    """Manage options for a specific game question (for image ID and MCQ games)."""
    question = get_object_or_404(GameQuestion, pk=pk)
    
    if request.method == 'POST':
        formset = GameOptionFormSet(request.POST, request.FILES, instance=question)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Options saved successfully!')
            return redirect('core:admin_game_update', pk=question.game.pk)
    else:
        formset = GameOptionFormSet(instance=question)
    
    return render(request, 'core/admin_panel/game_options_form.html', {
        'question': question,
        'formset': formset
    })


@staff_member_required
def game_stats(request):
    """View game statistics and leaderboards."""
    # Top games by attempts
    top_games = Game.objects.annotate(
        attempt_count=Count('attempts'),
        avg_score=Avg('attempts__score')
    ).order_by('-attempt_count')[:10]
    
    # Top students
    from django.contrib.auth import get_user_model
    User = get_user_model()
    top_students = User.objects.annotate(
        total_attempts=Count('game_attempts'),
        avg_score=Avg('game_attempts__score')
    ).filter(total_attempts__gt=0).order_by('-total_attempts')[:10]
    
    # Recent attempts
    recent_attempts = GameAttempt.objects.select_related('user', 'game').order_by('-created_at')[:20]
    
    return render(request, 'core/admin_panel/game_stats.html', {
        'top_games': top_games,
        'top_students': top_students,
        'recent_attempts': recent_attempts,
    })
