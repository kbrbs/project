"""
Test script to verify image identification game functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from games.models import Game, GameQuestion
from django.conf import settings

print("=" * 60)
print("IMAGE IDENTIFICATION GAME - FULL TEST")
print("=" * 60)

# Check media configuration
print("\n1. MEDIA CONFIGURATION:")
print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   Media directory exists: {os.path.exists(settings.MEDIA_ROOT)}")

# Check if game_images directory exists
game_images_path = os.path.join(settings.MEDIA_ROOT, 'game_images')
print(f"   game_images/ exists: {os.path.exists(game_images_path)}")
if os.path.exists(game_images_path):
    files = os.listdir(game_images_path)
    print(f"   Files in game_images/: {len(files)}")
    for f in files[:5]:  # Show first 5 files
        print(f"     - {f}")

# Check for image identification games
print("\n2. IMAGE IDENTIFICATION GAMES:")
img_games = Game.objects.filter(game_type='image_identification')
print(f"   Total games: {img_games.count()}")

for game in img_games:
    print(f"\n   Game: {game.title}")
    print(f"   - ID: {game.id}")
    print(f"   - Active: {game.is_active}")
    print(f"   - Questions: {game.questions.count()}")
    
    # Check each question
    for q in game.questions.all():
        print(f"\n     Question {q.order}: {q.question_text[:50]}...")
        print(f"     - ID: {q.id}")
        print(f"     - Has image: {bool(q.question_image)}")
        if q.question_image:
            print(f"     - Image path: {q.question_image.name}")
            print(f"     - Image URL: {q.question_image.url}")
            full_path = os.path.join(settings.MEDIA_ROOT, q.question_image.name)
            print(f"     - File exists: {os.path.exists(full_path)}")
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"     - File size: {size:,} bytes ({size/1024:.2f} KB)")
        print(f"     - Text choices: {q.text_choices[:80]}...")
        print(f"     - Correct answer: {q.correct_answer}")
        
        # Parse choices
        choices = q.get_text_choices_list()
        print(f"     - Number of choices: {len(choices)}")
        print(f"     - Choices: {choices}")
        
        # Verify correct answer is in choices
        if q.correct_answer:
            correct_in_choices = q.correct_answer.strip() in [c.strip() for c in choices]
            print(f"     - Correct answer in choices: {correct_in_choices}")
            if not correct_in_choices:
                print(f"       ⚠️ WARNING: Correct answer '{q.correct_answer}' not found in choices!")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

# Summary
print("\n3. SUMMARY:")
total_questions = GameQuestion.objects.filter(game__game_type='image_identification').count()
questions_with_images = GameQuestion.objects.filter(
    game__game_type='image_identification',
    question_image__isnull=False
).exclude(question_image='').count()

print(f"   - Total image identification questions: {total_questions}")
print(f"   - Questions with images: {questions_with_images}")
print(f"   - Questions missing images: {total_questions - questions_with_images}")

if questions_with_images > 0:
    print("\n✅ You have questions with images uploaded!")
    print("   Next steps:")
    print("   1. Start the Django development server")
    print("   2. Go to http://127.0.0.1:8000/games/")
    print("   3. Click on an Image Identification game")
    print("   4. Verify the image displays and choices work")
else:
    print("\n⚠️ No questions with images found!")
    print("   Steps to add images:")
    print("   1. Go to http://127.0.0.1:8000/admin-panel/games/")
    print("   2. Edit or create an Image Identification game")
    print("   3. Upload an image for the question_image field")
    print("   4. Add comma-separated text choices")
    print("   5. Set the correct answer (must match one choice exactly)")
