from pathlib import Path
import shutil

required_files = [
    "src/StudyTrack/Components/Pages/Assignments.razor",
    "src/StudyTrack/Components/Pages/Dashboard.razor",
    "src/StudyTrack/docs/TESTING_CHECKLIST.md",
]

for file_path in required_files:
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Required file does not exist: {file_path}")

def backup(path):
    p = Path(path)
    backup_path = p.with_suffix(p.suffix + ".bak_phase4")
    if not backup_path.exists():
        shutil.copy2(p, backup_path)

# Back up existing files first.
for file_path in required_files:
    backup(file_path)

assignments_path = Path("src/StudyTrack/Components/Pages/Assignments.razor")
assignments = assignments_path.read_text(encoding="utf-8")

# Add delete confirmation state only if missing.
if "pendingDeleteAssignmentId" not in assignments:
    assignments = assignments.replace(
        "private int? editingAssignmentId;",
        "private int? editingAssignmentId;\n    private int? pendingDeleteAssignmentId;"
    )

    assignments = assignments.replace(
        '''<button type="button" class="btn btn-sm btn-outline-danger" @onclick="() => DeleteAssignmentAsync(assignment.Id)">Delete</button>''',
        '''@if (pendingDeleteAssignmentId == assignment.Id)
                            {
                                <button type="button" class="btn btn-sm btn-danger" @onclick="() => DeleteAssignmentAsync(assignment.Id)">Confirm Delete</button>
                                <button type="button" class="btn btn-sm btn-outline-secondary" @onclick="CancelDelete">Cancel</button>
                            }
                            else
                            {
                                <button type="button" class="btn btn-sm btn-outline-danger" @onclick="() => RequestDelete(assignment.Id)">Delete</button>
                            }'''
    )

    assignments = assignments.replace(
        "editingAssignmentId = assignment.Id;",
        "editingAssignmentId = assignment.Id;\n        pendingDeleteAssignmentId = null;",
        1
    )

    assignments = assignments.replace(
        '''private async Task DeleteAssignmentAsync(int id)
    {''',
        '''private void RequestDelete(int id)
    {
        ClearMessages();
        editingAssignmentId = null;
        pendingDeleteAssignmentId = id;
        errorMessage = "Delete requested. Click Confirm Delete to permanently remove this assignment.";
    }

    private void CancelDelete()
    {
        ClearMessages();
        pendingDeleteAssignmentId = null;
    }

    private async Task DeleteAssignmentAsync(int id)
    {'''
    )

    assignments = assignments.replace(
        '''await LoadDataAsync();
    }

    private async Task MarkCompletedAsync''',
        '''pendingDeleteAssignmentId = null;
        await LoadDataAsync();
    }

    private async Task MarkCompletedAsync''',
        1
    )

    assignments = assignments.replace(
        '''private void ResetForm()
    {
        editingAssignmentId = null;''',
        '''private void ResetForm()
    {
        editingAssignmentId = null;
        pendingDeleteAssignmentId = null;'''
    )

assignments_path.write_text(assignments, encoding="utf-8")

dashboard_path = Path("src/StudyTrack/Components/Pages/Dashboard.razor")
dashboard = dashboard_path.read_text(encoding="utf-8")

# Dashboard was inspected and is simple placeholder content, so replace it with assignment-aware dashboard.
if "@inject AssignmentService AssignmentService" not in dashboard:
    dashboard_path.write_text("""@page "/"
@page "/dashboard"
@using StudyTrack.Models
@using StudyTrack.Services
@inject AssignmentService AssignmentService
@inject CourseService CourseService

<PageTitle>StudyTrack Dashboard</PageTitle>

<h1>StudyTrack Dashboard</h1>

<p class="lead">
    Welcome to StudyTrack. This dashboard summarizes courses, assignments, deadlines, and study progress.
</p>

@if (isLoading)
{
    <p><em>Loading dashboard...</em></p>
}
else
{
    <section class="dashboard-grid">
        <div class="summary-card">
            <h2>Courses</h2>
            <p>@courseCount course(s) available.</p>
        </div>

        <div class="summary-card">
            <h2>Upcoming</h2>
            <p>@upcomingCount assignment(s) due within the next 7 days.</p>
        </div>

        <div class="summary-card">
            <h2>Overdue</h2>
            <p>@overdueCount overdue assignment(s).</p>
        </div>

        <div class="summary-card">
            <h2>Completed</h2>
            <p>@completedCount completed assignment(s).</p>
        </div>
    </section>

    <section class="crud-panel">
        <div class="section-header">
            <h2>Nearest Deadlines</h2>
            <a class="btn btn-sm btn-outline-primary" href="/assignments">View Assignments</a>
        </div>

        @if (nearestAssignments.Count == 0)
        {
            <div class="empty-state">
                No active upcoming assignments found.
            </div>
        }
        else
        {
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Assignment</th>
                        <th>Course</th>
                        <th>Due Date</th>
                        <th>Priority</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    @foreach (var assignment in nearestAssignments)
                    {
                        <tr>
                            <td>@assignment.Title</td>
                            <td>@(assignment.Course?.Name ?? "No course")</td>
                            <td>@assignment.DueDate.ToString("yyyy-MM-dd")</td>
                            <td><PriorityBadge Priority="assignment.Priority" /></td>
                            <td><StatusBadge Status="assignment.Status" /></td>
                        </tr>
                    }
                </tbody>
            </table>
        }
    </section>
}

@code {
    private bool isLoading = true;
    private int courseCount;
    private int upcomingCount;
    private int overdueCount;
    private int completedCount;
    private List<AssignmentTask> nearestAssignments = new();

    protected override async Task OnInitializedAsync()
    {
        var courses = await CourseService.GetCoursesAsync();
        var assignments = await AssignmentService.GetAssignmentsAsync();

        var today = DateTime.Today;
        var nextWeek = today.AddDays(7);

        courseCount = courses.Count;

        upcomingCount = assignments.Count(a =>
            a.Status != AssignmentStatus.Completed &&
            a.DueDate.Date >= today &&
            a.DueDate.Date <= nextWeek);

        overdueCount = assignments.Count(a =>
            a.Status != AssignmentStatus.Completed &&
            a.DueDate.Date < today);

        completedCount = assignments.Count(a => a.Status == AssignmentStatus.Completed);

        nearestAssignments = assignments
            .Where(a => a.Status != AssignmentStatus.Completed && a.DueDate.Date >= today)
            .OrderBy(a => a.DueDate)
            .Take(5)
            .ToList();

        isLoading = false;
    }
}
""", encoding="utf-8")

testing_path = Path("src/StudyTrack/docs/TESTING_CHECKLIST.md")
testing = testing_path.read_text(encoding="utf-8")

if "## Phase 4: Assignment Management CRUD" not in testing:
    testing += """

---

## Phase 4: Assignment Management CRUD

### Terminal Tests

- [ ] Build succeeds with zero warnings and zero errors.

```bash
dotnet build src/StudyTrack/StudyTrack.csproj
