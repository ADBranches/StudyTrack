# StudyTrack Developer Notes

This document records implementation decisions, project structure, build commands, and development notes.

## Environment

- Kali Linux / Debian
- .NET 8 SDK
- Terminal-first workflow

## Current Phase

Phase 1: project skeleton and navigation.


## Phase 1 Notes

Phase 1 creates the application shell, layout, navigation links, placeholder pages, early responsive styling, and route validation process.


## Phase 3 Notes

Phase 3 implements Course Management CRUD. CourseService handles database operations. Courses.razor provides list, create, edit, and delete workflows with validation and user feedback. CourseDetails.razor shows course metadata and assignments linked to the selected course.


## Phase 4 Notes

Phase 4 implements Assignment Management CRUD. AssignmentService handles database operations. Assignments.razor provides list, create, edit, delete, complete, and reopen workflows with validation and feedback. AssignmentDetails.razor shows assignment metadata and connected study sessions. StatusBadge and PriorityBadge provide clear visual status/priority indicators.


## Phase 5 Notes

Phase 5 implements dashboard summary views. DashboardService calculates assignment totals, pending count, completed count, overdue count, high-priority count, upcoming assignments, overdue assignments, and high-priority assignments. Dashboard.razor displays these summaries and links users to assignment details.


## Phase 6 Notes

Phase 6 adds filtering and sorting to assignment management. Users can filter assignments by course, status, and priority. Users can sort assignments by due date, priority, course, or status. Filters can be cleared from the assignment page.


## Phase 7 Notes

Phase 7 implements study session planning. StudySessionService handles create, list, complete, reopen, and delete operations. StudySessions.razor lets users link sessions to assignments, set planned dates, add durations, add notes, and track completion.


## Phase 8 Notes

Phase 8 improves validation, error handling, and user feedback. ValidationMessagePanel provides reusable success, error, and warning messages. CourseService and AssignmentService include defensive checks for invalid IDs and required values. Error.razor provides a friendlier fallback error page.
