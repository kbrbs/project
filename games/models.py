from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, FileExtensionValidator
import json

User = get_user_model()


class Game(models.Model):
    """Represents a game/activity with a specific type and learning objective."""
    
    GAME_TYPE_CHOICES = [
        ('word_scramble', 'Word Scramble'),
        ('drag_drop', 'Drag and Drop Sorting'),
        ('image_identification', 'Image Identification'),
        ('memory_match', 'Memory Matching'),
    ]
    
    title = models.CharField(max_length=200)
    game_type = models.CharField(max_length=30, choices=GAME_TYPE_CHOICES)
    description = models.TextField(help_text="Learning goal and game instructions")
    article = models.ForeignKey('core.Article', on_delete=models.SET_NULL, null=True, blank=True, related_name='games')
    difficulty = models.CharField(max_length=20, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium')
    time_limit = models.IntegerField(null=True, blank=True, help_text="Time limit in seconds (optional)")
    points_per_correct = models.IntegerField(default=10, validators=[MinValueValidator(1)])
    order = models.PositiveIntegerField(default=0, help_text="Display order in game list")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_game_type_display()})"


class GameQuestion(models.Model):
    """Question/item within a game. Structure varies by game type."""
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='questions')
    order = models.IntegerField(default=0, help_text="Display order")
    
    # Common fields
    question_text = models.TextField(help_text="Question prompt or instruction")
    
    # For word_scramble: word to scramble
    word = models.CharField(max_length=100, blank=True, help_text="Word Scramble: the word to unscramble")
    
    # For drag_drop: fill-in-the-blanks with drag-drop
    sentence_template = models.TextField(blank=True, help_text="Drag-Drop: Sentence with blanks marked by * or _, e.g. 'Peter * picked a * peckpeck'")
    correct_answers = models.TextField(blank=True, help_text="Drag-Drop: Correct answers for each blank (comma-separated), e.g. 'piper, peck of'")
    extra_choices = models.TextField(blank=True, help_text="Drag-Drop: Additional wrong choices (comma-separated), e.g. 'pepper, pack, pick'")
    
    # Legacy field for sorting-type drag-drop (kept for backward compatibility)
    correct_sequence = models.TextField(blank=True, help_text="Drag-Drop Sorting: JSON array of correct order, e.g. ['Step 1', 'Step 2']")
    
    # For image_identification: image as question, text choices as answers
    question_image = models.ImageField(
        upload_to='game_images/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        help_text="Image Identification: The image to identify (jpg, jpeg, png, gif, webp only)"
    )
    text_choices = models.TextField(blank=True, help_text="Image Identification: Text choices (comma-separated), e.g. 'Arrowroot leaf, Cassava root, Minasa flour, Rice grain'")
    correct_answer = models.CharField(max_length=200, blank=True, help_text="Image Identification: The correct text answer (must match one of the choices)")
    
    # For memory_match: pairs stored as JSON (legacy text-based)
    memory_pairs = models.TextField(blank=True, help_text="Memory Match: JSON object of pairs, e.g. {'Arrowroot': 'Plant used for Minasa flour'}")
    
    # For memory_match with images: grid size and image fields
    grid_size = models.CharField(
        max_length=10,
        blank=True,
        choices=[
            ('2x2', '2x2 (2 pairs)'),
            ('3x3', '3x3 (3 pairs)'),
            ('4x4', '4x4 (4 pairs)'),
            ('5x5', '5x5 (5 pairs)'),
            ('6x6', '6x6 (6 pairs)'),
            ('7x7', '7x7 (7 pairs)'),
            ('8x8', '8x8 (8 pairs)'),
            ('9x9', '9x9 (9 pairs)'),
        ],
        help_text="Memory Match: Grid size for image-based memory game"
    )
    memory_image_1 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_2 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_3 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_4 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_5 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_6 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_7 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_8 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_9 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_10 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_11 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_12 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_13 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_14 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_15 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_16 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_17 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    memory_image_18 = models.ImageField(upload_to='game_images/memory/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])])
    
    # Explanation shown after answering
    explanation = models.TextField(blank=True, help_text="Educational explanation shown after answer")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.game.title} - Q{self.order}"
    
    def get_correct_sequence_list(self):
        """Parse correct_sequence JSON to list."""
        if self.correct_sequence:
            try:
                return json.loads(self.correct_sequence)
            except:
                return []
        return []
    
    def get_memory_pairs_dict(self):
        """Parse memory_pairs JSON to dict."""
        if self.memory_pairs:
            try:
                return json.loads(self.memory_pairs)
            except:
                return {}
        return {}
    
    def get_correct_answers_list(self):
        """Get list of correct answers for drag-drop blanks."""
        if self.correct_answers:
            return [answer.strip() for answer in self.correct_answers.split(',') if answer.strip()]
        return []
    
    def get_extra_choices_list(self):
        """Get list of extra wrong choices for drag-drop."""
        if self.extra_choices:
            return [choice.strip() for choice in self.extra_choices.split(',') if choice.strip()]
        return []
    
    def get_blanks_count(self):
        """Count number of blanks in sentence template."""
        if self.sentence_template:
            return self.sentence_template.count('*') + self.sentence_template.count('_')
        return 0
    
    def get_text_choices_list(self):
        """Get list of text choices for image identification."""
        if self.text_choices:
            return [choice.strip() for choice in self.text_choices.split(',') if choice.strip()]
        return []


class GameOption(models.Model):
    """Options for image identification and multiple choice games."""
    
    question = models.ForeignKey(GameQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200, help_text="Option label/text")
    option_image = models.ImageField(upload_to='game_images/', blank=True, null=True, help_text="Image for this option")
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.question} - {self.option_text}"


class GameAttempt(models.Model):
    """Tracks student attempts at games."""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_attempts')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    time_taken = models.IntegerField(null=True, blank=True, help_text="Time in seconds")
    answers = models.TextField(help_text="JSON of user answers")
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.game.title} ({self.score}/{self.max_score})"
    
    def get_percentage(self):
        if self.max_score > 0:
            return round((self.score / self.max_score) * 100)
        return 0
