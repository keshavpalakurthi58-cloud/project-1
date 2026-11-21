---
name: "QuadPulse"
description: "An energetic, high-clarity collegiate event platform built around instant role switching, live database ID context, and frictionless event discovery."
---

## Overview

QuadPulse is the **Guru Nanak University** college event-connecting platform designed for maximum student, organizer, faculty, and administrator engagement without login friction. The refined botanical palette pairs **Soft Creamy Lemon** (`#FAF6DF`) and **Pale Vanilla Cream** (`#FDFBF0`) surfaces with **Deep Customs Green** (`#163828`) sticky navigation, hero spotlights, and VIP passes, and integrates **Muted Gold** (`#C8A24A`) primary CTA buttons, card/pass borders, verified checkmarks, and active tab indicators alongside **Warm Muted Gold** (`#D9B866`) status and date pills. Editorial **Playfair Display** hero and section headings paired with **Lato** body copy keep every interaction crisp and scannable.

## Colors

The refined 4-color architecture eliminates plain `#FFFFFF` and `#000000`, anchoring on **Soft Creamy Lemon** (`surface`, `#FAF6DF`), **Pale Vanilla Cream** (`surface-container-lowest`, `#FDFBF0`), **Deep Customs Green** (`inverse-surface`, `#163828`), and **Muted Gold** (`primary`, `#C8A24A`). Primary CTAs use **Muted Gold** (`#C8A24A`) with **Deep Forest-Customs Ink** (`#10261C`) bold text and `#A88432` hover states; status and date pills use **Warm Muted Gold** (`#D9B866`) with `#10261C` text; and cards, hero banners, and digital passes are framed in **Muted Gold** (`#C8A24A`).

```yaml
colors:
  primary: "#C8A24A"
  on-primary: "#10261C"
  primary-container: "#A88432"
  on-primary-container: "#10261C"
  secondary: "#D9B866"
  on-secondary: "#10261C"
  secondary-container: "#D9B866"
  on-secondary-container: "#10261C"
  tertiary: "#163828"
  on-tertiary: "#FAF6DF"
  tertiary-container: "#F2E394"
  on-tertiary-container: "#10261C"
  error: "#8C2D2E"
  on-error: "#FAF6DF"
  error-container: "#F7DFD8"
  on-error-container: "#4A1213"
  success: "#C8A24A"
  on-success: "#10261C"
  success-container: "#D9B866"
  on-success-container: "#10261C"
  warning: "#7A5416"
  on-warning: "#FAF6DF"
  warning-container: "#D9B866"
  on-warning-container: "#10261C"
  background: "#FAF6DF"
  on-background: "#10261C"
  surface: "#FAF6DF"
  surface-dim: "#EFE7B8"
  surface-bright: "#FDFBF0"
  surface-container-lowest: "#FDFBF0"
  surface-container-low: "#F5EFC9"
  surface-container: "#EFE7B8"
  surface-container-high: "#E8DDA3"
  surface-container-highest: "#DFD28E"
  on-surface: "#10261C"
  surface-variant: "#F5EFC9"
  on-surface-variant: "#354A3F"
  outline: "#C8A24A"
  outline-variant: "#C8A24A"
  inverse-surface: "#163828"
  inverse-on-surface: "#FAF6DF"
  inverse-primary: "#C8A24A"
```

## Typography

QuadPulse pairs **Playfair Display** (SemiBold 600 and Bold 700, generous editorial line-heights) for main page banners, section headings, featured event titles, and digital pass headers with **Lato** (Regular 400 and Bold 700) for body descriptions, form inputs, navigation links, filter pills, and dashboard tables. Electric Teal CTA buttons, role badges, and database IDs (`STU-2026-041`) use **Lato Bold 700** with subtle `+0.04em` tracking and crisp `tabular-nums`.

```yaml
typography:
  display-lg:
    fontFamily: "Playfair Display"
    fontSize: 44px
    fontWeight: 700
    lineHeight: 54px
    letterSpacing: -0.44px
  display-lg-mobile:
    fontFamily: "Playfair Display"
    fontSize: 30px
    fontWeight: 700
    lineHeight: 38px
    letterSpacing: -0.3px
  headline-lg:
    fontFamily: "Playfair Display"
    fontSize: 32px
    fontWeight: 700
    lineHeight: 40px
    letterSpacing: -0.32px
  headline-md:
    fontFamily: "Playfair Display"
    fontSize: 24px
    fontWeight: 600
    lineHeight: 32px
    letterSpacing: -0.2px
  title-lg:
    fontFamily: "Lato"
    fontSize: 20px
    fontWeight: 700
    lineHeight: 28px
    letterSpacing: 0px
  title-md:
    fontFamily: "Lato"
    fontSize: 16px
    fontWeight: 700
    lineHeight: 22px
    letterSpacing: 0px
  body-lg:
    fontFamily: "Lato"
    fontSize: 16px
    fontWeight: 400
    lineHeight: 24px
    letterSpacing: 0px
  body-md:
    fontFamily: "Lato"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 20px
    letterSpacing: 0px
  body-sm:
    fontFamily: "Lato"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 16px
    letterSpacing: 0.1px
  label-lg:
    fontFamily: "Lato"
    fontSize: 14px
    fontWeight: 700
    lineHeight: 20px
    letterSpacing: 0.56px
  label-md:
    fontFamily: "Lato"
    fontSize: 12px
    fontWeight: 700
    lineHeight: 16px
    letterSpacing: 0.48px
  label-sm:
    fontFamily: "Lato"
    fontSize: 11px
    fontWeight: 700
    lineHeight: 14px
    letterSpacing: 0.44px
  mono-sm:
    fontFamily: "Lato"
    fontSize: 12px
    fontWeight: 700
    lineHeight: 16px
    letterSpacing: 0.48px
```

## Layout & Spacing

Desktop layouts use a **1280px max-width 12-column grid** with 24px gutters and 24px page margins, collapsing cleanly to a single-column fluid stack on mobile. A strict 4px/8px spacing rhythm separates internal component padding (`8px`, `12px`, `16px`) from section-level breathing room (`24px`, `32px`, `48px`).

```yaml
spacing:
  gutter-xs: 4px
  gutter-sm: 8px
  gutter-md: 16px
  gutter-lg: 24px
  gutter-xl: 32px
  section: 48px
  page-margin: 24px
```

## Elevation & Depth

Hierarchy relies on **crisp botanical 4-color framing** (`#FAF6DF` Soft Creamy Lemon canvas → `#FDFBF0` Pale Vanilla Cream cards → `#163828` Deep Customs Green sticky navbar, hero spotlight, and VIP pass) paired with `1.5px solid #163828` Deep Customs Green (`outline-variant`) borders and subtle `#163828` structural drop-shadows. Sticky navigation bars use Deep Customs Green (`bg-inverse-surface text-inverse-on-surface`) with Warm Butter Lemon (`#F2E394`) highlights and badges.

## Shapes

Cards and containers use confident, modern **16px (`lg`)** and **12px (`md`)** corners, while buttons, inputs, and dropdown triggers use **10px–12px (`md`)** for a cohesive, approachable collegiate feel. Category pills, status badges, and avatars use `full` (`9999px`).

```yaml
rounded:
  sm: 6px
  DEFAULT: 8px
  md: 12px
  lg: 16px
  xl: 24px
  full: 9999px
```

## Motion & Micro-interaction

Interactions feel snappy and responsive: button presses, registration toggles, and dropdown menus settle within `120ms` (`state-change`), while modals and role-switched view panels enter over `220ms` with an ease-out deceleration curve. All transitions animate only `transform`, `opacity`, and color properties.

```yaml
motion:
  state-change:
    duration: 120ms
    delay: 0ms
    timingFunction: ease-out
  surface-enter:
    duration: 220ms
    delay: 0ms
    timingFunction: cubic-bezier(0.2, 0, 0, 1)
  surface-exit:
    duration: 150ms
    delay: 0ms
    timingFunction: cubic-bezier(0.3, 0, 1, 1)
```

## Voice & Content Strategy

- **Tone of voice:** Energetic, direct, and campus-native—never corporate or bureaucratic. ("3 seats left — grab yours" rather than "Limited availability remaining.")
- **Capitalisation:** Sentence case for headings, descriptions, and navigation; concise verb-first labels for actions (`Register Now`, `Create Event`, `Export Report`, `Switch Role`).
- **Terminology:** Use `Event`, `Organizer`, `Student`, `Admin`, `Database ID`, and `Registration`.
- **Numbers & Dates:** Use `tabular-nums` for all attendee counts, fill rates, and timestamps (e.g., `Thu, Nov 20 · 6:30 PM`, `142 / 160`).

## Components

Component implementations live as individual HTML sticker sheet files in
`components/`. Each file contains the canonical, styled HTML components with
`<!-- COMPONENT: name -->` comment markers. Read each file before use.

- **Button** → `@components/button.html`: `button-primary`, `button-icon`, `button-with-icon`
- **Card** → `@components/card.html`: `card-elevated`, `card-action`, `card-interactive`, `card-interactive-2`
- **Dropdown Menu** → `@components/dropdown-menu.html`: `dropdown-menu-standard`, `dropdown-menu-with-icon`, `dropdown-menu-with-submenu`
- **Table** → `@components/table.html`: `table-standard`, `table-interactive`, `table-selectable`
