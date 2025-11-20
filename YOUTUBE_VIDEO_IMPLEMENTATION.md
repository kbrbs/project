# YouTube Video Embedding Feature

## Overview
This feature extends the educational content management system to support YouTube videos alongside images. Administrators can add YouTube videos with captions to educational sections, and these videos are displayed in the 3D book interface on lesson detail pages.

## Implementation Summary

### Database Model
**File:** `core/models.py`

Created `SectionVideo` model with the following fields:
- `section` (ForeignKey): Links to EducationalSection with related_name='content_videos'
- `youtube_url` (URLField): Stores YouTube video URL (max 500 characters)
- `caption` (CharField): Optional description/caption (max 255 characters)
- `order` (PositiveIntegerField): For ordering videos
- `created_at` (DateTimeField): Auto-generated timestamp

**Key Method:**
```python
def get_embed_url(self):
    """Converts various YouTube URL formats to embed URL"""
```

Supports three URL formats:
1. `https://www.youtube.com/watch?v=VIDEO_ID`
2. `https://youtu.be/VIDEO_ID`
3. `https://www.youtube.com/embed/VIDEO_ID`

### Admin Panel Integration
**File:** `core/admin_panel/views.py`

#### Changes:
1. **Import Added:**
   ```python
   from core.models import SectionVideo
   ```

2. **Formset Created:**
   ```python
   SectionVideoFormSet = inlineformset_factory(
       EducationalSection,
       SectionVideo,
       fields=('youtube_url', 'caption'),
       extra=0,
       can_delete=True,
       widgets={
           'youtube_url': forms.URLInput(attrs={'placeholder': '...'}),
           'caption': forms.TextInput(attrs={'placeholder': '...'})
       }
   )
   ```

3. **SectionCreateView Updates:**
   - `get()`: Added `video_formset = SectionVideoFormSet()`
   - `post()`: Added video formset validation and saving
   - Validation: `form.is_valid() and formset.is_valid() and video_formset.is_valid()`
   - Context: Passes `video_formset` to template

4. **SectionUpdateView Updates:**
   - `get()`: Added `video_formset = SectionVideoFormSet(instance=self.object)`
   - `post()`: Added video formset validation and saving with instance
   - Same validation logic as CreateView

### Frontend Template
**File:** `core/templates/core/admin_panel/section_form.html`

#### Content Videos Section:
- **Add Video Button:** Blue button with video icon
- **Video Formset Container:** `id="video-formset"`
- **Individual Video Forms:**
  - Video preview container with iframe
  - YouTube URL input field
  - Caption input field
  - Remove button
- **Empty Form Template:** `id="empty-video-form-template"`

#### JavaScript Functionality:
- `extractVideoId(url)`: Parses YouTube URLs to extract video ID
- `attachVideoPreview()`: Shows live iframe preview when URL is entered
- `updateLivePreviewVideos()`: Updates preview panel with embedded videos
- `addForm()`: Adds new video form
- `removeForm()`: Marks for deletion or removes form
- `updateFormNumbers()`: Renumbers forms after add/remove

#### Live Preview Panel:
- **Container:** `id="preview-videos-container"`
- **Grid:** `id="preview-videos"`
- Shows embedded YouTube videos with captions
- Hidden when no videos are added

### Lesson Display
**File:** `core/views.py`

#### lesson_detail() Updates:
```python
section_videos = section.content_videos.all().order_by('order', 'created_at')
```
Added to context as `section_videos`

**File:** `core/templates/core/lesson_detail.html`

#### Alpine.js Data Structure:
```javascript
const videos = [
  {
    embedUrl: "{{ video.get_embed_url }}",
    caption: "{{ video.caption|escapejs }}"
  }
];
```

#### Page Calculation:
```javascript
const videoSpreads = Math.ceil(videoCount / 2);
const calculatedTotalPages = 1 + imageSpreads + videoSpreads + 2;
```

#### Video Pages Rendering:
- **Left Pages:** Odd-indexed videos (0, 2, 4, ...)
  - Blue border styling (vs green for images)
  - Header: "🎥 Video Content" (shown on first video page)
  - Embedded iframe with full controls
  - Caption display in blue-themed box

- **Right Pages:** Even-indexed videos (1, 3, 5, ...)
  - Same styling and layout as left pages
  - Placeholder shown if odd number of videos

### Database Migration
**File:** `core/migrations/0011_sectionvideo.py`

Created migration with:
- CreateModel operation for SectionVideo
- All fields and foreign key relationship
- Meta options for ordering

**Applied:** Successfully migrated to database

## Usage Instructions

### For Administrators:

1. **Navigate to Admin Panel:**
   - Go to Educational Sections management
   - Create new section or edit existing section

2. **Add YouTube Videos:**
   - Scroll to "Content Videos" section
   - Click "Add Video" button
   - Paste YouTube URL (any format supported)
   - Add optional caption/description
   - See live preview in iframe

3. **Manage Videos:**
   - Add multiple videos using "Add Video"
   - Remove videos using "Remove" button
   - Videos appear in live preview panel
   - Save section to persist changes

4. **Supported URL Formats:**
   ```
   https://www.youtube.com/watch?v=dQw4w9WgXcQ
   https://youtu.be/dQw4w9WgXcQ
   https://www.youtube.com/embed/dQw4w9WgXcQ
   ```

### For Students:

1. **Viewing Videos:**
   - Videos appear in 3D book interface after image pages
   - Navigate using Next/Previous buttons or page numbers
   - Videos load with full YouTube controls
   - Captions displayed below video if provided

2. **Video Features:**
   - Full screen mode available
   - All YouTube playback controls
   - Responsive sizing (aspect-ratio maintained)
   - Caption text in italic font

## Technical Features

### URL Parsing
Three regex patterns handle different YouTube URL formats:
```python
patterns = [
    r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
    r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
    r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
]
```

### Formset Management
- **Dynamic Forms:** JavaScript clones empty form template
- **Index Management:** Automatically updates field names/IDs
- **Deletion:** Marks existing records for deletion, removes new forms
- **Validation:** Django validates both image and video formsets

### Live Preview
- **Real-time Updates:** URL input triggers iframe update
- **Video Extraction:** JavaScript extracts video ID client-side
- **Caption Updates:** Input listener updates preview captions
- **Container Management:** Shows/hides based on content

### Book Interface Integration
- **Page Calculation:** Dynamically calculates pages based on videos
- **Spread Layout:** 2 videos per spread (left/right pages)
- **Styling Consistency:** Blue theme for videos (vs green for images)
- **Navigation:** Seamless page transitions between content types

## Styling Details

### Video Forms (Admin):
- Border: `border-gray-200`
- Preview: `border-blue-200` (blue theme)
- Button: `bg-blue-600 hover:bg-blue-700`
- Caption box: `bg-blue-50 border-blue-200`

### Video Display (Lesson):
- Border: `border-4 border-blue-200`
- Title: "🎥 Video Content" with `border-b-4 border-blue-200`
- Caption: `bg-blue-50 px-6 py-4 rounded-xl border-2 border-blue-200`
- Iframe: `w-full aspect-video rounded-lg`

## File Structure

```
core/
├── models.py                          # SectionVideo model
├── admin_panel/
│   └── views.py                       # Formset and view updates
├── templates/
│   └── core/
│       ├── admin_panel/
│       │   └── section_form.html      # Admin form with video section
│       └── lesson_detail.html         # 3D book with video pages
├── views.py                           # Lesson detail with videos
└── migrations/
    └── 0011_sectionvideo.py           # Database migration

```

## Testing Checklist

- [x] Model created and migrated
- [x] Admin formset functional
- [x] URL parsing works for all formats
- [x] Live preview shows embedded videos
- [x] Add/remove video forms working
- [x] Form validation and saving
- [x] Lesson display shows videos
- [x] 3D book navigation with videos
- [x] Caption display working
- [x] Responsive iframe sizing

## Future Enhancements

### Potential Improvements:
1. **Video Ordering:** Drag-and-drop reordering
2. **Thumbnail Preview:** Show video thumbnail before embedding
3. **Playlist Support:** Support YouTube playlists
4. **Other Platforms:** Support Vimeo, Dailymotion, etc.
5. **Accessibility:** Add transcript support
6. **Analytics:** Track video views and completion
7. **Timestamp Links:** Link to specific video timestamps
8. **Download Option:** Allow downloading videos (if permitted)

## Related Features

- **Image Management:** Similar formset structure
- **PDF Resources:** Parallel content type
- **Quiz Integration:** Interactive learning elements
- **Activity Logging:** Track student engagement
- **3D Book Interface:** Unified display system

## Dependencies

- **Django 5.2.7:** Formsets, models, migrations
- **Alpine.js:** Live preview functionality
- **Tailwind CSS:** Styling framework
- **YouTube Embed API:** Video playback

## Notes

- Videos require internet connection to load
- YouTube embed policies apply (age restrictions, geo-blocking)
- Large numbers of videos may impact page load time
- Iframe allows full YouTube features (subtitles, speed, quality)
- Videos are not downloaded, only embedded from YouTube

## Support

For issues or questions:
1. Check YouTube URL format
2. Verify internet connection
3. Check browser console for errors
4. Ensure JavaScript is enabled
5. Test with different YouTube videos

---

**Last Updated:** November 20, 2025
**Version:** 1.0
**Status:** Production Ready ✅
