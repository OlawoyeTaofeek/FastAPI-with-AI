# 15-Day Frontend Challenge

A structured self-directed challenge to build real projects with HTML, CSS, and JavaScript — from a profile card to a full portfolio page. Every project is built from scratch, styled without frameworks, and documented as part of my frontend portfolio.

---

## About

I am Olawoye Taofeek, a self-taught frontend developer building in public. This repository documents my 15-day journey of writing clean, structured HTML, applying CSS layout and design, and progressively introducing JavaScript — one project per day.

The goal is not just to complete projects but to understand every line of code I write.

---

## Projects

### Completed

| Day | Project | Concepts Covered | Status |
|-----|---------|-----------------|--------|
| 01 | [Personal Profile Card](#day-01--personal-profile-card) | Semantic HTML, Flexbox, CSS Box Model, Google Fonts, Font Awesome | ✅ Done |
| 02 | [Pricing Table](#day-02--pricing-table) | CSS Grid, Flexbox, Position Absolute, Hover Effects, Pseudo-classes | ✅ Done |
| P1 | [Notification Card](#practice-1--notification-card) | Flexbox alignment, Border-left accent, Position Absolute | ✅ Done |
| P2 | [Stats Card Row](#practice-2--stats-card-row) | Flexbox with flex: 1, Column direction, Equal spacing | ✅ Done |

### Upcoming

| Day | Project | Key Concepts |
|-----|---------|-------------|
| 03 | CSS Photo Gallery | CSS Grid, overflow hidden, Transition, Opacity |
| 04 | Animated Landing Page Hero | Keyframes, CSS Animations, Flexbox |
| 05 | Responsive Nav Bar | Media Queries, CSS Checkbox Hack, Sticky Position |
| 06 | Quiz App | DOM Manipulation, Event Listeners, Score Tracking |
| 07 | Digital Clock | setInterval, Date Object, Theme Toggle |
| 08 | To-Do List | localStorage, Dynamic DOM, Filter by Status |
| 09 | Random Quote Generator | Arrays, Fetch API, Clipboard API |
| 10 | Tip Calculator | Input Events, Number Parsing, Live UI Updates |
| 11 | Pomodoro Timer | SVG Animation, State Machine, Audio API |
| 12 | Weather App | fetch() & async/await, API Integration, Error Handling |
| 13 | Memory Card Game | Array Shuffle, CSS 3D Flip, Game State Logic |
| 14 | Markdown Previewer | CDN Libraries, textarea Events, Split-pane Layout |
| 15 | Full Portfolio Page | Multi-section Layout, Form Validation, Smooth Scroll |

---

## Project Details

### Day 01 — Personal Profile Card

A styled profile card built entirely with HTML and CSS. Includes an avatar circle that overlaps a banner, skill tags, social links with icons, and a clean bio section.

**What I learned:**
- How the CSS box model (margin, padding, border) controls spacing
- Using Flexbox to align elements side by side
- `border-radius: 50%` for circle shapes and `999px` for pill shapes
- Linking external fonts (Google Fonts) and icon libraries (Font Awesome)
- `position: relative` and `margin-top: -50px` for the overlapping avatar effect

---

### Day 02 — Pricing Table

A 3-column pricing table with a featured plan highlighted by a purple border and a "Most popular" badge sitting on the card edge.

**What I learned:**
- CSS Flexbox with `flex: 1` for equal-width columns
- `position: absolute` and `position: relative` for the badge placement
- `transform: translateX(-50%)` combined with `left: 50%` for true centering
- `:hover` and `:active` pseudo-classes for button interactions
- `transition: all 0.2s` for smooth animations
- Targeting Font Awesome icon classes directly in CSS for color

---

### Practice 1 — Notification Card

A clean notification card with an icon circle, title, message, and timestamp pushed to the top right corner.

**What I learned:**
- `margin-left: auto` inside a flex container to push elements to the far right
- `align-self: flex-start` to pin the timestamp to the top
- `flex-shrink: 0` to prevent the icon circle from squishing
- `border-left` for a colored accent line without extra HTML elements

---

### Practice 2 — Stats Card Row

Three stat cards sitting side by side, each showing a number and label centered inside.

**What I learned:**
- `flex: 1` making all cards take equal width automatically
- `flex-direction: column` with `align-items: center` to stack and center content
- Font size hierarchy — large number vs small label

---

## What I Am Building Towards

By Day 15 this repository will contain a complete frontend portfolio page combining everything covered across the challenge — responsive navigation, animated hero section, project grid, contact form with JavaScript validation, and smooth scroll behavior.

---

## Tech Stack

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)

No frameworks. No libraries. Just vanilla HTML, CSS, and JavaScript.

---

## Structure

```
15-day-frontend-challenge/
├── day-01-profile-card/
│   ├── index.html
│   └── main.css
├── day-02-pricing-table/
│   ├── index.html
│   └── main.css
├── practice-01-notification-card/
│   ├── index.html
│   └── main.css
├── practice-02-stats-card-row/
│   ├── index.html
│   └── main.css
└── README.md
```

---

## Connect

- **GitHub** — you are here
- **Email** — olaideoladipupo069@gmail.com

---

*Updated daily as new projects are completed.*