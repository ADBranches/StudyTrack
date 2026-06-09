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

write("src/StudyTrack/Services/AssignmentService.cs", """
using Microsoft.EntityFrameworkCore;
using StudyTrack.Data;
using StudyTrack.Models;

namespace StudyTrack.Services;

public class AssignmentService
{
    private readonly StudyTrackDbContext _context;

    public AssignmentService(StudyTrackDbContext context)
    {
        _context = context;
    }

    public async Task[[LT]]List[[LT]]AssignmentTask[[GT]][[GT]] GetAssignmentsAsync(
        int? courseId = null,
        AssignmentStatus? status = null,
        AssignmentPriority? priority = null,
        string sortBy = "due-date")
    {
        IQueryable[[LT]]AssignmentTask[[GT]] query = _context.AssignmentTasks
            .Include(assignment [[ARROW]] assignment.Course);

        if (courseId.HasValue && courseId.Value > 0)
        {
            query = query.Where(assignment [[ARROW]] assignment.CourseId == courseId.Value);
        }

        if (status.HasValue)
        {
            query = query.Where(assignment [[ARROW]] assignment.Status == status.Value);
        }

        if (priority.HasValue)
        {
            query = query.Where(assignment [[ARROW]] assignment.Priority == priority.Value);
        }

        query = sortBy switch
        {
            "due-date-desc" => query.OrderByDescending(assignment [[ARROW]] assignment.DueDate),
            "priority" => query.OrderByDescending(assignment [[ARROW]] assignment.Priority).ThenBy(assignment [[ARROW]] assignment.DueDate),
            "course" => query.OrderBy(assignment [[ARROW]] assignment.Course!.Name).ThenBy(assignment [[ARROW]] assignment.DueDate),
            "status" => query.OrderBy(assignment [[ARROW]] assignment.Status).ThenBy(assignment [[ARROW]] assignment.DueDate),
            _ => query.OrderBy(assignment [[ARROW]] assignment.DueDate)
        };

        return await query.ToListAsync();
    }

    public async Task[[LT]]AssignmentTask?[[GT]] GetAssignmentByIdAsync(int id)
    {
        return await _context.AssignmentTasks
            .Include(assignment [[ARROW]] assignment.Course)
            .Include(assignment [[ARROW]] assignment.StudySessions.OrderBy(session [[ARROW]] session.PlannedDate))
            .FirstOrDefaultAsync(assignment [[ARROW]] assignment.Id == id);
    }

    public async Task[[LT]]AssignmentTask[[GT]] CreateAssignmentAsync(AssignmentTask assignment)
    {
        assignment.CreatedAt = DateTime.UtcNow;
        assignment.UpdatedAt = DateTime.UtcNow;

        if (assignment.Status == AssignmentStatus.Completed && assignment.CompletedAt is null)
        {
            assignment.CompletedAt = DateTime.UtcNow;
        }

        _context.AssignmentTasks.Add(assignment);
        await _context.SaveChangesAsync();

        return assignment;
    }

    public async Task[[LT]]bool[[GT]] UpdateAssignmentAsync(AssignmentTask updatedAssignment)
    {
        var existingAssignment = await _context.AssignmentTasks.FindAsync(updatedAssignment.Id);

        if (existingAssignment is null)
        {
            return false;
        }

        existingAssignment.Title = updatedAssignment.Title;
        existingAssignment.Description = updatedAssignment.Description;
        existingAssignment.DueDate = updatedAssignment.DueDate;
        existingAssignment.Priority = updatedAssignment.Priority;
        existingAssignment.Status = updatedAssignment.Status;
        existingAssignment.CourseId = updatedAssignment.CourseId;
        existingAssignment.UpdatedAt = DateTime.UtcNow;

        if (updatedAssignment.Status == AssignmentStatus.Completed)
        {
            existingAssignment.CompletedAt ??= DateTime.UtcNow;
        }
        else
        {
            existingAssignment.CompletedAt = null;
        }

        await _context.SaveChangesAsync();
        return true;
    }

    public async Task[[LT]]bool[[GT]] DeleteAssignmentAsync(int id)
    {
        var existingAssignment = await _context.AssignmentTasks.FindAsync(id);

        if (existingAssignment is null)
        {
            return false;
        }

        _context.AssignmentTasks.Remove(existingAssignment);
        await _context.SaveChangesAsync();

        return true;
    }

    public async Task[[LT]]bool[[GT]] MarkCompletedAsync(int id)
    {
        var existingAssignment = await _context.AssignmentTasks.FindAsync(id);

        if (existingAssignment is null)
        {
            return false;
        }

        existingAssignment.Status = AssignmentStatus.Completed;
        existingAssignment.CompletedAt = DateTime.UtcNow;
        existingAssignment.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        return true;
    }

    public async Task[[LT]]bool[[GT]] ReopenAssignmentAsync(int id)
    {
        var existingAssignment = await _context.AssignmentTasks.FindAsync(id);

        if (existingAssignment is null)
        {
            return false;
        }

        existingAssignment.Status = existingAssignment.DueDate.Date < DateTime.Today
            ? AssignmentStatus.Overdue
            : AssignmentStatus.Pending;

        existingAssignment.CompletedAt = null;
        existingAssignment.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        return true;
    }
}
""")

write("src/StudyTrack/Components/Pages/Assignments.razor", """
@page "/assignments"
@rendermode InteractiveServer
@using System.ComponentModel.DataAnnotations
@using StudyTrack.Models
@using StudyTrack.Services
@using StudyTrack.Components.Shared
@inject AssignmentService AssignmentService
@inject CourseService CourseService

[[LT]]PageTitle[[GT]]Assignments[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]Assignment Management[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Create, view, update, delete, complete, reopen, filter, and sort assignments.
[[LT]]/p[[GT]]

@if (!string.IsNullOrWhiteSpace(successMessage))
{
    [[LT]]div class="alert alert-success" role="alert"[[GT]]@successMessage[[LT]]/div[[GT]]
}

@if (!string.IsNullOrWhiteSpace(errorMessage))
{
    [[LT]]div class="alert alert-danger" role="alert"[[GT]]@errorMessage[[LT]]/div[[GT]]
}

@if (courses.Count == 0 && !isLoading)
{
    [[LT]]div class="alert alert-warning" role="alert"[[GT]]
        Create at least one course before adding assignments.
    [[LT]]/div[[GT]]
}

[[LT]]section class="crud-panel filter-panel"[[GT]]
    [[LT]]div class="section-header"[[GT]]
        [[LT]]h2[[GT]]Filter and Sort Assignments[[LT]]/h2[[GT]]
        [[LT]]span class="record-count"[[GT]]@ActiveFilterText[[LT]]/span[[GT]]
    [[LT]]/div[[GT]]

    [[LT]]div class="form-grid"[[GT]]
        [[LT]]div class="form-field"[[GT]]
            [[LT]]label for="filter-course"[[GT]]Course[[LT]]/label[[GT]]
            [[LT]]select id="filter-course" class="form-control" @bind="selectedCourseId"[[GT]]
                [[LT]]option value="0"[[GT]]All courses[[LT]]/option[[GT]]
                @foreach (var course in courses)
                {
                    [[LT]]option value="@course.Id"[[GT]]@course.Name[[LT]]/option[[GT]]
                }
            [[LT]]/select[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="form-field"[[GT]]
            [[LT]]label for="filter-status"[[GT]]Status[[LT]]/label[[GT]]
            [[LT]]select id="filter-status" class="form-control" @bind="selectedStatus"[[GT]]
                [[LT]]option value=""[[GT]]All statuses[[LT]]/option[[GT]]
                [[LT]]option value="Pending"[[GT]]Pending[[LT]]/option[[GT]]
                [[LT]]option value="InProgress"[[GT]]In Progress[[LT]]/option[[GT]]
                [[LT]]option value="Completed"[[GT]]Completed[[LT]]/option[[GT]]
                [[LT]]option value="Overdue"[[GT]]Overdue[[LT]]/option[[GT]]
            [[LT]]/select[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="form-field"[[GT]]
            [[LT]]label for="filter-priority"[[GT]]Priority[[LT]]/label[[GT]]
            [[LT]]select id="filter-priority" class="form-control" @bind="selectedPriority"[[GT]]
                [[LT]]option value=""[[GT]]All priorities[[LT]]/option[[GT]]
                [[LT]]option value="Low"[[GT]]Low[[LT]]/option[[GT]]
                [[LT]]option value="Medium"[[GT]]Medium[[LT]]/option[[GT]]
                [[LT]]option value="High"[[GT]]High[[LT]]/option[[GT]]
            [[LT]]/select[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="form-field"[[GT]]
            [[LT]]label for="sort-by"[[GT]]Sort By[[LT]]/label[[GT]]
            [[LT]]select id="sort-by" class="form-control" @bind="selectedSort"[[GT]]
                [[LT]]option value="due-date"[[GT]]Due date, earliest first[[LT]]/option[[GT]]
                [[LT]]option value="due-date-desc"[[GT]]Due date, latest first[[LT]]/option[[GT]]
                [[LT]]option value="priority"[[GT]]Priority, high first[[LT]]/option[[GT]]
                [[LT]]option value="course"[[GT]]Course name[[LT]]/option[[GT]]
                [[LT]]option value="status"[[GT]]Status[[LT]]/option[[GT]]
            [[LT]]/select[[GT]]
        [[LT]]/div[[GT]]
    [[LT]]/div[[GT]]

    [[LT]]div class="button-row"[[GT]]
        [[LT]]button type="button" class="btn btn-primary" @onclick="ApplyFiltersAsync"[[GT]]Apply Filters[[LT]]/button[[GT]]
        [[LT]]button type="button" class="btn btn-secondary" @onclick="ClearFiltersAsync"[[GT]]Clear Filters[[LT]]/button[[GT]]
    [[LT]]/div[[GT]]
[[LT]]/section[[GT]]

[[LT]]section class="crud-panel"[[GT]]
    [[LT]]h2[[GT]]@(editingAssignmentId is null ? "Add Assignment" : "Edit Assignment")[[LT]]/h2[[GT]]

    [[LT]]EditForm Model="assignmentForm" OnValidSubmit="SaveAssignmentAsync"[[GT]]
        [[LT]]DataAnnotationsValidator /[[GT]]
        [[LT]]ValidationSummary /[[GT]]

        [[LT]]div class="form-grid"[[GT]]
            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="assignment-title"[[GT]]Title[[LT]]/label[[GT]]
                [[LT]]InputText id="assignment-title" class="form-control" @bind-Value="assignmentForm.Title" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] assignmentForm.Title)" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="assignment-course"[[GT]]Course[[LT]]/label[[GT]]
                [[LT]]InputSelect id="assignment-course" class="form-control" @bind-Value="assignmentForm.CourseId"[[GT]]
                    [[LT]]option value="0"[[GT]]Select a course[[LT]]/option[[GT]]
                    @foreach (var course in courses)
                    {
                        [[LT]]option value="@course.Id"[[GT]]@course.Name[[LT]]/option[[GT]]
                    }
                [[LT]]/InputSelect[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] assignmentForm.CourseId)" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="assignment-due-date"[[GT]]Due Date[[LT]]/label[[GT]]
                [[LT]]InputDate id="assignment-due-date" class="form-control" @bind-Value="assignmentForm.DueDate" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="assignment-priority"[[GT]]Priority[[LT]]/label[[GT]]
                [[LT]]InputSelect id="assignment-priority" class="form-control" @bind-Value="assignmentForm.Priority"[[GT]]
                    [[LT]]option value="@AssignmentPriority.Low"[[GT]]Low[[LT]]/option[[GT]]
                    [[LT]]option value="@AssignmentPriority.Medium"[[GT]]Medium[[LT]]/option[[GT]]
                    [[LT]]option value="@AssignmentPriority.High"[[GT]]High[[LT]]/option[[GT]]
                [[LT]]/InputSelect[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="assignment-status"[[GT]]Status[[LT]]/label[[GT]]
                [[LT]]InputSelect id="assignment-status" class="form-control" @bind-Value="assignmentForm.Status"[[GT]]
                    [[LT]]option value="@AssignmentStatus.Pending"[[GT]]Pending[[LT]]/option[[GT]]
                    [[LT]]option value="@AssignmentStatus.InProgress"[[GT]]In Progress[[LT]]/option[[GT]]
                    [[LT]]option value="@AssignmentStatus.Completed"[[GT]]Completed[[LT]]/option[[GT]]
                    [[LT]]option value="@AssignmentStatus.Overdue"[[GT]]Overdue[[LT]]/option[[GT]]
                [[LT]]/InputSelect[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field form-field-wide"[[GT]]
                [[LT]]label for="assignment-description"[[GT]]Description[[LT]]/label[[GT]]
                [[LT]]InputTextArea id="assignment-description" class="form-control" @bind-Value="assignmentForm.Description" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] assignmentForm.Description)" /[[GT]]
            [[LT]]/div[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="button-row"[[GT]]
            [[LT]]button type="submit" class="btn btn-primary" disabled="@(courses.Count == 0)"[[GT]]
                @(editingAssignmentId is null ? "Create Assignment" : "Save Changes")
            [[LT]]/button[[GT]]

            @if (editingAssignmentId is not null)
            {
                [[LT]]button type="button" class="btn btn-secondary" @onclick="CancelEdit"[[GT]]Cancel[[LT]]/button[[GT]]
            }
        [[LT]]/div[[GT]]
    [[LT]]/EditForm[[GT]]
[[LT]]/section[[GT]]

[[LT]]section class="crud-panel"[[GT]]
    [[LT]]div class="section-header"[[GT]]
        [[LT]]h2[[GT]]Assignments[[LT]]/h2[[GT]]
        [[LT]]span class="record-count"[[GT]]@assignments.Count assignment(s)[[LT]]/span[[GT]]
    [[LT]]/div[[GT]]

    @if (isLoading)
    {
        [[LT]]p[[GT]][[LT]]em[[GT]]Loading assignments...[[LT]]/em[[GT]][[LT]]/p[[GT]]
    }
    else if (assignments.Count == 0)
    {
        [[LT]]div class="empty-state"[[GT]]
            No assignments match the selected filters.
        [[LT]]/div[[GT]]
    }
    else
    {
        [[LT]]table class="table table-striped assignment-table"[[GT]]
            [[LT]]thead[[GT]]
                [[LT]]tr[[GT]]
                    [[LT]]th[[GT]]Title[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Course[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Due Date[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Priority[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Status[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Actions[[LT]]/th[[GT]]
                [[LT]]/tr[[GT]]
            [[LT]]/thead[[GT]]
            [[LT]]tbody[[GT]]
                @foreach (var assignment in assignments)
                {
                    [[LT]]tr[[GT]]
                        [[LT]]td[[GT]]
                            [[LT]]strong[[GT]]@assignment.Title[[LT]]/strong[[GT]]
                            @if (!string.IsNullOrWhiteSpace(assignment.Description))
                            {
                                [[LT]]div class="muted-text"[[GT]]@assignment.Description[[LT]]/div[[GT]]
                            }
                        [[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@(assignment.Course?.Name ?? "No course")[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@assignment.DueDate.ToString("yyyy-MM-dd")[[LT]]/td[[GT]]
                        [[LT]]td[[GT]][[LT]]PriorityBadge Priority="assignment.Priority" /[[GT]][[LT]]/td[[GT]]
                        [[LT]]td[[GT]][[LT]]StatusBadge Status="assignment.Status" /[[GT]][[LT]]/td[[GT]]
                        [[LT]]td[[GT]]
                            [[LT]]a class="btn btn-sm btn-outline-primary" href="@($"/assignments/{assignment.Id}")"[[GT]]Details[[LT]]/a[[GT]]
                            [[LT]]button type="button" class="btn btn-sm btn-outline-secondary" @onclick="() [[ARROW]] BeginEdit(assignment)"[[GT]]Edit[[LT]]/button[[GT]]

                            @if (assignment.Status == AssignmentStatus.Completed)
                            {
                                [[LT]]button type="button" class="btn btn-sm btn-outline-warning" @onclick="() [[ARROW]] ReopenAssignmentAsync(assignment.Id)"[[GT]]Reopen[[LT]]/button[[GT]]
                            }
                            else
                            {
                                [[LT]]button type="button" class="btn btn-sm btn-outline-success" @onclick="() [[ARROW]] MarkCompletedAsync(assignment.Id)"[[GT]]Complete[[LT]]/button[[GT]]
                            }

                            [[LT]]button type="button" class="btn btn-sm btn-outline-danger" @onclick="() [[ARROW]] DeleteAssignmentAsync(assignment.Id)"[[GT]]Delete[[LT]]/button[[GT]]
                        [[LT]]/td[[GT]]
                    [[LT]]/tr[[GT]]
                }
            [[LT]]/tbody[[GT]]
        [[LT]]/table[[GT]]
    }
[[LT]]/section[[GT]]

@code {
    private List[[LT]]AssignmentTask[[GT]] assignments = new();
    private List[[LT]]Course[[GT]] courses = new();
    private AssignmentForm assignmentForm = new();
    private int? editingAssignmentId;
    private bool isLoading = true;
    private string? successMessage;
    private string? errorMessage;

    private int selectedCourseId;
    private string selectedStatus = string.Empty;
    private string selectedPriority = string.Empty;
    private string selectedSort = "due-date";

    private string ActiveFilterText =>
        selectedCourseId == 0 && string.IsNullOrWhiteSpace(selectedStatus) && string.IsNullOrWhiteSpace(selectedPriority)
            ? "No active filters"
            : "Filters active";

    protected override async Task OnInitializedAsync()
    {
        await LoadDataAsync();
    }

    private async Task LoadDataAsync()
    {
        isLoading = true;
        courses = await CourseService.GetCoursesAsync();

        if (assignmentForm.CourseId == 0 && courses.Count > 0)
        {
            assignmentForm.CourseId = courses[0].Id;
        }

        await LoadAssignmentsAsync();
        isLoading = false;
    }

    private async Task LoadAssignmentsAsync()
    {
        assignments = await AssignmentService.GetAssignmentsAsync(
            selectedCourseId > 0 ? selectedCourseId : null,
            TryParseStatus(),
            TryParsePriority(),
            selectedSort);
    }

    private AssignmentStatus? TryParseStatus()
    {
        return Enum.TryParse[[LT]]AssignmentStatus[[GT]](selectedStatus, out var parsedStatus)
            ? parsedStatus
            : null;
    }

    private AssignmentPriority? TryParsePriority()
    {
        return Enum.TryParse[[LT]]AssignmentPriority[[GT]](selectedPriority, out var parsedPriority)
            ? parsedPriority
            : null;
    }

    private async Task ApplyFiltersAsync()
    {
        ClearMessages();
        isLoading = true;
        await LoadAssignmentsAsync();
        isLoading = false;
    }

    private async Task ClearFiltersAsync()
    {
        ClearMessages();
        selectedCourseId = 0;
        selectedStatus = string.Empty;
        selectedPriority = string.Empty;
        selectedSort = "due-date";
        isLoading = true;
        await LoadAssignmentsAsync();
        isLoading = false;
    }

    private async Task SaveAssignmentAsync()
    {
        ClearMessages();

        var assignment = new AssignmentTask
        {
            Id = editingAssignmentId ?? 0,
            Title = assignmentForm.Title.Trim(),
            Description = string.IsNullOrWhiteSpace(assignmentForm.Description) ? null : assignmentForm.Description.Trim(),
            CourseId = assignmentForm.CourseId,
            DueDate = assignmentForm.DueDate.Date,
            Priority = assignmentForm.Priority,
            Status = assignmentForm.Status
        };

        if (editingAssignmentId is null)
        {
            await AssignmentService.CreateAssignmentAsync(assignment);
            successMessage = "Assignment created successfully.";
        }
        else
        {
            var updated = await AssignmentService.UpdateAssignmentAsync(assignment);

            if (!updated)
            {
                errorMessage = "The selected assignment could not be found.";
                await LoadDataAsync();
                return;
            }

            successMessage = "Assignment updated successfully.";
        }

        ResetForm();
        await LoadDataAsync();
    }

    private void BeginEdit(AssignmentTask assignment)
    {
        ClearMessages();

        editingAssignmentId = assignment.Id;
        assignmentForm = new AssignmentForm
        {
            Title = assignment.Title,
            Description = assignment.Description,
            CourseId = assignment.CourseId,
            DueDate = assignment.DueDate.Date,
            Priority = assignment.Priority,
            Status = assignment.Status
        };
    }

    private void CancelEdit()
    {
        ClearMessages();
        ResetForm();
    }

    private async Task DeleteAssignmentAsync(int id)
    {
        ClearMessages();

        var deleted = await AssignmentService.DeleteAssignmentAsync(id);

        successMessage = deleted ? "Assignment deleted successfully." : null;
        errorMessage = deleted ? null : "The selected assignment could not be found.";

        await LoadDataAsync();
    }

    private async Task MarkCompletedAsync(int id)
    {
        ClearMessages();

        var completed = await AssignmentService.MarkCompletedAsync(id);

        successMessage = completed ? "Assignment marked as completed." : null;
        errorMessage = completed ? null : "The selected assignment could not be found.";

        await LoadDataAsync();
    }

    private async Task ReopenAssignmentAsync(int id)
    {
        ClearMessages();

        var reopened = await AssignmentService.ReopenAssignmentAsync(id);

        successMessage = reopened ? "Assignment reopened successfully." : null;
        errorMessage = reopened ? null : "The selected assignment could not be found.";

        await LoadDataAsync();
    }

    private void ResetForm()
    {
        editingAssignmentId = null;
        assignmentForm = new AssignmentForm
        {
            CourseId = courses.FirstOrDefault()?.Id ?? 0
        };
    }

    private void ClearMessages()
    {
        successMessage = null;
        errorMessage = null;
    }

    private sealed class AssignmentForm
    {
        [Required(ErrorMessage = "Assignment title is required.")]
        [StringLength(120, MinimumLength = 2, ErrorMessage = "Assignment title must be between 2 and 120 characters.")]
        public string Title { get; set; } = string.Empty;

        [StringLength(500, ErrorMessage = "Assignment description must be 500 characters or fewer.")]
        public string? Description { get; set; }

        [Range(1, int.MaxValue, ErrorMessage = "A course must be selected.")]
        public int CourseId { get; set; }

        [Required]
        public DateTime DueDate { get; set; } = DateTime.Today.AddDays(7);

        public AssignmentPriority Priority { get; set; } = AssignmentPriority.Medium;

        public AssignmentStatus Status { get; set; } = AssignmentStatus.Pending;
    }
}
""")

css_path = Path("src/StudyTrack/wwwroot/css/app.css")
css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

phase6_css = """
.filter-panel {
    border-left: 6px solid #0d6efd;
}

.filter-panel .section-header {
    margin-bottom: 1rem;
}

.filter-panel select {
    min-height: 2.3rem;
}
"""

if ".filter-panel" not in css:
    css = css.rstrip() + "\n\n" + phase6_css.strip() + "\n"

css_path.write_text(css, encoding="utf-8")

testing_path = Path("docs/TESTING_CHECKLIST.md")
testing = testing_path.read_text(encoding="utf-8")

if "## Phase 6 Checks" not in testing:
    testing += """

## Phase 6 Checks

- [ ] Assignments can be filtered by course
- [ ] Assignments can be filtered by status
- [ ] Assignments can be filtered by priority
- [ ] Assignments can be sorted by due date ascending
- [ ] Assignments can be sorted by due date descending
- [ ] Assignments can be sorted by priority
- [ ] Assignments can be sorted by course
- [ ] Assignments can be sorted by status
- [ ] Filters can be cleared
- [ ] Filtered assignment results remain linked to assignment details
- [ ] Project builds successfully
"""
testing_path.write_text(testing, encoding="utf-8")

devnotes_path = Path("docs/DEVELOPER_NOTES.md")
devnotes = devnotes_path.read_text(encoding="utf-8")

if "## Phase 6 Notes" not in devnotes:
    devnotes += """

## Phase 6 Notes

Phase 6 adds filtering and sorting to assignment management. Users can filter assignments by course, status, and priority. Users can sort assignments by due date, priority, course, or status. Filters can be cleared from the assignment page.
"""
devnotes_path.write_text(devnotes, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")

if "## Phase 6 Filtering and Sorting" not in readme:
    readme += """

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
"""
readme_path.write_text(readme, encoding="utf-8")

print("Phase 6 patch applied successfully.")

