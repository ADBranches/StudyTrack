from pathlib import Path

LT = chr(60)
GT = chr(62)

def convert(text):
    return text.replace("[[LT]]", LT).replace("[[GT]]", GT)

def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(convert(text).strip() + "\n", encoding="utf-8")

# Nav menu
write("src/StudyTrack/Components/Layout/NavMenu.razor", r'''
[[LT]]div class="top-row ps-3 navbar navbar-dark"[[GT]]
    [[LT]]div class="container-fluid"[[GT]]
        [[LT]]a class="navbar-brand" href=""[[GT]]StudyTrack[[LT]]/a[[GT]]
    [[LT]]/div[[GT]]
[[LT]]/div[[GT]]

[[LT]]input type="checkbox" title="Navigation menu" class="navbar-toggler" /[[GT]]

[[LT]]div class="nav-scrollable" onclick="document.querySelector('.navbar-toggler').click()"[[GT]]
    [[LT]]nav class="flex-column"[[GT]]
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
''')

# Main layout
write("src/StudyTrack/Components/Layout/MainLayout.razor", r'''
@inherits LayoutComponentBase

[[LT]]div class="page"[[GT]]
    [[LT]]div class="sidebar"[[GT]]
        [[LT]]NavMenu /[[GT]]
    [[LT]]/div[[GT]]

    [[LT]]main[[GT]]
        [[LT]]div class="top-row px-4 studytrack-topbar"[[GT]]
            [[LT]]span class="app-tagline"[[GT]]Student Assignment and Study Planner[[LT]]/span[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]article class="content px-4"[[GT]]
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
''')

# Dashboard page
write("src/StudyTrack/Components/Pages/Dashboard.razor", r'''
@page "/"
@page "/dashboard"

[[LT]]PageTitle[[GT]]StudyTrack Dashboard[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]StudyTrack Dashboard[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Welcome to StudyTrack. This dashboard will summarize courses, assignments, deadlines, and study progress.
[[LT]]/p[[GT]]

[[LT]]section class="dashboard-grid"[[GT]]
    [[LT]]div class="summary-card"[[GT]]
        [[LT]]h2[[GT]]Upcoming[[LT]]/h2[[GT]]
        [[LT]]p[[GT]]Assignments due soon will appear here.[[LT]]/p[[GT]]
    [[LT]]/div[[GT]]

    [[LT]]div class="summary-card"[[GT]]
        [[LT]]h2[[GT]]Overdue[[LT]]/h2[[GT]]
        [[LT]]p[[GT]]Overdue assignments will be highlighted here.[[LT]]/p[[GT]]
    [[LT]]/div[[GT]]

    [[LT]]div class="summary-card"[[GT]]
        [[LT]]h2[[GT]]Completed[[LT]]/h2[[GT]]
        [[LT]]p[[GT]]Completed assignment progress will be shown here.[[LT]]/p[[GT]]
    [[LT]]/div[[GT]]
[[LT]]/section[[GT]]
''')

# Courses page
write("src/StudyTrack/Components/Pages/Courses.razor", r'''
@page "/courses"

[[LT]]PageTitle[[GT]]Courses[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]Courses[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Course management will let students create, view, edit, and remove courses.
[[LT]]/p[[GT]]

[[LT]]div class="placeholder-panel"[[GT]]
    [[LT]]h2[[GT]]Planned Course Actions[[LT]]/h2[[GT]]
    [[LT]]ul[[GT]]
        [[LT]]li[[GT]]Create a course[[LT]]/li[[GT]]
        [[LT]]li[[GT]]View course list[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Edit course details[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Delete a course[[LT]]/li[[GT]]
        [[LT]]li[[GT]]View assignments connected to a course[[LT]]/li[[GT]]
    [[LT]]/ul[[GT]]
[[LT]]/div[[GT]]
''')

# Assignments page
write("src/StudyTrack/Components/Pages/Assignments.razor", r'''
@page "/assignments"

[[LT]]PageTitle[[GT]]Assignments[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]Assignments[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Assignment management will support creating, viewing, editing, deleting, filtering, and marking assignments complete.
[[LT]]/p[[GT]]

[[LT]]table class="table table-striped skeleton-table"[[GT]]
    [[LT]]thead[[GT]]
        [[LT]]tr[[GT]]
            [[LT]]th[[GT]]Assignment[[LT]]/th[[GT]]
            [[LT]]th[[GT]]Course[[LT]]/th[[GT]]
            [[LT]]th[[GT]]Due Date[[LT]]/th[[GT]]
            [[LT]]th[[GT]]Priority[[LT]]/th[[GT]]
            [[LT]]th[[GT]]Status[[LT]]/th[[GT]]
        [[LT]]/tr[[GT]]
    [[LT]]/thead[[GT]]
    [[LT]]tbody[[GT]]
        [[LT]]tr[[GT]]
            [[LT]]td[[GT]]Sample Assignment Workflow[[LT]]/td[[GT]]
            [[LT]]td[[GT]]CSE 325[[LT]]/td[[GT]]
            [[LT]]td[[GT]]Pending model phase[[LT]]/td[[GT]]
            [[LT]]td[[GT]]High[[LT]]/td[[GT]]
            [[LT]]td[[GT]]Planned[[LT]]/td[[GT]]
        [[LT]]/tr[[GT]]
    [[LT]]/tbody[[GT]]
[[LT]]/table[[GT]]
''')

# Study sessions page
write("src/StudyTrack/Components/Pages/StudySessions.razor", r'''
@page "/study-sessions"

[[LT]]PageTitle[[GT]]Study Sessions[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]Study Sessions[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Study sessions will help students plan focused time for assignments and track preparation progress.
[[LT]]/p[[GT]]

[[LT]]div class="placeholder-panel"[[GT]]
    [[LT]]h2[[GT]]Planned Study Session Actions[[LT]]/h2[[GT]]
    [[LT]]ul[[GT]]
        [[LT]]li[[GT]]Create a study session[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Link a study session to an assignment[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Add planned date and duration[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Add notes[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Mark study session complete[[LT]]/li[[GT]]
    [[LT]]/ul[[GT]]
[[LT]]/div[[GT]]
''')

# Help page
write("src/StudyTrack/Components/Pages/Help.razor", r'''
@page "/help"

[[LT]]PageTitle[[GT]]StudyTrack Help[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]StudyTrack Help[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    This page will guide users through dashboard, course, assignment, and study-session workflows.
[[LT]]/p[[GT]]

[[LT]]div class="placeholder-panel"[[GT]]
    [[LT]]h2[[GT]]Documentation Links[[LT]]/h2[[GT]]
    [[LT]]ul[[GT]]
        [[LT]]li[[GT]]User guide: docs/USER_GUIDE.md[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Developer notes: docs/DEVELOPER_NOTES.md[[LT]]/li[[GT]]
        [[LT]]li[[GT]]Testing checklist: docs/TESTING_CHECKLIST.md[[LT]]/li[[GT]]
    [[LT]]/ul[[GT]]
[[LT]]/div[[GT]]
''')

# Remove default pages that are no longer part of navigation.
for old_page in [
    "src/StudyTrack/Components/Pages/Home.razor",
    "src/StudyTrack/Components/Pages/Counter.razor",
    "src/StudyTrack/Components/Pages/Weather.razor"
]:
    Path(old_page).unlink(missing_ok=True)

# Add phase-specific CSS file.
write("src/StudyTrack/wwwroot/css/app.css", r'''
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}

.summary-card,
.placeholder-panel {
    border: 1px solid #d6d5d5;
    border-radius: 0.75rem;
    padding: 1rem;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.summary-card h2,
.placeholder-panel h2 {
    font-size: 1.15rem;
    margin-bottom: 0.5rem;
}

.studytrack-topbar {
    font-weight: 600;
}

.app-tagline {
    color: #2f4f6f;
}

.studytrack-footer {
    border-top: 1px solid #d6d5d5;
    margin-top: 2rem;
    padding: 1rem 1.5rem;
    color: #333333;
    background: #f8f9fa;
    font-size: 0.95rem;
}

.lead {
    font-size: 1.08rem;
    color: #333333;
}

.skeleton-table {
    margin-top: 1rem;
}

@media (max-width: 700px) {
    .studytrack-footer {
        padding: 0.75rem;
        font-size: 0.85rem;
    }
}
''')

# Ensure App.razor links the phase CSS.
app_path = Path("src/StudyTrack/Components/App.razor")
app_text = app_path.read_text(encoding="utf-8")
link_line = '    <link rel="stylesheet" href="css/app.css" />'
if 'href="css/app.css"' not in app_text:
    app_text = app_text.replace('    <link rel="stylesheet" href="app.css" />', '    <link rel="stylesheet" href="app.css" />\n' + link_line)
app_path.write_text(app_text, encoding="utf-8")

# Update README phase.
readme = Path("README.md")
readme_text = readme.read_text(encoding="utf-8")
readme_text = readme_text.replace("Phase 0: Project setup and repository hygiene.", "Phase 1: Project skeleton, navigation, layout, branding, and placeholder pages.")
if "## Phase 1 Navigation Routes" not in readme_text:
    readme_text += """

## Phase 1 Navigation Routes

- `/` and `/dashboard` — Dashboard
- `/courses` — Courses
- `/assignments` — Assignments
- `/study-sessions` — Study Sessions
- `/help` — Help and documentation overview
"""
readme.write_text(readme_text, encoding="utf-8")

# Update testing checklist.
testing = Path("docs/TESTING_CHECKLIST.md")
testing_text = testing.read_text(encoding="utf-8")
if "## Phase 1 Checks" not in testing_text:
    testing_text += """

## Phase 1 Checks

- [ ] App builds successfully
- [ ] App runs locally
- [ ] Dashboard route opens
- [ ] Courses route opens
- [ ] Assignments route opens
- [ ] Study Sessions route opens
- [ ] Help route opens
- [ ] Navigation links are visible
- [ ] StudyTrack branding is visible
- [ ] Layout footer is visible
"""
testing.write_text(testing_text, encoding="utf-8")

# Update developer notes.
devnotes = Path("docs/DEVELOPER_NOTES.md")
dev_text = devnotes.read_text(encoding="utf-8")
dev_text = dev_text.replace("Phase 0: repository setup and hygiene.", "Phase 1: project skeleton and navigation.")
if "## Phase 1 Notes" not in dev_text:
    dev_text += """

## Phase 1 Notes

Phase 1 creates the application shell, layout, navigation links, placeholder pages, early responsive styling, and route validation process.
"""
devnotes.write_text(dev_text, encoding="utf-8")
