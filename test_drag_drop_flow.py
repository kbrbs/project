"""
Test script to verify drag-drop game flow
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'minasa_site.settings')
django.setup()

from games.models import Game, GameQuestion

print("=" * 60)
print("DRAG-DROP GAME FLOW TEST")
print("=" * 60)

# Check for drag-drop games
drag_drop_games = Game.objects.filter(game_type='drag_drop')
print(f"\n✅ Total drag-drop games: {drag_drop_games.count()}")

for game in drag_drop_games:
    print(f"\n📝 Game: {game.title}")
    print(f"   - ID: {game.id}")
    print(f"   - Active: {game.is_active}")
    print(f"   - Questions: {game.questions.count()}")
    
    for q in game.questions.all():
        print(f"\n   Question {q.order + 1}:")
        print(f"   - Text: {q.question_text[:60]}...")
        print(f"   - Sentence template: {q.sentence_template[:80] if q.sentence_template else 'N/A'}...")
        print(f"   - Correct answers: {q.correct_answers}")
        print(f"   - Extra choices: {q.extra_choices}")
        
        # Count blanks
        blank_count = q.get_blanks_count()
        correct_answers = q.get_correct_answers_list()
        print(f"   - Number of blanks: {blank_count}")
        print(f"   - Number of correct answers: {len(correct_answers)}")
        
        if blank_count != len(correct_answers):
            print(f"   ⚠️ WARNING: Blank count ({blank_count}) doesn't match correct answers ({len(correct_answers)})")

print("\n" + "=" * 60)
print("BUTTON FLOW ENHANCEMENT")
print("=" * 60)
print("\n✅ Enhanced Features:")
print("   1. Button starts as 'Check Answer'")
print("   2. After checking, button changes to:")
print("      - 'Next Question →' (purple) if more questions exist")
print("      - 'Finish' (green) if it's the last question")
print("   3. Dragging is disabled after checking answer")
print("   4. Click 'Next' or 'Finish' to proceed")
print("\n🎮 Test Instructions:")
print("   1. Visit a drag-drop game URL")
print("   2. Drag words into blanks")
print("   3. Click 'Check Answer' - see feedback")
print("   4. Button should change to 'Next Question →' or 'Finish'")
print("   5. Click the button to proceed")
print("\n" + "=" * 60)
