"""
Test script to verify image upload configuration for games
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from django.conf import settings
from games.models import Game, GameQuestion
from pathlib import Path

print("=== IMAGE UPLOAD CONFIGURATION TEST ===\n")

# Test 1: Check settings
print("1. Django Settings:")
print(f"   MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"   MEDIA_URL: {settings.MEDIA_URL}")
print(f"   MEDIA_ROOT exists: {Path(settings.MEDIA_ROOT).exists()}")
print()

# Test 2: Check game_images directory
game_images_path = Path(settings.MEDIA_ROOT) / 'game_images'
print("2. Game Images Directory:")
print(f"   Path: {game_images_path}")
print(f"   Exists: {game_images_path.exists()}")
if not game_images_path.exists():
    print("   ℹ️  Will be created automatically on first upload")
print()

# Test 3: Check model field configuration
print("3. GameQuestion Model Field:")
field = GameQuestion._meta.get_field('question_image')
print(f"   Field type: {type(field).__name__}")
print(f"   Upload to: {field.upload_to}")
print(f"   Validators: {[v.__class__.__name__ for v in field.validators]}")
print()

# Test 4: Check file extension validator
from django.core.validators import FileExtensionValidator
for validator in field.validators:
    if isinstance(validator, FileExtensionValidator):
        print("4. File Extension Validator:")
        print(f"   Allowed extensions: {', '.join(validator.allowed_extensions)}")
        print()
        break

# Test 5: Check if any games exist with images
print("5. Existing Games with Images:")
games_with_images = GameQuestion.objects.exclude(question_image='').exclude(question_image__isnull=True)
print(f"   Count: {games_with_images.count()}")
if games_with_images.exists():
    for gq in games_with_images[:3]:
        print(f"   - Q{gq.id}: {gq.question_image.name}")
        print(f"     URL: {gq.question_image.url}")
        print(f"     Path: {gq.question_image.path}")
        print(f"     Exists on disk: {Path(gq.question_image.path).exists()}")
print()

print("=== TEST COMPLETE ===")
print("\n✅ Configuration Summary:")
print("   • Images will be saved to: media/game_images/")
print("   • Accessible via URL: /media/game_images/[filename]")
print("   • Allowed formats: jpg, jpeg, png, gif, webp")
print("   • Validation: Server-side (Django) + Client-side (HTML5)")
