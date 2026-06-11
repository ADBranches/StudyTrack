from pathlib import Path

LT = chr(60)
GT = chr(62)

def fix(text):
    return text.replace("[[LT]]", LT).replace("[[GT]]", GT)

def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(fix(text).strip() + "\n", encoding="utf-8")

write("src/StudyTrack/Components/Layout/MainLayout.razor", """
@inherits LayoutComponentBase

[[LT]]a class="skip-link" href="#main-content"[[GT]]Skip to main content[[LT]]/a[[GT]]

[[LT]]div class="page"[[GT]]
    [[LT]]div class="sidebar"[[GT]]
        [[LT]]NavMenu /[[GT]]
    [[LT]]/div[[GT]]

    [[LT]]main class="studytrack-main"[[GT]]
        [[LT]]div class="top-row px-4 studytrack-topbar"[[GT]]
            [[LT]]span class="app-tagline"[[GT]]Student Assignment and Study Planner[[LT]]/span[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]article id="main-content" class="content px-4" tabindex="-1"[[GT]]
            @Body
        [[LT]]/article[[GT]]

        [[LT]]footer class="studytrack-footer"[[GT]]
            StudyTrack • CSE 325 Group Project • Built for student planning and deadline tracking
        [[LT]]/footer[[GT]]
    [[LT]]/main[[GT]]
[[LT]]/div[[GT]]

[[LT]]div id="blazor-error-ui"[[GT]]
    An unhandled error has occurred.
    [[LT]]a href="" class="reload"[[GT]]Reload[[LT]]/a[[GT]]
    [[LT]]a class="dismiss"[[GT]]🗙[[LT]]/a[[GT]]
[[LT]]/div[[GT]]
""")

write("src/StudyTrack/Components/Layout/NavMenu.razor", """
[[LT]]div class="top-row ps-3 navbar navbar-dark"[[GT]]
    [[LT]]div class="container-fluid"[[GT]]
        [[LT]]a class="navbar-brand" href="" aria-label="StudyTrack dashboard"[[GT]]StudyTrack[[LT]]/a[[GT]]
    [[LT]]/div[[GT]]
[[LT]]/div[[GT]]

[[LT]]input type="checkbox" title="Navigation menu" class="navbar-toggler" aria-label="Toggle navigation menu" /[[GT]]

[[LT]]div class="nav-scrollable" onclick="document.querySelector('.navbar-toggler').click()"[[GT]]
    [[LT]]nav class="flex-column" aria-label="Primary navigation"[[GT]]
        [[LT]]div class="nav-item px-3"[[GT]]
            [[LT]]NavLink class="nav-link" href="" Match="NavLinkMatch.All"[[GT]]
                [[LT]]span class="bi bi-house-door-fill-nav-menu" aria-hidden="true"[[GT]][[LT]]/span[[GT]] Dashboard
            [[LT]]/NavLink[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="nav-item px-3"[[GT]]
            [[LT]]NavLink class="nav-link" href="courses"[[GT]]
                [[LT]]span class="bi bi-list-nested-nav-menu" aria-hidden="true"[[GT]][[LT]]/span[[GT]] Courses
            [[LT]]/NavLink[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="nav-item px-3"[[GT]]
            [[LT]]NavLink class="nav-link" href="assignments"[[GT]]
                [[LT]]span class="bi bi-check2-square" aria-hidden="true"[[GT]][[LT]]/span[[GT]] Assignments
            [[LT]]/NavLink[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="nav-item px-3"[[GT]]
            [[LT]]NavLink class="nav-link" href="study-sessions"[[GT]]
                [[LT]]span class="bi bi-calendar-event" aria-hidden="true"[[GT]][[LT]]/span[[GT]] Study Sessions
            [[LT]]/NavLink[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="nav-item px-3"[[GT]]
            [[LT]]NavLink class="nav-link" href="help"[[GT]]
                [[LT]]span class="bi bi-info-circle" aria-hidden="true"[[GT]][[LT]]/span[[GT]] Help
            [[LT]]/NavLink[[GT]]
        [[LT]]/div[[GT]]
    [[LT]]/nav[[GT]]
[[LT]]/div[[GT]]
""")

css_path = Path("src/StudyTrack/wwwroot/css/app.css")
css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

phase9_css = """
/* Phase 9 UX, accessibility, and responsive polish */
:root {
    --studytrack-primary: #240046;
    --studytrack-primary-light: #7b5ea7;
    --studytrack-accent: #3b5bdb;
    --studytrack-border: #d6d5d5;
    --studytrack-surface: #ffffff;
    --studytrack-muted: #555555;
    --studytrack-focus: #ffbf47;
}

html {
    scroll-behavior: smooth;
}

body {
    color: #222222;
    background: #f7f7fb;
}

.skip-link {
    position: absolute;
    left: -999px;
    top: 0;
    z-index: 9999;
    padding: 0.75rem 1rem;
    background: #ffffff;
    color: #000000;
    border: 3px solid var(--studytrack-focus);
    border-radius: 0.35rem;
}

.skip-link:focus {
    left: 1rem;
    top: 1rem;
}

.studytrack-main {
    background: #f7f7fb;
    min-height: 100vh;
}

.content {
    max-width: 1200px;
    margin: 0 auto;
}

.content h1 {
    font-size: clamp(2rem, 4vw, 2.6rem);
    margin-bottom: 0.75rem;
}

.content h2 {
    font-size: clamp(1.35rem, 3vw, 1.9rem);
}

.lead {
    max-width: 860px;
    line-height: 1.6;
}

.nav-link {
    border-radius: 0.35rem;
    transition: background-color 0.15s ease-in-out, color 0.15s ease-in-out;
}

.nav-link:focus,
.navbar-brand:focus,
button:focus,
.btn:focus,
input:focus,
select:focus,
textarea:focus,
a:focus {
    outline: 3px solid var(--studytrack-focus);
    outline-offset: 2px;
}

.crud-panel,
.details-panel,
.dashboard-section,
.summary-card,
.placeholder-panel {
    border-color: var(--studytrack-border);
    border-radius: 0.85rem;
}

.crud-panel,
.details-panel,
.dashboard-section {
    overflow-x: auto;
}

.form-control {
    min-height: 2.35rem;
}

label {
    color: #222222;
}

.btn {
    min-height: 2.25rem;
    border-radius: 0.35rem;
    font-weight: 600;
}

.btn-sm {
    min-height: 2rem;
}

.table {
    background: #ffffff;
}

.table th {
    white-space: nowrap;
}

.table td {
    line-height: 1.45;
}

.empty-state {
    font-weight: 600;
}

.feedback-panel {
    max-width: 900px;
}

.dashboard-grid {
    align-items: stretch;
}

.summary-card {
    min-height: 6.5rem;
}

.dashboard-item-title {
    color: #124bc2;
}

.dashboard-item-title:hover {
    color: #0a2f7a;
}

@media (max-width: 900px) {
    .content {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    .section-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

    .button-row {
        flex-direction: column;
        align-items: stretch;
    }

    .button-row .btn,
    .course-table .btn,
    .assignment-table .btn,
    .study-session-table .btn {
        width: 100%;
        margin-top: 0.25rem;
    }

    .dashboard-grid {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 700px) {
    .table {
        font-size: 0.92rem;
    }

    .crud-panel,
    .details-panel,
    .dashboard-section {
        padding: 0.85rem;
    }

    .studytrack-footer {
        text-align: center;
    }
}
"""

if "Phase 9 UX" not in css:
    css = css.rstrip() + "\n\n" + phase9_css.strip() + "\n"

css_path.write_text(css, encoding="utf-8")

# Add helpful empty-state wording to Dashboard if not already present.
dashboard_path = Path("src/StudyTrack/Components/Pages/Dashboard.razor")
dashboard = dashboard_path.read_text(encoding="utf-8")
dashboard = dashboard.replace(
    "Quickly review upcoming, overdue, completed, and high-priority assignments.",
    "Quickly review upcoming, overdue, completed, and high-priority assignments from one clear dashboard."
)
dashboard_path.write_text(dashboard, encoding="utf-8")

# Improve page descriptions slightly.
courses_path = Path("src/StudyTrack/Components/Pages/Courses.razor")
courses = courses_path.read_text(encoding="utf-8")
courses = courses.replace(
    "Create, view, update, and delete courses. Courses organize assignments by class or subject.",
    "Create, view, update, and delete courses. Courses organize assignments by class or subject and keep student work structured."
)
courses_path.write_text(courses, encoding="utf-8")

assignments_path = Path("src/StudyTrack/Components/Pages/Assignments.razor")
assignments = assignments_path.read_text(encoding="utf-8")
assignments = assignments.replace(
    "Create, view, update, delete, complete, reopen, filter, and sort assignments.",
    "Create, view, update, delete, complete, reopen, filter, and sort assignments with clear priority and status indicators."
)
assignments_path.write_text(assignments, encoding="utf-8")

testing_path = Path("docs/TESTING_CHECKLIST.md")
testing = testing_path.read_text(encoding="utf-8")

if "## Phase 9 Checks" not in testing:
    testing += """

## Phase 9 Checks

- [ ] Navigation is clear and consistent
- [ ] Skip link exists for keyboard users
- [ ] Focus outlines are visible
- [ ] Page headings are consistent
- [ ] Form labels are visible and meaningful
- [ ] Buttons are readable and consistently styled
- [ ] Tables/cards remain usable on smaller screens
- [ ] Empty-state messages are readable
- [ ] Color contrast is readable
- [ ] Dashboard, Courses, and Assignments pages remain functional
- [ ] Project builds successfully
"""
testing_path.write_text(testing, encoding="utf-8")

devnotes_path = Path("docs/DEVELOPER_NOTES.md")
devnotes = devnotes_path.read_text(encoding="utf-8")

if "## Phase 9 Notes" not in devnotes:
    devnotes += """

## Phase 9 Notes

Phase 9 improves design, UX, accessibility, and responsiveness. The app now includes a skip link, visible focus outlines, clearer layout spacing, improved responsive form/table behavior, and more consistent visual styling across dashboard, course, assignment, and study-session workflows.
"""
devnotes_path.write_text(devnotes, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")

if "## Phase 9 UX and Accessibility Polish" not in readme:
    readme += """

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
"""
readme_path.write_text(readme, encoding="utf-8")

print("Phase 9 patch applied successfully.")

