# StudyTrack

Student Assignment and Study Planner for CSE 325.

## Project Overview

StudyTrack helps students organize courses, assignments, deadlines, priorities, completion status, and study sessions.

## Current Build Phase

Phase 1: Project skeleton, navigation, layout, branding, and placeholder pages.

## Planned Core Features

- Dashboard summaries
- Course management
- Assignment management
- Filtering and sorting
- Validation and user feedback
- Study session planning

## Development Environment

- Kali Linux / Debian-based terminal workflow
- .NET 8 SDK
- Git and GitHub

## How to Build

Run these commands from the repository root:

    dotnet build src/StudyTrack/StudyTrack.csproj

## Project Board

https://trello.com/b/kXoxNah7


## Phase 1 Navigation Routes

- `/` and `/dashboard` — Dashboard
- `/courses` — Courses
- `/assignments` — Assignments
- `/study-sessions` — Study Sessions
- `/help` — Help and documentation overview


## Phase 3 Course Management

Course management now supports:

- Viewing seeded courses
- Creating courses
- Editing courses
- Deleting courses
- Viewing course details
- Viewing assignments connected to a course
- Validation and user feedback


## Phase 4 Assignment Management

Assignment management now supports:

- Viewing seeded assignments
- Creating assignments
- Editing assignments
- Deleting assignments
- Marking assignments complete
- Reopening completed assignments
- Viewing assignment details
- Viewing study sessions connected to an assignment
- Displaying status and priority badges
- Validation and user feedback


## Phase 5 Dashboard

The dashboard now supports:

- Total assignment count
- Pending assignment count
- Completed assignment count
- Overdue assignment count
- High-priority assignment count
- Upcoming assignment list
- Overdue assignment list
- High-priority assignment list
- Links from dashboard items to assignment details


## Phase 6 Filtering and Sorting

Assignment filtering and sorting now supports:

- Filter by course
- Filter by status
- Filter by priority
- Sort by due date ascending
- Sort by due date descending
- Sort by priority
- Sort by course
- Sort by status
- Clear filters


## Phase 7 Study Session Planning

Study session planning now supports:

- Creating study sessions
- Linking sessions to assignments
- Setting planned dates
- Adding duration in minutes
- Adding notes
- Marking sessions complete
- Reopening sessions
- Deleting sessions


## Phase 8 Validation and Error Handling

Validation and user feedback now includes:

- Reusable validation and feedback panel
- Required field validation
- Friendly not-found messages
- Friendly application error page
- Defensive service checks for invalid IDs and required values
- Success and error feedback after important actions


## Phase 9 UX and Accessibility Polish

Design and usability improvements include:

- Consistent navigation
- Keyboard skip link
- Visible focus outlines
- Improved responsive layout
- Clearer form spacing
- Consistent button styling
- More readable cards and tables
- Improved empty-state presentation
