"""
Test script to verify drag-drop game editing works correctly
Simulates the edit flow: create, edit, verify
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from games.models import Game, GameQuestion

print("=== DRAG-DROP EDIT TEST ===\n")

# Step 1: Create a test game with a drag-drop question
print("STEP 1: Creating test game with drag-drop question")
test_game = Game.objects.create(
    title="Edit Test Game",
    game_type="drag_drop",
    description="Testing edit functionality",
    difficulty="easy",
    points_per_correct=10
)
print(f"✓ Created game: {test_game.title} (ID: {test_game.id})")

test_question = GameQuestion.objects.create(
    game=test_game,
    order=1,
    question_text="Original Question",
    sentence_template="Original * template with *",
    correct_answers="original, values",
    extra_choices="wrong, options"
)
print(f"✓ Created question (ID: {test_question.id})")
print(f"  sentence_template: '{test_question.sentence_template}'")
print(f"  correct_answers: '{test_question.correct_answers}'")
print(f"  extra_choices: '{test_question.extra_choices}'")

# Step 2: Simulate editing (fetch, modify, save)
print("\nSTEP 2: Simulating edit (fetch and modify)")
question_to_edit = GameQuestion.objects.get(id=test_question.id)
print(f"✓ Fetched question ID={question_to_edit.id}")

# Modify the fields
question_to_edit.sentence_template = "The city of * is famous for *"
question_to_edit.correct_answers = "Bustos, Minasa"
question_to_edit.extra_choices = "Manila, rice cake"
question_to_edit.save()
print(f"✓ Modified and saved question")

# Step 3: Verify the changes persisted
print("\nSTEP 3: Verifying changes persisted")
verified_question = GameQuestion.objects.get(id=test_question.id)
print(f"✓ Re-fetched question ID={verified_question.id}")
print(f"  sentence_template: '{verified_question.sentence_template}'")
print(f"  correct_answers: '{verified_question.correct_answers}'")
print(f"  extra_choices: '{verified_question.extra_choices}'")

# Check if values match
if (verified_question.sentence_template == "The city of * is famous for *" and
    verified_question.correct_answers == "Bustos, Minasa" and
    verified_question.extra_choices == "Manila, rice cake"):
    print("\n✅ SUCCESS: All fields updated correctly!")
else:
    print("\n❌ FAILURE: Fields did not update correctly!")
    print(f"Expected: 'The city of * is famous for *', 'Bustos, Minasa', 'Manila, rice cake'")
    print(f"Got: '{verified_question.sentence_template}', '{verified_question.correct_answers}', '{verified_question.extra_choices}'")

# Step 4: Test editing multiple times
print("\nSTEP 4: Testing multiple edits")
for i in range(3):
    q = GameQuestion.objects.get(id=test_question.id)
    q.sentence_template = f"Edit {i+1}: Test * and *"
    q.correct_answers = f"value{i+1}, option{i+1}"
    q.extra_choices = f"wrong{i+1}, bad{i+1}"
    q.save()
    
    verify = GameQuestion.objects.get(id=test_question.id)
    if verify.sentence_template == f"Edit {i+1}: Test * and *":
        print(f"  ✓ Edit {i+1} successful")
    else:
        print(f"  ✗ Edit {i+1} FAILED")

# Cleanup
print("\nCLEANUP: Deleting test game")
test_game.delete()
print("✓ Deleted test game and questions")

print("\n=== TEST COMPLETE ===")
print("If all steps passed, the model layer works correctly.")
print("If form edits still fail, the issue is in:")
print("  1. Form not binding to correct instance (missing ID field)")
print("  2. JavaScript hiding/disabling fields")
print("  3. Form validation errors")
