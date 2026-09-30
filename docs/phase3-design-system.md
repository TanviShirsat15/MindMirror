# MindMirror Phase 3 Design System

## 1. Purpose

This document defines the visual and reusable UI conventions for the MindMirror frontend.

The design system is intended to keep the application:

- Calm
- Professional
- Minimal
- Clean
- Accessible
- Responsive
- Consistent across screens

MindMirror is a personal self-reflection and behavioral analytics application. The interface should not look childish, overly futuristic, or like a clinical/medical application.

---

## 2. Visual Direction

The interface uses a light visual style with low-saturation neutral colors and restrained accent colors.

Primary visual characteristics:

- Light backgrounds
- White content surfaces
- Neutral slate text
- Muted blue/teal-style accents where appropriate
- Subtle borders
- Soft shadows
- Rounded corners
- Clear spacing
- Simple Lucide icons
- Strong readability

The interface should communicate clarity and calmness rather than clinical diagnosis or medical treatment.

---

## 3. Color Tokens

### Neutral Colors

The frontend primarily uses Tailwind slate colors:

- `slate-50` — very light background areas
- `slate-100` — subtle backgrounds
- `slate-200` — borders
- `slate-300` — stronger borders
- `slate-400` — muted interface elements
- `slate-500` — secondary text
- `slate-600` — supporting text
- `slate-700` — primary interface text
- `slate-800` — headings and strong text
- `white` — cards and form surfaces

### Semantic Colors

Semantic colors are used only where their meaning is useful:

- Emerald — success/completed states
- Amber — warning/attention states
- Red — errors
- Sky/blue — informational states

Semantic colors should not be used excessively.

---

## 4. Typography

The interface uses the default Tailwind/system typography stack.

Typography hierarchy:

- Large page headings for major screen titles
- Medium semibold headings for cards and sections
- Regular body text for descriptions
- Smaller muted text for supporting information
- Small text for badges and secondary metadata

Text should remain readable and avoid unnecessary decorative typography.

---

## 5. Spacing

The UI follows Tailwind's spacing scale.

Common spacing values include:

- `p-4` for compact sections
- `p-5` for cards
- `p-6` for larger content areas
- `gap-2` for closely related elements
- `gap-4` for normal component spacing
- `gap-6` for larger sections
- `mt-1` and `mt-2` for supporting text

Spacing should create clear visual grouping without making screens feel crowded.

---

## 6. Border Radius

Rounded corners are used consistently:

- `rounded-lg` for buttons and form controls
- `rounded-xl` for cards and major content containers
- `rounded-full` for badges and pill-shaped elements

The interface should avoid excessive rounding that makes it look playful.

---

## 7. Shadows

Shadows are intentionally subtle.

Primary card treatment:

```text
shadow-sm

8. Focus and Accessibility
Interactive elements should provide visible keyboard focus states.
The UI should support:
- Keyboard navigation
- Visible focus indicators
- Accessible labels
- Appropriate semantic HTML
- aria-* attributes where required
- Sufficient text/background contrast
- Clear error messages
Accessibility is part of the UI implementation, not an optional enhancement.
9. Icons
MindMirror uses Lucide React for interface icons.
Icons should:
- Have a clear purpose
- Be visually consistent
- Avoid replacing important text unnecessarily
- Include accessible labels when an icon-only control is used
Icons should remain simple and professional.
10. Reusable Components
The Phase 3 UI system provides the following reusable components.
Button
Supports:
- Primary
- Secondary
- Ghost
- Disabled
- Loading
Location:
src/components/ui/Button.tsx
Card
Provides a consistent content surface with optional:
- Title
- Description
- Content
Location:
src/components/ui/Card.tsx
Input
Reusable form input supporting:
- Label
- Error message
- Helper text
- Standard HTML input attributes
Location:
src/components/ui/Input.tsx
TextArea
Reusable multiline input supporting:
- Label
- Error message
- Helper text
- Standard textarea attributes
There is no word-count restriction implemented by this component.
Location:
src/components/ui/TextArea.tsx
Badge
Supports semantic variants:
- Default
- Success
- Warning
- Error
- Info
Location:
src/components/ui/Badge.tsx
Modal
Reusable dialog component supporting:
- Open/closed state
- Title
- Close action
- Custom content
- Accessible dialog semantics
Location:
src/components/ui/Modal.tsx
LoadingState
Provides a consistent loading presentation with an optional message.
Location:
src/components/ui/LoadingState.tsx
EmptyState
Provides a consistent presentation when no data exists.
Supports:
- Title
- Description
- Optional action
Location:
src/components/ui/EmptyState.tsx
ErrorState
Provides a consistent error presentation.
Supports:
- Title
- Message
- Optional action
Location:
src/components/ui/ErrorState.tsx
ChartContainer
Provides a consistent container for future Recharts visualizations.
Supports:
- Title
- Description
- Chart content
- Optional custom styling
Location:
src/components/ui/ChartContainer.tsx
11. Form Design
Forms should use:
- Clear labels
- Adequate spacing
- Visible focus states
- Clear validation messages
- Helper text where useful
- Accessible error indicators
Form controls should use consistent borders, radius, padding, and typography.
12. Responsive Design
The application should work across:
- Desktop
- Tablet
- Mobile
The layout should adapt without removing core functionality.
The sidebar/navigation should support smaller screens through the responsive application shell.
Content should not rely on fixed widths that cause horizontal scrolling.
13. UI State Conventions
Screens should account for common application states.
Loading
Use LoadingState.
Empty
Use EmptyState.
Error
Use ErrorState.
Success
Use semantic success feedback such as the Badge component where appropriate.
Normal
Display the normal content state using the standard card, form, and layout components.
14. MindMirror-Specific UI Principles
The interface should present the Well-Being Index as a self-reflection and behavioral analytics measure.
The UI must not visually imply:
- Medical diagnosis
- Clinical measurement
- Medical treatment
- Professional mental-health assessment
The interface should emphasize:
- Personal trends
- Self-reflection
- Habits
- Journal patterns
- Historical changes
- Personal baseline
- Explainable observations
15. Journal UI Principle
Journal entries are unlimited.
The interface must not introduce:
- A 1,000-word minimum
- A 1,000-word maximum
- A fixed word limit
- A fixed number of journal entries
A journal entry may contain:
- One sentence
- A paragraph
- Multiple paragraphs
- Multiline text
The TextArea component therefore does not implement a word-count restriction.
16. Habit UI Principle
Habits are user-customizable.
The interface should support the concept of:
- Adding habits
- Editing habits
- Renaming habits
- Deactivating/deleting habits
- User-defined targets
- Completion tracking
- Historical completion
- Consistency metrics
Starter habits may be displayed as examples, but the system must not depend on a fixed hard-coded habit list.
17. Component Design Principle
Reusable components should remain practical and understandable.
Avoid unnecessary abstraction.
A component should be created when it provides:
- Repeated visual structure
- Repeated behavior
- Consistent accessibility
- Consistent styling
- Clear reuse across multiple screens
Screen-specific logic should remain inside the relevant page when reuse is not justified.
18. Phase 3 Scope Boundary
Phase 3 is focused on the frontend application shell and UI foundation.
The following are intentionally not implemented as real functionality in this phase:
- Production authentication
- Database CRUD
- Real journal persistence
- Real habit persistence
- NLP analysis
- Mamdani fuzzy inference
- Personal baseline calculation
- Production analytics
- Production insight generation
Mock data may be used to demonstrate the interface.
Real functionality will be implemented in later phases.
19. Technology
Frontend technologies used by the Phase 3 design system:
- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Recharts
- Lucide React
No unnecessary frontend framework or UI library is introduced.
20. Consistency Rule
All new Phase 3 screens and components should follow this design system unless there is a documented reason to deviate.
The goal is a consistent, calm, professional, accessible MindMirror experience.