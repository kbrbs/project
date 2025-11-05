"""
Test script to verify drag-drop fields can be saved to GameQuestion model
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from games.models import Game, GameQuestion

# Test 1: Check if fields exist in model
print("=== TEST 1: Model Field Check ===")
game_question_fields = [f.name for f in GameQuestion._meta.get_fields()]
required_fields = ['sentence_template', 'correct_answers', 'extra_choices']

for field in required_fields:
    if field in game_question_fields:
        print(f"✓ Field '{field}' exists in GameQuestion model")
    else:
        print(f"✗ Field '{field}' MISSING from GameQuestion model")

# Test 2: Try to create and save a test game with drag-drop question
print("\n=== TEST 2: Create and Save Test ===")
try:
    # Create a test game
    test_game = Game.objects.create(
        title="Test Drag-Drop Game",
        game_type="drag_drop",
        description="Testing drag-drop field save",
        difficulty="easy",
        points_per_correct=10
    )
    print(f"✓ Created test game: {test_game.title} (ID: {test_game.id})")
    
    # Create a test question with drag-drop fields
    test_question = GameQuestion.objects.create(
        game=test_game,
        order=1,
        question_text="Test Question",
        sentence_template="The city of * is famous for *",
        correct_answers="Bustos, Minasa",
        extra_choices="Manila, rice cake"
    )
    print(f"✓ Created test question (ID: {test_question.id})")
    print(f"  sentence_template: '{test_question.sentence_template}'")
    print(f"  correct_answers: '{test_question.correct_answers}'")
    print(f"  extra_choices: '{test_question.extra_choices}'")
    
    # Verify by re-fetching from database
    saved_question = GameQuestion.objects.get(id=test_question.id)
    print(f"\n✓ Re-fetched from database:")
    print(f"  sentence_template: '{saved_question.sentence_template}'")
    print(f"  correct_answers: '{saved_question.correct_answers}'")
    print(f"  extra_choices: '{saved_question.extra_choices}'")
    
    # Test 3: Update the question
    print("\n=== TEST 3: Update Test ===")
    saved_question.sentence_template = "Updated: The * is in *"
    saved_question.correct_answers = "Updated, Values"
    saved_question.extra_choices = "Wrong, Options"
    saved_question.save()
    print("✓ Updated question fields")
    
    # Re-fetch to verify update
    updated_question = GameQuestion.objects.get(id=test_question.id)
    print(f"✓ Re-fetched after update:")
    print(f"  sentence_template: '{updated_question.sentence_template}'")
    print(f"  correct_answers: '{updated_question.correct_answers}'")
    print(f"  extra_choices: '{updated_question.extra_choices}'")
    
    # Cleanup
    print("\n=== CLEANUP ===")
    test_game.delete()
    print("✓ Deleted test game and questions")
    
    print("\n=== ALL TESTS PASSED ✓ ===")
    print("The model can save and retrieve drag-drop fields correctly.")
    print("If form save is failing, the issue is in the form/view logic, not the model.")
    
except Exception as e:
    print(f"\n✗ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
