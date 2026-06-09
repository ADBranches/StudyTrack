from pathlib import Path

LT = chr(60)
GT = chr(62)
ARROW = "=>"

def fix(text):
    return (
        text.replace("[[LT]]", LT)
            .replace("[[GT]]", GT)
            .replace("[[ARROW]]", ARROW)
    )

def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(fix(text).strip() + "\n", encoding="utf-8")

write("src/StudyTrack/Services/DashboardService.cs", """
using Microsoft.EntityFrameworkCore;
using StudyTrack.Data;
using StudyTrack.Models;

namespace StudyTrack.Services;

public class DashboardService
{
    private readonly StudyTrackDbContext _context;

    public DashboardService(StudyTrackDbContext context)
    {
        _context = context;
    }

    public async Task[[LT]]DashboardSummary[[GT]] GetDashboardSummaryAsync()
    {
        var today = DateTime.Today;
        var upcomingLimit = today.AddDays(7);

        var assignments = await _context.AssignmentTasks
            .Include(assignment [[ARROW]] assignment.Course)
            .OrderBy(assignment [[ARROW]] assignment.DueDate)
            .ToListAsync();

        var pendingAssignments = assignments
            .Where(assignment [[ARROW]] assignment.Status != AssignmentStatus.Completed)
            .ToList();

        return new DashboardSummary
        {
            TotalAssignments = assignments.Count,
            PendingCount = pendingAssignments.Count,
            CompletedCount = assignments.Count(assignment [[ARROW]] assignment.Status == AssignmentStatus.Completed),
            OverdueCount = assignments.Count(assignment [[ARROW]]
                assignment.Status != AssignmentStatus.Completed &&
                assignment.DueDate.Date < today),
            HighPriorityCount = pendingAssignments.Count(assignment [[ARROW]] assignment.Priority == AssignmentPriority.High),
            UpcomingAssignments = pendingAssignments
                .Where(assignment [[ARROW]] assignment.DueDate.Date >= today && assignment.DueDate.Date <= upcomingLimit)
                .OrderBy(assignment [[ARROW]] assignment.DueDate)
                .Take(5)
                .ToList(),
            OverdueAssignments = pendingAssignments
                .Where(assignment [[ARROW]] assignment.DueDate.Date < today)
                .OrderBy(assignment [[ARROW]] assignment.DueDate)
                .Take(5)
                .ToList(),
            HighPriorityAssignments = pendingAssignments
                .Where(assignment [[ARROW]] assignment.Priority == AssignmentPriority.High)
                .OrderBy(assignment [[ARROW]] assignment.DueDate)
                .Take(5)
                .ToList()
        };
    }
}

public class DashboardSummary
{
    public int TotalAssignments { get; set; }
    public int PendingCount { get; set; }
    public int CompletedCount { get; set; }
    public int OverdueCount { get; set; }
    public int HighPriorityCount { get; set; }

    public List[[LT]]AssignmentTask[[GT]] UpcomingAssignments { get; set; } = new();
    public List[[LT]]AssignmentTask[[GT]] OverdueAssignments { get; set; } = new();
    public List[[LT]]AssignmentTask[[GT]] HighPriorityAssignments { get; set; } = new();
}
""")

write("src/StudyTrack/Components/Pages/Dashboard.razor", """
@page "/"
@page "/dashboard"
@rendermode InteractiveServer
@using StudyTrack.Models
@using StudyTrack.Services
@inject DashboardService DashboardService

[[LT]]PageTitle[[GT]]StudyTrack Dashboard[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]StudyTrack Dashboard[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Quickly review upcoming, overdue, completed, and high-priority assignments.
[[LT]]/p[[GT]]

@if (isLoading)
{
    [[LT]]p[[GT]][[LT]]em[[GT]]Loading dashboard...[[LT]]/em[[GT]][[LT]]/p[[GT]]
}
else if (summary is not null)
{
    [[LT]]section class="dashboard-grid"[[GT]]
        [[LT]]div class="summary-card"[[GT]]
            [[LT]]span class="summary-label"[[GT]]Total Assignments[[LT]]/span[[GT]]
            [[LT]]strong class="summary-number"[[GT]]@summary.TotalAssignments[[LT]]/strong[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="summary-card"[[GT]]
            [[LT]]span class="summary-label"[[GT]]Pending[[LT]]/span[[GT]]
            [[LT]]strong class="summary-number"[[GT]]@summary.PendingCount[[LT]]/strong[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="summary-card summary-completed"[[GT]]
            [[LT]]span class="summary-label"[[GT]]Completed[[LT]]/span[[GT]]
            [[LT]]strong class="summary-number"[[GT]]@summary.CompletedCount[[LT]]/strong[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="summary-card summary-overdue"[[GT]]
            [[LT]]span class="summary-label"[[GT]]Overdue[[LT]]/span[[GT]]
            [[LT]]strong class="summary-number"[[GT]]@summary.OverdueCount[[LT]]/strong[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="summary-card summary-high"[[GT]]
            [[LT]]span class="summary-label"[[GT]]High Priority[[LT]]/span[[GT]]
            [[LT]]strong class="summary-number"[[GT]]@summary.HighPriorityCount[[LT]]/strong[[GT]]
        [[LT]]/div[[GT]]
    [[LT]]/section[[GT]]

    [[LT]]section class="dashboard-section"[[GT]]
        [[LT]]h2[[GT]]Upcoming Assignments[[LT]]/h2[[GT]]
        @RenderAssignmentList(summary.UpcomingAssignments, "No upcoming assignments in the next 7 days.")
    [[LT]]/section[[GT]]

    [[LT]]section class="dashboard-section dashboard-urgent"[[GT]]
        [[LT]]h2[[GT]]Overdue Assignments[[LT]]/h2[[GT]]
        @RenderAssignmentList(summary.OverdueAssignments, "No overdue assignments.")
    [[LT]]/section[[GT]]

    [[LT]]section class="dashboard-section"[[GT]]
        [[LT]]h2[[GT]]High-Priority Assignments[[LT]]/h2[[GT]]
        @RenderAssignmentList(summary.HighPriorityAssignments, "No high-priority pending assignments.")
    [[LT]]/section[[GT]]
}

@code {
    private DashboardSummary? summary;
    private bool isLoading = true;

    protected override async Task OnInitializedAsync()
    {
        summary = await DashboardService.GetDashboardSummaryAsync();
        isLoading = false;
    }

    private RenderFragment RenderAssignmentList(List[[LT]]AssignmentTask[[GT]] assignments, string emptyMessage) => builder =>
    {
        var sequence = 0;

        if (assignments.Count == 0)
        {
            builder.OpenElement(sequence++, "div");
            builder.AddAttribute(sequence++, "class", "empty-state");
            builder.AddContent(sequence++, emptyMessage);
            builder.CloseElement();
            return;
        }

        builder.OpenElement(sequence++, "div");
        builder.AddAttribute(sequence++, "class", "dashboard-list");

        foreach (var assignment in assignments)
        {
            builder.OpenElement(sequence++, "article");
            builder.AddAttribute(sequence++, "class", "dashboard-list-item");

            builder.OpenElement(sequence++, "div");
            builder.AddAttribute(sequence++, "class", "dashboard-item-main");

            builder.OpenElement(sequence++, "a");
            builder.AddAttribute(sequence++, "href", $"/assignments/{assignment.Id}");
            builder.AddAttribute(sequence++, "class", "dashboard-item-title");
            builder.AddContent(sequence++, assignment.Title);
            builder.CloseElement();

            builder.OpenElement(sequence++, "div");
            builder.AddAttribute(sequence++, "class", "muted-text");
            builder.AddContent(sequence++, $"{assignment.Course?.Name ?? "No course"} • Due {assignment.DueDate:yyyy-MM-dd}");
            builder.CloseElement();

            builder.CloseElement();

            builder.OpenElement(sequence++, "div");
            builder.AddAttribute(sequence++, "class", "dashboard-badge-row");
            builder.OpenComponentsequence++;
            builder.AddAttribute(sequence++, "Priority", assignment.Priority);
            builder.CloseComponent();

            builder.OpenComponentsequence++;
            builder.AddAttribute(sequence++, "Status", assignment.Status);
            builder.CloseComponent();
            builder.CloseElement();

            builder.CloseElement();
        }

        builder.CloseElement();
    };
}
""")

# Register DashboardService.
program_path = Path("src/StudyTrack/Program.cs")
program = program_path.read_text(encoding="utf-8")

if "builder.Services.AddScoped<DashboardService>();" not in program:
    if "builder.Services.AddScoped<AssignmentService>();" in program:
        program = program.replace(
            "builder.Services.AddScoped<AssignmentService>();",
            "builder.Services.AddScoped<AssignmentService>();\nbuilder.Services.AddScoped<DashboardService>();"
        )
    else:
        program += "\nbuilder.Services.AddScoped<DashboardService>();\n"

program_path.write_text(fix(program), encoding="utf-8")

css_path = Path("src/StudyTrack/wwwroot/css/app.css")
css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

phase5_css = """
.summary-label {
    display: block;
    color: #555555;
    font-weight: 700;
    margin-bottom: 0.4rem;
}

.summary-number {
    display: block;
    font-size: 2rem;
    color: #222222;
}

.summary-overdue {
    border-left: 6px solid #dc3545;
}

.summary-high {
    border-left: 6px solid #ffc107;
}

.summary-completed {
    border-left: 6px solid #198754;
}

.dashboard-section {
    border: 1px solid #d6d5d5;
    border-radius: 0.75rem;
    padding: 1rem;
    margin-top: 1.25rem;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.dashboard-urgent {
    border-left: 6px solid #dc3545;
}

.dashboard-list {
    display: grid;
    gap: 0.75rem;
}

.dashboard-list-item {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    border-bottom: 1px solid #eeeeee;
    padding-bottom: 0.75rem;
}

.dashboard-list-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.dashboard-item-title {
    font-weight: 700;
    text-decoration: none;
}

.dashboard-badge-row {
    display: flex;
    gap: 0.35rem;
    align-items: center;
    flex-wrap: wrap;
}

@media (max-width: 800px) {
    .dashboard-list-item {
        flex-direction: column;
    }
}
"""

if ".summary-number" not in css:
    css = css.rstrip() + "\n\n" + phase5_css.strip() + "\n"

css_path.write_text(css, encoding="utf-8")

testing_path = Path("docs/TESTING_CHECKLIST.md")
testing = testing_path.read_text(encoding="utf-8")

if "## Phase 5 Checks" not in testing:
    testing += """

## Phase 5 Checks

- [ ] Dashboard displays total assignment count
- [ ] Dashboard displays pending count
- [ ] Dashboard displays completed count
- [ ] Dashboard displays overdue count
- [ ] Dashboard displays high-priority count
- [ ] Upcoming assignments list displays
- [ ] Overdue assignments list displays
- [ ] High-priority assignments list displays
- [ ] Dashboard links open assignment details
- [ ] Urgent items are visually separated
- [ ] Project builds successfully
"""
testing_path.write_text(testing, encoding="utf-8")

devnotes_path = Path("docs/DEVELOPER_NOTES.md")
devnotes = devnotes_path.read_text(encoding="utf-8")

if "## Phase 5 Notes" not in devnotes:
    devnotes += """

## Phase 5 Notes

Phase 5 implements dashboard summary views. DashboardService calculates assignment totals, pending count, completed count, overdue count, high-priority count, upcoming assignments, overdue assignments, and high-priority assignments. Dashboard.razor displays these summaries and links users to assignment details.
"""
devnotes_path.write_text(devnotes, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")

if "## Phase 5 Dashboard" not in readme:
    readme += """

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
"""
readme_path.write_text(readme, encoding="utf-8")

print("Phase 5 patch applied successfully.")

