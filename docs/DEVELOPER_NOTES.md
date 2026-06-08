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
