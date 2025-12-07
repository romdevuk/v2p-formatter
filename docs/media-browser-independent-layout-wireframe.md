# Media Browser Independent Layout - Text Wireframe

## Current Layout (Before)
```
┌─────────────────────────────────────────────────────────────────┐
│ Navigation Tabs                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Top Controls Bar (Subfolder Select, Text Size, Load Draft)    │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────┬──────────────────────────────────────┐ │
│ │                      │                                      │ │
│ │  Media Browser       │   Live Preview                      │ │
│ │  (50% width)         │   (50% width)                       │ │
│ │                      │                                      │ │
│ │  ┌────────────────┐  │   ┌──────────────────────────────┐  │ │
│ │  │ visit2 (30) ▼  │  │   │ Document Preview Content     │  │ │
│ │  ├────────────────┤  │   │                              │  │ │
│ │  │ [media cards]  │  │   │ [Preview of text/media]      │  │ │
│ │  │                │  │   │                              │  │ │
│ │  │ [media cards]  │  │   │                              │  │ │
│ │  │                │  │   │                              │  │ │
│ │  └────────────────┘  │   │                              │  │ │
│ │                      │   └──────────────────────────────┘  │ │
│ │                      │                                      │ │
│ │  (Height matches     │   ┌──────────────────────────────┐  │ │
│ │   Live Preview)      │   │ Text Editor                  │  │ │
│ │                      │   │                              │  │ │
│ │                      │   │ [Editable text area]         │  │ │
│ │                      │   │                              │  │ │
│ │                      │   │                              │  │ │
│ │                      │   └──────────────────────────────┘  │ │
│ │                      │                                      │ │
│ └──────────────────────┴──────────────────────────────────────┘ │
│                                                                  │
│ Bottom Actions Bar (Save Draft, Preview Draft, Export DOCX)    │
└─────────────────────────────────────────────────────────────────┘

Problem: Media Browser height is constrained by Live Preview + Text Editor height
```

## Proposed Layout (After)
```
┌─────────────────────────────────────────────────────────────────┐
│ Navigation Tabs                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Top Controls Bar (Subfolder Select, Text Size, Load Draft)    │
├─────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────┬──────────────────────────────────────┐ │
│ │                      │                                      │ │
│ │  Media Browser       │   Live Preview                      │ │
│ │  (50% width)         │   (50% width)                       │ │
│ │                      │                                      │ │
│ │  ┌────────────────┐  │   ┌──────────────────────────────┐  │ │
│ │  │ Settings/Expand│  │   │ Document Preview Content     │  │ │
│ │  │ [0 files]      │  │   │                              │  │ │
│ │  ├────────────────┤  │   │ [Preview of text/media]      │  │ │
│ │  │                │  │   │                              │  │ │
│ │  │ visit2 (30) ▼  │  │   │                              │  │ │
│ │  │ visit2/post ▼  │  │   │                              │  │ │
│ │  │ visit2/tasks ▼ │  │   │                              │  │ │
│ │  │                │  │   │                              │  │ │
│ │  │ [media cards]  │  │   │                              │  │ │
│ │  │ [media cards]  │  │   └──────────────────────────────┘  │ │
│ │  │ [media cards]  │  │                                      │ │
│ │  │ [media cards]  │  │   ┌──────────────────────────────┐  │ │
│ │  │                │  │   │ Text Editor                  │  │ │
│ │  │ [scrollable]   │  │   │                              │  │ │
│ │  │                │  │   │ [Editable text area]         │  │ │
│ │  │ [media cards]  │  │   │                              │  │ │
│ │  │                │  │   │                              │  │ │
│ │  │ [media cards]  │  │   │                              │  │ │
│ │  │                │  │   │                              │  │ │
│ │  │ [media cards]  │  │   │                              │  │ │
│ │  │                │  │   │                              │  │ │
│ │  │ [media cards]  │  │   │                              │  │ │
│ │  │                │  │   │                              │  │ │
│ │  └────────────────┘  │   └──────────────────────────────┘  │ │
│ │                      │                                      │ │
│ │  (Independent        │   (Independent height)               │ │
│ │   scrollable panel)  │                                      │ │
│ │                      │                                      │ │
│ └──────────────────────┴──────────────────────────────────────┘ │
│                                                                  │
│ Bottom Actions Bar (Save Draft, Preview Draft, Export DOCX)    │
└─────────────────────────────────────────────────────────────────┘

Key Changes:
- Media Browser has its own independent height
- Media Browser is scrollable independently
- Live Preview and Text Editor are independent in right panel
- Both panels can scroll independently
```

## Detailed Structure

### Left Panel: Media Browser
```
┌────────────────────────────────────┐
│ ⚙️ Settings  ⬛ Expand  [0 files] │  ← Header (fixed)
├────────────────────────────────────┤
│                                    │
│ ▶ visit2 (30 files)                │  ← Collapsible folder
│ ▶ visit2/post (32 files)           │
│ ▶ visit2/tasks/drylining (20)      │
│                                    │
│ [Media Grid - Scrollable Area]     │
│                                    │
│ ┌────┐ ┌────┐ ┌────┐              │
│ │img │ │img │ │img │              │
│ └────┘ └────┘ └────┘              │
│                                    │
│ ┌────┐ ┌────┐ ┌────┐              │
│ │img │ │img │ │img │              │
│ └────┘ └────┘ └────┘              │
│                                    │
│ ┌────┐ ┌────┐ ┌────┐              │
│ │img │ │img │ │img │              │
│ └────┘ └────┘ └────┘              │
│                                    │
│ [scrollable]                       │
│                                    │
│ ┌────┐ ┌────┐ ┌────┐              │
│ │img │ │img │ │img │              │
│ └────┘ └────┘ └────┘              │
│                                    │
└────────────────────────────────────┘

Height: Independent, uses available viewport height
Scroll: Independent vertical scrolling
Expand: Can expand to 100% width (hides right panel)
```

### Right Panel: Preview & Editor
```
┌────────────────────────────────────┐
│ Live Preview         ▼ Expand All  │  ← Header (fixed)
├────────────────────────────────────┤
│                                    │
│ [Preview Content - Scrollable]     │
│                                    │
│ Text paragraph 1...                │
│                                    │
│ ┌──────────┬──────────┐            │
│ │  Image   │  Image   │            │
│ └──────────┴──────────┘            │
│                                    │
│ Text paragraph 2...                │
│                                    │
│ ┌──────────┬──────────┐            │
│ │  Image   │  Image   │            │
│ └──────────┴──────────┘            │
│                                    │
│ [more preview content...]          │
│                                    │
├────────────────────────────────────┤
│ Text Editor    Placeholders: 5     │  ← Header (fixed)
├────────────────────────────────────┤
│                                    │
│ [Text Editor - Scrollable]         │
│                                    │
│ Enter text with placeholders...    │
│                                    │
│ {{Image1}}                         │
│                                    │
│ Text here...                       │
│                                    │
│ {{Image2}}                         │
│                                    │
│ [more text...]                     │
│                                    │
└────────────────────────────────────┘

Height: Independent, shares space with preview
Scroll: Independent vertical scrolling for each section
```

## Layout Specifications

### Container Structure
```
.observation-media-container
├── .observation-media-left-panel (Media Browser)
│   ├── Header (fixed, ~40px height)
│   │   ├── Settings button
│   │   ├── Expand button
│   │   └── File count
│   └── Content (scrollable, flex: 1)
│       └── #observationMediaGrid
│           ├── Subfolder sections (collapsible)
│           └── Media cards grid
│
└── .observation-media-right-panel (Preview & Editor)
    ├── Preview Section
    │   ├── Header (fixed, ~40px height)
    │   └── #observationPreview (scrollable, flex: 1)
    └── Text Editor Section
        ├── Header (fixed, ~40px height)
        └── #observationTextEditor (scrollable, flex: 1)
```

### CSS Properties

#### Media Browser (Left Panel)
- `height`: `100vh - topControlsHeight - bottomBarHeight - margins`
- `display`: `flex`, `flex-direction`: `column`
- `overflow`: `hidden` (container)
- Content area: `flex: 1`, `overflow-y: auto`

#### Preview & Editor (Right Panel)
- `height`: `100vh - topControlsHeight - bottomBarHeight - margins`
- `display`: `flex`, `flex-direction`: `column`
- Each section: `flex: 1`, `display: flex`, `flex-direction: column`
- Content areas: `flex: 1`, `overflow-y: auto`

### Key Features

1. **Independent Heights**: Each panel calculates its own height based on viewport
2. **Independent Scrolling**: Each scrollable area scrolls independently
3. **Fixed Headers**: Headers stay visible while content scrolls
4. **Flex Layout**: Uses flexbox for proper space distribution
5. **Responsive**: Panels can expand/collapse while maintaining independence

### Benefits

- ✅ Media browser can show many folders/files without being limited by preview height
- ✅ Preview can be long without affecting media browser
- ✅ Better use of vertical space
- ✅ Both panels scroll independently
- ✅ More content visible at once

### Responsive Behavior

**Desktop (>1024px)**:
- Side-by-side: 50% / 50% or 100% / 0% when expanded

**Tablet (768px - 1024px)**:
- Stacked vertically
- Each panel gets full width
- Each maintains independent scrolling

**Mobile (<768px)**:
- Stacked vertically
- Reduced heights for better mobile UX


