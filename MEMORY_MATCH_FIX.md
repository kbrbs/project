# Memory Match Game - Score & Attempt Tracking Fix

## Issues Found

### 1. **Frontend Not Tracking Per-Question Results**
The game was only tracking the last question's results and sending only that data to the server.

### 2. **Backend Calculation Error**
The backend was trying to call a non-existent method `get_memory_cards()` and couldn't properly calculate the score.

### 3. **Data Mismatch**
Frontend was sending `{matched_pairs, attempts, time}` but backend was expecting a different format for validation.

## Fixes Applied

### Frontend Changes (`games/templates/games/memory_match_game.html`)

#### 1. Added Result Tracking Variable
```javascript
let allQuestionResults = {}; // Track results for each question
```

#### 2. Initialize Tracking Per Question
```javascript
// Initialize result tracking for this question
allQuestionResults[q.id] = {
  matched_pairs: 0,
  attempts: 0,
  total_pairs: totalPairsForQuestion
};
```

#### 3. Update Tracking on Each Attempt
```javascript
// Update tracking for current question
const currentQuestion = gameData.questions[currentQuestionIndex];
if (allQuestionResults[currentQuestion.id]) {
  allQuestionResults[currentQuestion.id].attempts = attempts;
}
```

#### 4. Update Tracking on Successful Match
```javascript
// Update tracking for current question
const currentQuestion = gameData.questions[currentQuestionIndex];
if (allQuestionResults[currentQuestion.id]) {
  allQuestionResults[currentQuestion.id].matched_pairs = matchedPairs;
  allQuestionResults[currentQuestion.id].attempts = attempts;
}
```

#### 5. Send Complete Data to Server
```javascript
// Build answers object with all question results
const userAnswers = {};
for (const questionId in allQuestionResults) {
  userAnswers[questionId] = {
    matched_pairs: allQuestionResults[questionId].matched_pairs,
    attempts: allQuestionResults[questionId].attempts,
    total_pairs: allQuestionResults[questionId].total_pairs,
    time: timeTaken
  };
}
```

### Backend Changes (`games/views.py`)

#### Fixed Memory Match Scoring Logic
```python
elif game.game_type == 'memory_match':
    # For memory match, check if all pairs were matched
    # user_answer is a dict: {matched_pairs: X, attempts: Y, total_pairs: Z, time: T}
    if isinstance(user_answer, dict):
        matched_pairs = user_answer.get('matched_pairs', 0)
        total_pairs = user_answer.get('total_pairs', 0)
        
        # Award full points if all pairs matched
        if matched_pairs == total_pairs and total_pairs > 0:
            score += game.points_per_correct
        elif total_pairs > 0:
            # Award partial credit based on percentage
            score += int((matched_pairs / total_pairs) * game.points_per_correct)
```

## How It Works Now

### 1. **Game Initialization**
- When each question loads, it initializes tracking in `allQuestionResults[questionId]`
- Stores `matched_pairs: 0`, `attempts: 0`, `total_pairs: X`

### 2. **During Gameplay**
- Every time 2 cards are flipped, `attempts` is incremented and tracked
- Every time a match is found, `matched_pairs` is incremented and tracked
- Each question maintains its own independent statistics

### 3. **Score Calculation**
- **Frontend**: Adds points immediately when match is found (`score += gameData.points_per_correct`)
- **Backend**: Validates and recalculates based on submitted data
  - Full points if `matched_pairs == total_pairs`
  - Partial credit: `(matched_pairs / total_pairs) * points_per_correct`

### 4. **Game Submission**
When the game ends:
```javascript
{
  "answers": {
    "question_id_1": {
      "matched_pairs": 8,
      "attempts": 15,
      "total_pairs": 8,
      "time": 45
    },
    "question_id_2": {
      "matched_pairs": 6,
      "attempts": 12,
      "total_pairs": 6,
      "time": 45
    }
  },
  "time_taken": 45
}
```

### 5. **Database Storage**
```python
GameAttempt.objects.create(
    user=request.user,
    game=game,
    score=score,              # Calculated total score
    max_score=max_score,      # Maximum possible score
    time_taken=time_taken,    # Total time in seconds
    answers=json.dumps(answers),  # Full answer data
    completed=True
)
```

### 6. **Percentage Calculation**
```python
def get_percentage(self):
    if self.max_score > 0:
        return round((self.score / self.max_score) * 100)
    return 0
```

## Example Scenarios

### Scenario 1: Perfect Game
- Game has 1 question with 8 pairs
- Player matches all 8 pairs in 15 attempts
- **Score**: 10 points (full `points_per_correct`)
- **Percentage**: 100%

### Scenario 2: Partial Success
- Game has 1 question with 8 pairs
- Player matches 6 pairs in 12 attempts (game incomplete)
- **Score**: 7 points (`(6/8) * 10 = 7.5, rounded to 7`)
- **Percentage**: 70%

### Scenario 3: Multiple Questions
- Game has 2 questions, each with 6 pairs
- Question 1: 6/6 pairs matched → 10 points
- Question 2: 4/6 pairs matched → 6 points
- **Total Score**: 16 points
- **Max Score**: 20 points
- **Percentage**: 80%

## Testing

### Test the Fix
1. Go to memory match game
2. Play the game and match all pairs
3. Check the results page shows correct score
4. Go to your attempts history
5. Verify:
   - Score is correctly calculated
   - Percentage is accurate (score/max_score * 100)
   - Attempts and time are properly recorded

### Verify in Django Admin
```python
from games.models import GameAttempt
latest = GameAttempt.objects.latest('created_at')
print(f"Score: {latest.score}/{latest.max_score}")
print(f"Percentage: {latest.get_percentage()}%")
print(f"Time: {latest.time_taken}s")
print(f"Answers: {latest.answers}")
```

## Summary

✅ **Fixed**: Score calculation now properly accounts for all matched pairs  
✅ **Fixed**: Attempts are properly tracked and stored  
✅ **Fixed**: Percentage calculation is accurate  
✅ **Fixed**: Multi-question games properly track each question separately  
✅ **Improved**: Better error handling and data validation  
✅ **Improved**: Console logging for debugging  

The memory match game now correctly saves:
- ✅ Score (with partial credit support)
- ✅ Max score (based on number of questions × points_per_correct)
- ✅ Percentage (calculated correctly as score/max_score * 100)
- ✅ Attempts (total number of card flip pairs)
- ✅ Time taken (in seconds)
- ✅ Complete answer data (per question results)
