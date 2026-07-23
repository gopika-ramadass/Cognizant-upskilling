# Hands-On 9: Web Accessibility (WCAG 2.1 AA) & Responsive UI Design

## Overview
This hands-on exercise enhances the Student Portal application with **WCAG 2.1 AA Web Accessibility Compliance**, **ARIA Live Regions & Navigation Landmarks**, **Keyboard Navigability & Focus Management**, **Responsive CSS Design**, and a complete **Accessibility Audit & Remediation Report**.

---

## Key Technical Features Implemented

### 1. WCAG 2.1 AA Web Accessibility & Structural Semantics
- **Skip to Main Content Link (`.skip-link`)**: Positioned off-screen by default, becomes visible when receiving keyboard focus to allow screen reader and keyboard users to bypass header navigation directly to `#main-content`.
- **Landmark Regions**: Uses native semantic HTML5 tags (`<header role="banner">`, `<nav aria-label="Main navigation">`, `<main id="main-content">`, `<footer role="contentinfo">`).
- **Explicit Label Associations**: All input fields (course search, full name, email, semester) are explicitly linked to `<label htmlFor="...">` elements with descriptive labels.
- **Heading Hierarchy**: Enforces a logical heading structure from `<h1>` (hero title) down to `<h2>` (section headers) and `<h3>` (course card titles) without skipping levels.

### 2. ARIA Live Regions & Interactive Focus Management
- **Screen Reader Announcements (`aria-live="polite"`)**: Uses `role="status"` and `aria-live="polite"` to automatically announce search filter result updates (e.g. *"Showing 3 of 5 courses matching search criteria."*) without interrupting speech.
- **Interactive Keyboard Controls**: Course cards support `tabIndex={0}` and keyboard handlers for `Enter` and `Space` key triggers to toggle course enrollment.
- **ARIA States & Properties**:
  - `aria-expanded`: Dynamically tracks mobile navigation menu expansion state.
  - `aria-controls`: Associates mobile toggle button with the primary navigation element.
  - `aria-pressed`: Reflects course enrollment button state.
  - `aria-current="page"`: Indicates active page tab.

### 3. Responsive & High-Contrast Design
- **Color Contrast**: All text elements meet WCAG 2.1 AA minimum contrast requirements (minimum 4.5:1 contrast ratio for normal text, 3:1 for UI elements).
- **Responsive Layout**: CSS Grid and Flexbox with `minmax()` breakpoints ensure smooth scaling across desktop, tablet, and mobile viewports.
- **Focus Ring Customisation**: Clear `:focus-visible` styling (`outline: 3px solid #2563eb`, `outline-offset: 3px`) provides visible focus indicators for all interactive controls.

---

## Accessibility Audit & Remediation Summary

| Flagged Violation | WCAG Success Criterion | Remediation Fix Applied |
| :--- | :--- | :--- |
| **Missing Image Alt Text** | 1.1.1 Non-text Content | Added descriptive `alt` text to functional images and `alt=""` to decorative icons. |
| **Orphan Form Inputs** | 1.3.1 Info and Relationships | Linked all `<input>` elements to explicit `<label htmlFor="...">` tags. |
| **Skipped Heading Levels** | 1.3.1 Structural Hierarchy | Corrected heading tree sequentially (`<h1>` → `<h2>` → `3`). |
| **Non-semantic Interactive Elements** | 2.1.1 Keyboard Navigability | Converted `<div>`/`<span>` click handlers to native `<button type="button">` or added keyboard `Enter`/`Space` handlers. |
| **Missing Navigation Context** | 4.1.2 Name, Role, Value | Added `aria-label="Main navigation"` to `<nav>` and `aria-current="page"` to active links. |
| **Unannounced Search Filtering** | 4.1.3 Status Messages | Added `role="status"` and `aria-live="polite"` live region container for search count. |

---

## How to Run & Verify

1. **Install Dependencies**:
   ```bash
   npm install
   ```

2. **Run Development Server**:
   ```bash
   npm run dev
   ```

3. **Production Build**:
   ```bash
   npm run build
   ```

4. **Verify Features**:
   - Press `Tab` on page load to reveal the **"Skip to main content"** link.
   - Use `Tab`, `Enter`, and `Space` to navigate through navigation tabs and course catalog cards.
   - Type in the search box and verify real-time status announcements in screen reader / ARIA live inspector.
