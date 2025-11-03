# Drag-and-Drop Fill-in-the-Blanks Game - Implementation Guide

## 🎯 Overview

The drag-and-drop game has been completely redesigned as a **fill-in-the-blanks** game where students drag words into blank spaces in sentences. This is much more intuitive and educational than the previous sorting format.

## ✨ Key Features

### For Admins:
- **Simple Input Format**: Use `*` or `_` to mark blanks in sentences
- **Automatic Choice Generation**: Correct answers automatically become draggable choices
- **Optional Wrong Answers**: Add extra choices to increase difficulty
- **No JSON Required**: Everything is comma-separated, easy to understand

### For Students:
- **Visual Sentence Display**: See the sentence with blank spaces
- **Drag-and-Drop Interface**: Drag words from a choice bank into blanks
- **Interactive Feedback**: Real-time visual feedback when dragging
- **Clear Instructions**: Intuitive UI that doesn't need explanation

## 🔧 How to Create a Drag-and-Drop Game

### Step 1: Navigate to Admin Panel
1. Go to http://127.0.0.1:8000/admin-panel/
2. Click on **Games** in the sidebar
3. Click **Add New Game**

### Step 2: Fill in Game Details
- **Title**: e.g., "Peter Piper Tongue Twisters"
- **Game Type**: Select **"Drag and Drop Sorting"**
- **Description**: e.g., "Complete the famous tongue twisters by dragging the correct words"
- **Difficulty**: Choose Easy/Medium/Hard
- **Time Limit**: Optional (leave blank for no time limit)
- **Points Per Correct**: Default is 10
- **Active**: Check this box to make it visible to students

### Step 3: Add Questions

When you select "Drag and Drop Sorting" as the game type, you'll see three fields:

#### Field 1: Sentence with Blanks
Enter your sentence and use `*` or `_` to mark where blanks should appear.

**Example 1:**
```
Peter * picked a * peckpeck
```
**Result:** Peter _____ picked a _____ peckpeck

**Example 2:**
```
Arrowroot is used to make _ flour
```
**Result:** Arrowroot is used to make _____ flour

**Example 3:**
```
The city of _ is famous for its _ product called Minasa
```
**Result:** The city of _____ is famous for its _____ product called Minasa

#### Field 2: Correct Answers (comma-separated)
Enter the correct words for each blank **in order**, separated by commas.

**For Example 1:**
```
piper, peck of
```

**For Example 2:**
```
Minasa
```

**For Example 3:**
```
Bustos, arrowroot-based
```

#### Field 3: Additional Choices (comma-separated, optional)
Add wrong answer options to make it more challenging. These will be shuffled together with the correct answers.

**For Example 1:**
```
pepper, pack, pick, peter
```

**For Example 2:**
```
rice, wheat, corn
```

**For Example 3:**
```
Manila, wheat-based, corn-based, Bataan
```

#### Field 4: Explanation (optional)
Provide educational context shown after the student answers.

**Example:**
```
"Peter Piper" is a famous English tongue twister. A peck is a unit of measurement equal to 8 quarts.
```

### Step 4: Save the Game
Click **Save Game** button. The form will stay on the same page so you can add more questions if needed.

## 📝 Complete Example Game

Here's a complete example you can copy and test:

### Game Details:
- **Title**: Filipino Culture Fill-in-the-Blanks
- **Game Type**: Drag and Drop Sorting
- **Description**: Test your knowledge of Filipino culture and traditions
- **Difficulty**: Medium
- **Points Per Correct**: 10
- **Active**: ✓ (checked)

### Question 1:
- **Question Text**: Complete the sentence about Minasa
- **Sentence with Blanks**: `The city of * is famous for its * made from arrowroot`
- **Correct Answers**: `Bustos, Minasa`
- **Additional Choices**: `Manila, rice cakes, Quezon, cassava`
- **Explanation**: Bustos, Bulacan is renowned for Minasa, a traditional Filipino delicacy made from arrowroot starch.

### Question 2:
- **Question Text**: Complete this sentence about arrowroot processing
- **Sentence with Blanks**: `After harvesting arrowroot, we * the roots, then * them into pulp`
- **Correct Answers**: `wash, grate`
- **Additional Choices**: `boil, slice, fry, bake`
- **Explanation**: The traditional process involves washing the roots thoroughly and then grating them to extract the starch.

### Question 3:
- **Question Text**: Identify the correct term
- **Sentence with Blanks**: `Arrowroot * is extracted from the grated pulp and dried to make flour`
- **Correct Answers**: `starch`
- **Additional Choices**: `fiber, juice, oil, powder`
- **Explanation**: Starch is the main component extracted from arrowroot roots, which is then processed into flour.

## 🎮 How Students Play

### Step 1: Browse Games
Students navigate to http://127.0.0.1:8000/games/ and see all active games.

### Step 2: Start the Game
Click on a drag-and-drop game to start playing.

### Step 3: Gameplay
1. **Read the Question**: See the instruction text at the top
2. **View the Sentence**: The sentence appears with blank spaces (shown as `_____`)
3. **View Choices**: All available words appear in a "choice bank" below the sentence
4. **Drag and Drop**: Drag words from the choice bank into the blank spaces
5. **Rearrange**: If needed, drag words back to the choice bank or to different blanks
6. **Submit**: Click "Check Answer" to see if they're correct

### Step 4: Feedback
- ✅ **Correct**: Green box with congratulations + explanation
- ❌ **Incorrect**: Red box showing the correct answer + explanation

### Step 5: Continue
After 4 seconds, the next question loads automatically. At the end, students see their final score and percentage.

## 🎨 UI/UX Features

### Visual Design:
- **Blank Spaces**: Dashed blue boxes with `______` placeholder
- **Draggable Choices**: Blue gradient pills with hover effects
- **Drop Zones**: Highlight when dragging over them
- **Filled Blanks**: Turn green when a word is placed
- **Smooth Animations**: All interactions are animated

### User-Friendly Elements:
- **Instructions Box**: Clear blue box explaining "drag and drop the words"
- **Progress Bar**: Shows current question number and score
- **Timer** (optional): Counts down if time limit is set
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🔍 Testing Checklist

### Admin Side:
- [ ] Navigate to http://127.0.0.1:8000/admin-panel/games/add/
- [ ] Select "Drag and Drop Sorting" game type
- [ ] Verify the three drag-drop fields appear (sentence, correct answers, extra choices)
- [ ] Create a test game with 2-3 questions using the example above
- [ ] Save successfully
- [ ] Edit the game and verify fields are populated correctly

### User Side:
- [ ] Go to http://127.0.0.1:8000/games/
- [ ] Find your test game in the list
- [ ] Click to start playing
- [ ] Verify sentence displays with blank spaces
- [ ] Verify all choices (correct + extra) appear shuffled below
- [ ] Drag a choice into a blank - verify it fits properly
- [ ] Drag a choice back to the choice bank - verify it works
- [ ] Try dragging a second choice into an already-filled blank - verify it swaps/replaces
- [ ] Submit with correct answers - verify green success message
- [ ] Play another question with wrong answers - verify red error message with correct answer shown
- [ ] Complete all questions - verify final score screen appears
- [ ] Check http://127.0.0.1:8000/games/my-attempts/ - verify the attempt was saved

## 🐛 Common Issues & Solutions

### Issue 1: Fields not showing
**Solution**: Make sure you selected "Drag and Drop Sorting" as the game type. The fields are dynamically shown/hidden based on this selection.

### Issue 2: Blanks not appearing in sentence
**Solution**: Make sure you're using `*` or `_` (underscore) to mark blanks, not other characters.

### Issue 3: Too many/few choices
**Solution**: Count your blanks carefully. You should have exactly as many correct answers (comma-separated) as there are `*` or `_` symbols in your sentence.

### Issue 4: Scoring not working
**Solution**: Make sure your correct answers are in the exact order they appear in the sentence (left to right).

## 📊 Database Changes

### New Fields Added to `GameQuestion` Model:
- `sentence_template` (TextField): Sentence with `*` or `_` for blanks
- `correct_answers` (TextField): Comma-separated correct answers
- `extra_choices` (TextField): Comma-separated additional wrong choices
- `correct_sequence` (TextField): Legacy field kept for backward compatibility

### Migration Applied:
- `games/migrations/0002_gamequestion_correct_answers_and_more.py`

## 🚀 Next Steps

1. **Test the implementation** using the example above
2. **Create educational content** relevant to your Minasa/Arrowroot curriculum
3. **Get student feedback** on the drag-and-drop interface
4. **Add more questions** to make comprehensive games
5. **Monitor attempts** via the admin stats dashboard

## 💡 Tips for Great Drag-Drop Games

1. **Keep sentences concise** - 1-2 blanks per sentence is ideal
2. **Make blanks meaningful** - Test important vocabulary or concepts
3. **Choose good distractors** - Extra choices should be plausible but wrong
4. **Provide explanations** - Help students learn from mistakes
5. **Vary difficulty** - Start easy, get progressively harder
6. **Test yourself first** - Always play through before assigning to students

---

**Server Status**: ✅ Running at http://127.0.0.1:8000/

**Ready to test!** Navigate to the admin panel and create your first drag-and-drop game.
