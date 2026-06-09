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

write("src/StudyTrack/Services/StudySessionService.cs", """
using Microsoft.EntityFrameworkCore;
using StudyTrack.Data;
using StudyTrack.Models;

namespace StudyTrack.Services;

public class StudySessionService
{
    private readonly StudyTrackDbContext _context;

    public StudySessionService(StudyTrackDbContext context)
    {
        _context = context;
    }

    public async Task[[LT]]List[[LT]]StudySession[[GT]][[GT]] GetStudySessionsAsync()
    {
        return await _context.StudySessions
            .Include(session [[ARROW]] session.AssignmentTask)
                .ThenInclude(assignment [[ARROW]] assignment!.Course)
            .OrderBy(session [[ARROW]] session.PlannedDate)
            .ToListAsync();
    }

    public async Task[[LT]]StudySession?[[GT]] GetStudySessionByIdAsync(int id)
    {
        return await _context.StudySessions
            .Include(session [[ARROW]] session.AssignmentTask)
                .ThenInclude(assignment [[ARROW]] assignment!.Course)
            .FirstOrDefaultAsync(session [[ARROW]] session.Id == id);
    }

    public async Task[[LT]]StudySession[[GT]] CreateStudySessionAsync(StudySession session)
    {
        session.CreatedAt = DateTime.UtcNow;

        _context.StudySessions.Add(session);
        await _context.SaveChangesAsync();

        return session;
    }

    public async Task[[LT]]bool[[GT]] MarkCompletedAsync(int id)
    {
        var existingSession = await _context.StudySessions.FindAsync(id);

        if (existingSession is null)
        {
            return false;
        }

        existingSession.IsCompleted = true;
        await _context.SaveChangesAsync();

        return true;
    }

    public async Task[[LT]]bool[[GT]] ReopenAsync(int id)
    {
        var existingSession = await _context.StudySessions.FindAsync(id);

        if (existingSession is null)
        {
            return false;
        }

        existingSession.IsCompleted = false;
        await _context.SaveChangesAsync();

        return true;
    }

    public async Task[[LT]]bool[[GT]] DeleteStudySessionAsync(int id)
    {
        var existingSession = await _context.StudySessions.FindAsync(id);

        if (existingSession is null)
        {
            return false;
        }

        _context.StudySessions.Remove(existingSession);
        await _context.SaveChangesAsync();

        return true;
    }
}
""")

write("src/StudyTrack/Components/Pages/StudySessions.razor", """
@page "/study-sessions"
@rendermode InteractiveServer
@using System.ComponentModel.DataAnnotations
@using StudyTrack.Models
@using StudyTrack.Services
@inject StudySessionService StudySessionService
@inject AssignmentService AssignmentService

[[LT]]PageTitle[[GT]]Study Sessions[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]Study Session Planning[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Plan focused study time by linking study sessions to assignments.
[[LT]]/p[[GT]]

@if (!string.IsNullOrWhiteSpace(successMessage))
{
    [[LT]]div class="alert alert-success" role="alert"[[GT]]@successMessage[[LT]]/div[[GT]]
}

@if (!string.IsNullOrWhiteSpace(errorMessage))
{
    [[LT]]div class="alert alert-danger" role="alert"[[GT]]@errorMessage[[LT]]/div[[GT]]
}

@if (assignments.Count == 0 && !isLoading)
{
    [[LT]]div class="alert alert-warning" role="alert"[[GT]]
        Create at least one assignment before planning study sessions.
    [[LT]]/div[[GT]]
}

[[LT]]section class="crud-panel study-session-form-panel"[[GT]]
    [[LT]]h2[[GT]]Add Study Session[[LT]]/h2[[GT]]

    [[LT]]EditForm Model="sessionForm" OnValidSubmit="CreateSessionAsync"[[GT]]
        [[LT]]DataAnnotationsValidator /[[GT]]
        [[LT]]ValidationSummary /[[GT]]

        [[LT]]div class="form-grid"[[GT]]
            [[LT]]div class="form-field form-field-wide"[[GT]]
                [[LT]]label for="session-assignment"[[GT]]Assignment[[LT]]/label[[GT]]
                [[LT]]InputSelect id="session-assignment" class="form-control" @bind-Value="sessionForm.AssignmentTaskId"[[GT]]
                    [[LT]]option value="0"[[GT]]Select an assignment[[LT]]/option[[GT]]
                    @foreach (var assignment in assignments)
                    {
                        [[LT]]option value="@assignment.Id"[[GT]]@assignment.Title (@(assignment.Course?.Name ?? "No course"))[[LT]]/option[[GT]]
                    }
                [[LT]]/InputSelect[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] sessionForm.AssignmentTaskId)" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="planned-date"[[GT]]Planned Date[[LT]]/label[[GT]]
                [[LT]]InputDate id="planned-date" class="form-control" @bind-Value="sessionForm.PlannedDate" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] sessionForm.PlannedDate)" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="duration-minutes"[[GT]]Duration Minutes[[LT]]/label[[GT]]
                [[LT]]InputNumber id="duration-minutes" class="form-control" @bind-Value="sessionForm.DurationMinutes" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] sessionForm.DurationMinutes)" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field form-field-wide"[[GT]]
                [[LT]]label for="session-notes"[[GT]]Notes[[LT]]/label[[GT]]
                [[LT]]InputTextArea id="session-notes" class="form-control" @bind-Value="sessionForm.Notes" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] sessionForm.Notes)" /[[GT]]
            [[LT]]/div[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="button-row"[[GT]]
            [[LT]]button type="submit" class="btn btn-primary" disabled="@(assignments.Count == 0)"[[GT]]Create Study Session[[LT]]/button[[GT]]
        [[LT]]/div[[GT]]
    [[LT]]/EditForm[[GT]]
[[LT]]/section[[GT]]

[[LT]]section class="crud-panel"[[GT]]
    [[LT]]div class="section-header"[[GT]]
        [[LT]]h2[[GT]]Planned Study Sessions[[LT]]/h2[[GT]]
        [[LT]]span class="record-count"[[GT]]@studySessions.Count session(s)[[LT]]/span[[GT]]
    [[LT]]/div[[GT]]

    @if (isLoading)
    {
        [[LT]]p[[GT]][[LT]]em[[GT]]Loading study sessions...[[LT]]/em[[GT]][[LT]]/p[[GT]]
    }
    else if (studySessions.Count == 0)
    {
        [[LT]]div class="empty-state"[[GT]]
            No study sessions exist yet. Use the form above to plan the first session.
        [[LT]]/div[[GT]]
    }
    else
    {
        [[LT]]table class="table table-striped study-session-table"[[GT]]
            [[LT]]thead[[GT]]
                [[LT]]tr[[GT]]
                    [[LT]]th[[GT]]Assignment[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Course[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Planned Date[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Duration[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Status[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Notes[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Actions[[LT]]/th[[GT]]
                [[LT]]/tr[[GT]]
            [[LT]]/thead[[GT]]
            [[LT]]tbody[[GT]]
                @foreach (var session in studySessions)
                {
                    [[LT]]tr[[GT]]
                        [[LT]]td[[GT]]
                            [[LT]]a href="@($"/assignments/{session.AssignmentTaskId}")"[[GT]]
                                @(session.AssignmentTask?.Title ?? "Assignment not found")
                            [[LT]]/a[[GT]]
                        [[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@(session.AssignmentTask?.Course?.Name ?? "No course")[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@session.PlannedDate.ToString("yyyy-MM-dd")[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@session.DurationMinutes minutes[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]
                            @if (session.IsCompleted)
                            {
                                [[LT]]span class="badge badge-status badge-completed"[[GT]]Completed[[LT]]/span[[GT]]
                            }
                            else
                            {
                                [[LT]]span class="badge badge-status badge-pending"[[GT]]Planned[[LT]]/span[[GT]]
                            }
                        [[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@(string.IsNullOrWhiteSpace(session.Notes) ? "—" : session.Notes)[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]
                            @if (session.IsCompleted)
                            {
                                [[LT]]button type="button" class="btn btn-sm btn-outline-warning" @onclick="() [[ARROW]] ReopenSessionAsync(session.Id)"[[GT]]Reopen[[LT]]/button[[GT]]
                            }
                            else
                            {
                                [[LT]]button type="button" class="btn btn-sm btn-outline-success" @onclick="() [[ARROW]] MarkSessionCompletedAsync(session.Id)"[[GT]]Complete[[LT]]/button[[GT]]
                            }

                            [[LT]]button type="button" class="btn btn-sm btn-outline-danger" @onclick="() [[ARROW]] DeleteSessionAsync(session.Id)"[[GT]]Delete[[LT]]/button[[GT]]
                        [[LT]]/td[[GT]]
                    [[LT]]/tr[[GT]]
                }
            [[LT]]/tbody[[GT]]
        [[LT]]/table[[GT]]
    }
[[LT]]/section[[GT]]

@code {
    private List[[LT]]StudySession[[GT]] studySessions = new();
    private List[[LT]]AssignmentTask[[GT]] assignments = new();
    private StudySessionForm sessionForm = new();
    private bool isLoading = true;
    private string? successMessage;
    private string? errorMessage;

    protected override async Task OnInitializedAsync()
    {
        await LoadDataAsync();
    }

    private async Task LoadDataAsync()
    {
        isLoading = true;

        assignments = await AssignmentService.GetAssignmentsAsync();
        studySessions = await StudySessionService.GetStudySessionsAsync();

        if (sessionForm.AssignmentTaskId == 0 && assignments.Count > 0)
        {
            sessionForm.AssignmentTaskId = assignments[0].Id;
        }

        isLoading = false;
    }

    private async Task CreateSessionAsync()
    {
        ClearMessages();

        var session = new StudySession
        {
            AssignmentTaskId = sessionForm.AssignmentTaskId,
            PlannedDate = sessionForm.PlannedDate.Date,
            DurationMinutes = sessionForm.DurationMinutes,
            Notes = string.IsNullOrWhiteSpace(sessionForm.Notes) ? null : sessionForm.Notes.Trim(),
            IsCompleted = false
        };

        await StudySessionService.CreateStudySessionAsync(session);

        successMessage = "Study session created successfully.";
        ResetForm();

        await LoadDataAsync();
    }

    private async Task MarkSessionCompletedAsync(int id)
    {
        ClearMessages();

        var completed = await StudySessionService.MarkCompletedAsync(id);

        successMessage = completed ? "Study session marked as completed." : null;
        errorMessage = completed ? null : "The selected study session could not be found.";

        await LoadDataAsync();
    }

    private async Task ReopenSessionAsync(int id)
    {
        ClearMessages();

        var reopened = await StudySessionService.ReopenAsync(id);

        successMessage = reopened ? "Study session reopened successfully." : null;
        errorMessage = reopened ? null : "The selected study session could not be found.";

        await LoadDataAsync();
    }

    private async Task DeleteSessionAsync(int id)
    {
        ClearMessages();

        var deleted = await StudySessionService.DeleteStudySessionAsync(id);

        successMessage = deleted ? "Study session deleted successfully." : null;
        errorMessage = deleted ? null : "The selected study session could not be found.";

        await LoadDataAsync();
    }

    private void ResetForm()
    {
        sessionForm = new StudySessionForm
        {
            AssignmentTaskId = assignments.FirstOrDefault()?.Id ?? 0
        };
    }

    private void ClearMessages()
    {
        successMessage = null;
        errorMessage = null;
    }

    private sealed class StudySessionForm
    {
        [Range(1, int.MaxValue, ErrorMessage = "An assignment must be selected.")]
        public int AssignmentTaskId { get; set; }

        [Required]
        public DateTime PlannedDate { get; set; } = DateTime.Today.AddDays(1);

        [Range(1, 600, ErrorMessage = "Duration must be between 1 and 600 minutes.")]
        public int DurationMinutes { get; set; } = 60;

        [StringLength(500, ErrorMessage = "Notes must be 500 characters or fewer.")]
        public string? Notes { get; set; }
    }
}
""")

program_path = Path("src/StudyTrack/Program.cs")
program = program_path.read_text(encoding="utf-8")

if "builder.Services.AddScoped<StudySessionService>();" not in program:
    if "builder.Services.AddScoped<DashboardService>();" in program:
        program = program.replace(
            "builder.Services.AddScoped<DashboardService>();",
            "builder.Services.AddScoped<DashboardService>();\nbuilder.Services.AddScoped<StudySessionService>();"
        )
    else:
        program += "\nbuilder.Services.AddScoped<StudySessionService>();\n"

program_path.write_text(program, encoding="utf-8")

css_path = Path("src/StudyTrack/wwwroot/css/app.css")
css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

phase7_css = """
.study-session-form-panel {
    border-left: 6px solid #6f42c1;
}

.study-session-table td {
    vertical-align: middle;
}

.study-session-table .btn {
    margin: 0.15rem;
}
"""

if ".study-session-form-panel" not in css:
    css = css.rstrip() + "\n\n" + phase7_css.strip() + "\n"

css_path.write_text(css, encoding="utf-8")

user_guide_path = Path("docs/USER_GUIDE.md")
user_guide = user_guide_path.read_text(encoding="utf-8")

if "## Study Session Planning" not in user_guide:
    user_guide += """

## Study Session Planning

Study sessions help students plan focused work time for assignments.

Users can:

- Select an assignment
- Choose a planned study date
- Enter a duration in minutes
- Add notes
- Create a study session
- Mark a study session complete
- Reopen a completed study session
- Delete a study session
"""
user_guide_path.write_text(user_guide, encoding="utf-8")

testing_path = Path("docs/TESTING_CHECKLIST.md")
testing = testing_path.read_text(encoding="utf-8")

if "## Phase 7 Checks" not in testing:
    testing += """

## Phase 7 Checks

- [ ] Study Sessions page opens
- [ ] Study session create form appears
- [ ] Assignment dropdown displays assignments
- [ ] Planned date field appears
- [ ] Duration field validates values between 1 and 600
- [ ] Notes field appears
- [ ] New study session can be created
- [ ] Study sessions display in a list
- [ ] Study sessions link back to assignment details
- [ ] Study session can be marked complete
- [ ] Completed study session can be reopened
- [ ] Study session can be deleted
- [ ] Project builds successfully
"""
testing_path.write_text(testing, encoding="utf-8")

devnotes_path = Path("docs/DEVELOPER_NOTES.md")
devnotes = devnotes_path.read_text(encoding="utf-8")

if "## Phase 7 Notes" not in devnotes:
    devnotes += """

## Phase 7 Notes

Phase 7 implements study session planning. StudySessionService handles create, list, complete, reopen, and delete operations. StudySessions.razor lets users link sessions to assignments, set planned dates, add durations, add notes, and track completion.
"""
devnotes_path.write_text(devnotes, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")

if "## Phase 7 Study Session Planning" not in readme:
    readme += """

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
"""
readme_path.write_text(readme, encoding="utf-8")

print("Phase 7 patch applied successfully.")
