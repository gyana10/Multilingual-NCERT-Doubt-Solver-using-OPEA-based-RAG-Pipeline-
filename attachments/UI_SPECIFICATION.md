# UI/UX Specification - NCERT Doubt-Solver

## Design Overview

### Design Philosophy
- **Student-Centric**: Clean, distraction-free interface
- **Accessible**: Works for all ages and abilities
- **Responsive**: Seamless across devices
- **Modern**: Contemporary design patterns
- **Fast**: Optimized for performance

---

## Color Palette

### Primary Colors
```css
--primary-color: #4f46e5      /* Indigo 600 */
--primary-dark: #4338ca       /* Indigo 700 */
--secondary-color: #10b981    /* Green 500 */
--danger-color: #ef4444       /* Red 500 */
--warning-color: #f59e0b      /* Amber 500 */
```

### Neutral Colors
```css
--text-primary: #1f2937       /* Gray 800 */
--text-secondary: #6b7280     /* Gray 500 */
--bg-primary: #ffffff         /* White */
--bg-secondary: #f9fafb       /* Gray 50 */
--bg-tertiary: #f3f4f6        /* Gray 100 */
--border-color: #e5e7eb       /* Gray 200 */
```

### Gradients
```css
/* Header/Hero */
linear-gradient(135deg, #4f46e5, #4338ca)

/* Welcome Screen */
linear-gradient(135deg, #667eea 0%, #764ba2 100%)

/* User Message */
linear-gradient(135deg, #667eea, #764ba2)
```

---

## Typography

### Font Family
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Roboto, 'Helvetica Neue', Arial, sans-serif;
```

### Font Sizes
- **Hero Title**: 2.5rem (40px)
- **Page Title**: 1.5rem (24px)
- **Section Header**: 1.25rem (20px)
- **Body Text**: 1rem (16px)
- **Small Text**: 0.875rem (14px)
- **Tiny Text**: 0.75rem (12px)

### Font Weights
- **Bold**: 700 (headings)
- **Semi-bold**: 600 (labels)
- **Regular**: 400 (body text)

---

## Layout Structure

### Desktop Layout (> 968px)
```
┌─────────────────────────────────────────────────┐
│                    Header                        │
├──────────┬──────────────────────────────────────┤
│          │                                       │
│  Sidebar │         Chat Area                    │
│  (320px) │                                       │
│          │  ┌────────────────────────────────┐  │
│          │  │  Welcome/Messages              │  │
│          │  │                                │  │
│          │  │                                │  │
│          │  └────────────────────────────────┘  │
│          │  ┌────────────────────────────────┐  │
│          │  │  Input Area                    │  │
│          │  └────────────────────────────────┘  │
└──────────┴──────────────────────────────────────┘
```

### Mobile Layout (< 968px)
```
┌─────────────────────────┐
│       Header            │
├─────────────────────────┤
│                         │
│     Chat Area           │
│     (Full Width)        │
│                         │
│  ┌───────────────────┐  │
│  │  Messages         │  │
│  │                   │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │  Input Area       │  │
│  └───────────────────┘  │
└─────────────────────────┘

Sidebar: Slides in from left (overlay)
```

---

## Component Specifications

### 1. Header

**Dimensions:**
- Height: 72px
- Padding: 1rem (16px) vertical

**Elements:**
- Logo with graduation cap icon
- App name: "NCERT Doubt-Solver"
- Settings button
- History button

**Mobile Changes:**
- Logo text size reduced
- Button text hidden (icons only)

---

### 2. Sidebar

**Desktop:**
- Width: 320px
- Position: Fixed left
- Background: White
- Border: 1px right

**Mobile:**
- Position: Fixed overlay
- Transform: translateX(-100%) when hidden
- Box shadow when visible
- Close button appears

**Content:**
1. Grade selector (dropdown)
2. Subject selector (dropdown)
3. Language selector (dropdown)
4. New Conversation button

---

### 3. Welcome Screen

**Layout:**
- Centered content
- Max-width: 900px
- Gradient background

**Elements:**
1. Animated robot icon (5rem)
2. Welcome heading (2.5rem)
3. Subtitle text
4. 4 feature cards (grid)
5. CTA button

**Feature Cards:**
- Grid: 2x2 (desktop), 1 column (mobile)
- Background: rgba(255, 255, 255, 0.1)
- Border: 1px rgba(255, 255, 255, 0.2)
- Padding: 1.5rem
- Border-radius: 1rem
- Hover: translateY(-5px)

---

### 4. Chat Messages

**Container:**
- Padding: 2rem (desktop), 1rem (mobile)
- Flex column with gap: 1.5rem
- Auto-scroll to bottom

**User Message:**
- Align: Right
- Background: Purple gradient
- Color: White
- Max-width: 70%
- Border-radius: 1rem

**Assistant Message:**
- Align: Left
- Background: White
- Color: Dark gray
- Max-width: 70%
- Border-radius: 1rem

**Message Structure:**
```
┌─────┬────────────────────────────┐
│ 👤  │  Message Bubble            │
│     │  ┌──────────────────────┐  │
│     │  │  Message Text        │  │
│     │  │  [Image if present]  │  │
│     │  └──────────────────────┘  │
│     │  [Citations box]           │
│     │  Time | Confidence         │
│     │  [Copy] [Rate]             │
└─────┴────────────────────────────┘
```

---

### 5. Citations Box

**Style:**
- Background: Light gray (#f3f4f6)
- Border-left: 3px solid primary color
- Padding: 1rem
- Border-radius: 0.5rem
- Margin-top: 1rem

**Citation Item:**
- Background: White
- Padding: 0.75rem
- Border-radius: 0.5rem
- Source: Bold, primary color
- Text: Italic, gray

---

### 6. Input Area

**Container:**
- Background: White
- Border-top: 1px solid gray
- Padding: 1.5rem
- Sticky bottom

**Input Wrapper:**
- Display: Flex
- Background: Light gray
- Border: 2px solid gray
- Border-radius: 1rem
- Padding: 0.75rem

**Elements (left to right):**
1. Image upload button (icon)
2. Textarea (flexible)
3. Voice input button (icon)
4. Send button (circle)

**Textarea:**
- Auto-resize
- Max-height: 150px
- Font-size: 16px (prevents iOS zoom)
- No border
- Placeholder text

**Send Button:**
- Size: 44x44px
- Border-radius: 50%
- Background: Primary color
- Disabled state: Gray

---

### 7. Image Preview

**Position:** Above input wrapper
**Style:**
- Display: inline-block
- Max-width: 200px
- Max-height: 200px
- Border: 2px solid gray
- Border-radius: 0.5rem

**Remove Button:**
- Position: Absolute (top-right)
- Size: 24x24px
- Border-radius: 50%
- Background: Red
- Color: White

---

### 8. Feedback Modal

**Overlay:**
- Background: rgba(0, 0, 0, 0.5)
- Fixed position (full screen)
- Z-index: 2000

**Modal Box:**
- Max-width: 500px
- Background: White
- Border-radius: 1rem
- Box-shadow: Large

**Structure:**
```
┌─────────────────────────────┐
│ Rate this Answer      [×]   │  ← Header
├─────────────────────────────┤
│                             │
│    ⭐ ⭐ ⭐ ⭐ ⭐            │  ← Star Rating
│                             │
│  ┌─────────────────────┐   │
│  │ Comment textarea    │   │  ← Comment
│  └─────────────────────┘   │
├─────────────────────────────┤
│        [Cancel] [Submit]    │  ← Footer
└─────────────────────────────┘
```

**Star Rating:**
- Size: 2rem
- Hover: Yellow color
- Active: Yellow filled

---

### 9. Loading Overlay

**Style:**
- Fixed full screen
- Background: rgba(0, 0, 0, 0.5)
- Z-index: 2000
- Centered content

**Spinner:**
- Background: White
- Padding: 2rem 3rem
- Border-radius: 1rem
- Icon: 3rem, spinning
- Text: "Processing..."

---

## Interactions & Animations

### Hover Effects

**Buttons:**
```css
transition: all 0.3s ease;
hover: {
  transform: translateY(-2px);
  box-shadow: medium;
}
```

**Feature Cards:**
```css
transition: all 0.3s ease;
hover: {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
}
```

### Click Effects

**Send Button:**
- Scale: 1.05 on hover
- Disabled opacity: 0.5

**Rating Stars:**
- Color change on click
- Fill animation

### Animations

**Message Appear:**
```css
@keyframes messageSlide {
  from: {
    opacity: 0;
    transform: translateY(20px);
  }
  to: {
    opacity: 1;
    transform: translateY(0);
  }
}
duration: 0.3s
```

**Modal Appear:**
```css
@keyframes modalSlide {
  from: {
    opacity: 0;
    transform: translateY(-50px);
  }
  to: {
    opacity: 1;
    transform: translateY(0);
  }
}
duration: 0.3s
```

**Welcome Icon Float:**
```css
@keyframes float {
  0%, 100%: translateY(0);
  50%: translateY(-20px);
}
duration: 3s infinite
```

---

## Responsive Breakpoints

### Large Desktop (> 1400px)
- Max container width: 1400px
- Full features visible

### Desktop (968px - 1400px)
- Sidebar visible
- Full layout

### Tablet (640px - 968px)
- Sidebar collapsible
- Message max-width: 85%
- Touch-friendly targets

### Mobile (< 640px)
- Sidebar overlay
- Message max-width: 100%
- Reduced font sizes
- Compact spacing
- Single column layout

### Small Mobile (< 480px)
- Further reduced spacing
- Smaller feature cards
- Mobile-optimized buttons

---

## Accessibility Features

### Keyboard Navigation
- Tab order: Logical flow
- Focus indicators: Visible outline
- Enter to submit
- Escape to close modals

### Screen Reader Support
- ARIA labels on buttons
- Alt text for images
- Semantic HTML
- Proper heading hierarchy

### Touch Targets
- Minimum size: 44x44px
- Adequate spacing: 8px minimum
- No tiny clickable areas

### Color Contrast
- Text: Minimum 4.5:1 ratio
- Interactive elements: 3:1 ratio
- High contrast mode compatible

---

## Icons (Font Awesome 6.4.0)

### Used Icons:
- `fa-graduation-cap` - Logo
- `fa-cog` - Settings
- `fa-history` - History
- `fa-robot` - AI Assistant
- `fa-user` - Student
- `fa-image` - Image upload
- `fa-microphone` - Voice input
- `fa-paper-plane` - Send
- `fa-copy` - Copy
- `fa-star` - Rating
- `fa-quote-right` - Citations
- `fa-times` - Close
- `fa-circle-notch fa-spin` - Loading
- `fa-comments` - Multilingual
- `fa-book-open` - NCERT
- `fa-sliders-h` - Preferences
- `fa-user-graduate` - Grade
- `fa-book` - Subject
- `fa-language` - Language
- `fa-plus` - New
- `fa-comment-dots` - Start chat

---

## State Management

### Button States

**Send Button:**
- Enabled: Primary color, pointer cursor
- Disabled: Gray, not-allowed cursor
- Hover: Darker shade, scale up
- Active: Pressed effect

**Action Buttons:**
- Default: Gray border
- Hover: Primary color border
- Active: Primary background
- Focus: Outline visible

### Input States

**Textarea:**
- Default: Gray border
- Focus: Primary border + shadow
- Error: Red border
- Disabled: Light gray background

**Dropdowns:**
- Default: Gray border
- Focus: Primary border + shadow
- Hover: Light gray background

### Modal States

**Feedback Modal:**
- Hidden: display: none
- Visible: Fade in animation
- Closing: Fade out animation

### Loading States

**Overlay:**
- Hidden: display: none
- Active: Fade in, spinner rotating
- Completing: Fade out

---

## Performance Optimizations

### CSS
- Single stylesheet (styles.css)
- Mobile styles in separate file
- Minimal repaints
- Hardware acceleration for animations
- Efficient selectors

### JavaScript
- Event delegation
- Debounced input handlers
- Lazy loading images
- Efficient DOM updates
- No memory leaks

### Images
- Optimized sizes
- Lazy loading
- WebP format support
- Responsive images

### Fonts
- System fonts (no web fonts)
- Fallback chain
- Font-display: swap

---

## Browser Compatibility

### Supported Browsers
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Graceful Degradation
- Voice input: Feature detection
- Service Worker: Progressive enhancement
- CSS Grid: Fallback to flexbox
- Modern CSS: Vendor prefixes where needed

---

## Mobile-Specific Features

### PWA Capabilities
- Installable
- Offline structure
- App manifest
- Service worker
- Add to home screen

### Touch Gestures
- Tap to interact
- Swipe to dismiss sidebar
- Pull to refresh (future)
- Long press for context (future)

### Mobile Optimizations
- Prevent zoom on input
- Safe area insets (iOS)
- Bottom navigation consideration
- Landscape mode support

---

## Design Tokens

### Spacing Scale
```css
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
```

### Border Radius
```css
--radius-sm: 0.25rem;  /* 4px */
--radius-md: 0.5rem;   /* 8px */
--radius-lg: 1rem;     /* 16px */
--radius-full: 9999px; /* Circle */
```

### Shadows
```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
--shadow-xl: 0 20px 25px rgba(0,0,0,0.1);
```

---

## Future Enhancements

### Planned Features
- Dark mode toggle
- Custom themes
- Emoji reactions
- Bookmark answers
- Share functionality
- Print answers
- Export conversations
- Voice output (TTS)
- Rich text editor
- Code syntax highlighting
- Math equation rendering
- Diagrams/charts display

### UX Improvements
- Onboarding tour
- Contextual help
- Keyboard shortcuts guide
- User preferences saving
- Recently asked questions
- Popular questions
- Search history
- Auto-suggestions

---

## Component Library Ready

All components are modular and reusable:
- Button variants
- Input types
- Modal patterns
- Card layouts
- List items
- Avatar styles
- Badge components
- Alert messages

**Ready for**: React, Vue, or Web Components conversion

---

## Conclusion

This UI specification provides a complete design system for the NCERT Doubt-Solver application. All components are production-ready, accessible, and optimized for performance across devices.

**Design Goals Achieved:**
✅ Student-friendly interface
✅ Mobile-first responsive design
✅ Accessible to all users
✅ Modern and professional appearance
✅ Fast and performant
✅ Consistent design language
✅ Extensible component system
