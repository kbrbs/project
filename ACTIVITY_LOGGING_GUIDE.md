# Activity Logging System Documentation

## Overview
A comprehensive activity logging system has been implemented to track all user activities across the application. Activities are categorized and can be viewed in the user's profile or admin panel.

## Categories

### 1. **Security** (`security`)
Tracks authentication and account security events:
- `login` - User successfully logged in
- `logout` - User logged out
- `password_change` - User changed their password
- `failed_login` - Failed login attempt
- `avatar_upload` - Profile picture uploaded

### 2. **Progress** (`progress`)
Tracks learning progress and content consumption:
- `lesson_started` - User started a lesson
- `lesson_completed` - User completed a lesson
- `lesson_viewed` - User viewed lesson content

### 3. **Quiz** (`quiz`)
Tracks quiz-related activities:
- `quiz_started` - User started a quiz
- `quiz_completed` - User completed a quiz
- `quiz_passed` - User passed a quiz (≥60%)
- `quiz_failed` - User failed a quiz (<60%)

### 4. **Game** (`game`)
Tracks game activities:
- `game_started` - User started a game
- `game_completed` - User completed a game
- `game_score` - Game score recorded

### 5. **Profile** (`profile`)
Tracks profile-related changes:
- `profile_update` - User updated their profile information
- `avatar_upload` - User uploaded a new avatar

### 6. **Content** (`content`)
Tracks general content viewing:
- `content_viewed` - User viewed content
- `video_watched` - User watched a video
- `festival_tour` - User visited the Festival Tour

### 7. **Download** (`download`)
Tracks file downloads:
- `file_downloaded` - User downloaded a file
- `pdf_downloaded` - User downloaded a PDF

### 8. **System** (`system`)
Tracks system-level events:
- `account_created` - New account was created
- `account_blocked` - Account was blocked
- `account_unblocked` - Account was unblocked

## Database Schema

### ActivityLog Model
```python
class ActivityLog(models.Model):
    user = ForeignKey(User)  # Who performed the action
    category = CharField  # One of the categories above
    action = CharField  # Specific action taken
    description = TextField  # Human-readable description
    
    # Optional references
    article = ForeignKey(Article, null=True)
    quiz_id = IntegerField(null=True)
    game_id = IntegerField(null=True)
    media = ForeignKey(MediaAsset, null=True)
    
    # Metadata
    ip_address = CharField  # User's IP address
    user_agent = CharField  # User's browser/device info
    metadata = JSONField  # Additional data (scores, changes, etc.)
    
    created_at = DateTimeField  # When the activity occurred
```

## Usage

### Logging an Activity

```python
from core.utils import log_activity

# Simple activity log
log_activity(
    user=request.user,
    category='security',
    action='login',
    description='User logged in successfully',
    request=request
)

# Activity with related object
log_activity(
    user=request.user,
    category='progress',
    action='lesson_viewed',
    description=f'Viewed lesson: {article.title}',
    request=request,
    article=article
)

# Activity with metadata
log_activity(
    user=request.user,
    category='quiz',
    action='quiz_passed',
    description=f'Completed quiz: {quiz.title} - Score: 85%',
    request=request,
    quiz_id=quiz.id,
    metadata={
        'score_percentage': 85,
        'correct_count': 17,
        'total_questions': 20
    }
)
```

### Viewing Activity Logs

#### User Profile
Recent activities are automatically displayed in the user's profile page under "Recent Activity" section.

#### Admin Panel
1. Go to Django Admin: `/admin/`
2. Navigate to "Activity logs" under Core section
3. Filter by:
   - Category
   - Action
   - Date
   - User
4. Search by username, description, or IP address

#### Querying in Code
```python
from core.models import ActivityLog

# Get all activities for a user
user_activities = ActivityLog.objects.filter(user=user)

# Get security-related activities
security_logs = ActivityLog.objects.filter(category='security')

# Get quiz activities for a user
quiz_activities = ActivityLog.objects.filter(
    user=user,
    category='quiz'
).order_by('-created_at')

# Get activities from the last 7 days
from datetime import timedelta
from django.utils import timezone

recent = ActivityLog.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=7)
)
```

## Currently Logged Activities

### ✅ Implemented
- User login/logout
- Failed login attempts
- Password changes
- Profile updates (name, grade, birthday)
- Avatar uploads
- Lesson viewing
- Quiz start/completion/pass/fail
- Game start/completion
- Festival tour visits
- Account creation

### 🔄 Ready to Add
To log additional activities, simply call `log_activity()` in the appropriate view:

```python
# Example: Log file download
from core.utils import log_activity

def download_file(request, file_id):
    file = get_object_or_404(MediaAsset, id=file_id)
    
    log_activity(
        user=request.user,
        category='download',
        action='file_downloaded',
        description=f'Downloaded: {file.title}',
        request=request,
        media=file
    )
    
    # ... rest of download logic
```

## Benefits

1. **Security Monitoring**: Track login attempts and suspicious activities
2. **User Engagement**: Understand how users interact with content
3. **Progress Tracking**: Monitor learning progress and completion rates
4. **Audit Trail**: Complete history of all user actions
5. **Analytics**: Generate reports on user behavior
6. **Compliance**: Meet data tracking requirements

## Performance Considerations

- Activities are indexed by user, category, and date for fast queries
- Old logs can be archived or deleted to maintain performance
- Consider setting up a cleanup task for logs older than X months

## Privacy & GDPR

- Activity logs contain personal data and IP addresses
- Implement data retention policies
- Provide users ability to request their activity data
- Allow users to request deletion of their activity history (if required by law)

## Future Enhancements

1. **Activity Dashboard**: Create visual analytics dashboard
2. **Export Functionality**: Allow users to export their activity history
3. **Real-time Notifications**: Notify admins of suspicious activities
4. **Activity Filtering**: Advanced filtering in profile page
5. **Activity Search**: Full-text search across activity descriptions
