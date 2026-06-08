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

write("src/StudyTrack/Services/CourseService.cs", """
using Microsoft.EntityFrameworkCore;
using StudyTrack.Data;
using StudyTrack.Models;

namespace StudyTrack.Services;

public class CourseService
{
    private readonly StudyTrackDbContext _context;

    public CourseService(StudyTrackDbContext context)
    {
        _context = context;
    }

    public async Task[[LT]]List[[LT]]Course[[GT]][[GT]] GetCoursesAsync()
    {
        return await _context.Courses
            .Include(course [[ARROW]] course.Assignments)
            .OrderBy(course [[ARROW]] course.Name)
            .ToListAsync();
    }

    public async Task[[LT]]Course?[[GT]] GetCourseByIdAsync(int id)
    {
        return await _context.Courses
            .Include(course [[ARROW]] course.Assignments.OrderBy(assignment [[ARROW]] assignment.DueDate))
            .FirstOrDefaultAsync(course [[ARROW]] course.Id == id);
    }

    public async Task[[LT]]Course[[GT]] CreateCourseAsync(Course course)
    {
        course.CreatedAt = DateTime.UtcNow;
        course.UpdatedAt = DateTime.UtcNow;

        _context.Courses.Add(course);
        await _context.SaveChangesAsync();

        return course;
    }

    public async Task[[LT]]bool[[GT]] UpdateCourseAsync(Course updatedCourse)
    {
        var existingCourse = await _context.Courses.FindAsync(updatedCourse.Id);

        if (existingCourse is null)
        {
            return false;
        }

        existingCourse.Name = updatedCourse.Name;
        existingCourse.Code = updatedCourse.Code;
        existingCourse.Description = updatedCourse.Description;
        existingCourse.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        return true;
    }

    public async Task[[LT]]bool[[GT]] DeleteCourseAsync(int id)
    {
        var existingCourse = await _context.Courses
            .Include(course [[ARROW]] course.Assignments)
            .FirstOrDefaultAsync(course [[ARROW]] course.Id == id);

        if (existingCourse is null)
        {
            return false;
        }

        _context.Courses.Remove(existingCourse);
        await _context.SaveChangesAsync();

        return true;
    }
}
""")

write("src/StudyTrack/Components/Pages/Courses.razor", """
@page "/courses"
@rendermode InteractiveServer
@using System.ComponentModel.DataAnnotations
@using StudyTrack.Models
@using StudyTrack.Services
@inject CourseService CourseService

[[LT]]PageTitle[[GT]]Courses[[LT]]/PageTitle[[GT]]

[[LT]]h1[[GT]]Course Management[[LT]]/h1[[GT]]

[[LT]]p class="lead"[[GT]]
    Create, view, update, and delete courses. Courses organize assignments by class or subject.
[[LT]]/p[[GT]]

@if (!string.IsNullOrWhiteSpace(successMessage))
{
    [[LT]]div class="alert alert-success" role="alert"[[GT]]@successMessage[[LT]]/div[[GT]]
}

@if (!string.IsNullOrWhiteSpace(errorMessage))
{
    [[LT]]div class="alert alert-danger" role="alert"[[GT]]@errorMessage[[LT]]/div[[GT]]
}

[[LT]]section class="crud-panel"[[GT]]
    [[LT]]h2[[GT]]@(editingCourseId is null ? "Add Course" : "Edit Course")[[LT]]/h2[[GT]]

    [[LT]]EditForm Model="courseForm" OnValidSubmit="SaveCourseAsync"[[GT]]
        [[LT]]DataAnnotationsValidator /[[GT]]
        [[LT]]ValidationSummary /[[GT]]

        [[LT]]div class="form-grid"[[GT]]
            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="course-name"[[GT]]Course Name[[LT]]/label[[GT]]
                [[LT]]InputText id="course-name" class="form-control" @bind-Value="courseForm.Name" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] courseForm.Name)" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field"[[GT]]
                [[LT]]label for="course-code"[[GT]]Course Code[[LT]]/label[[GT]]
                [[LT]]InputText id="course-code" class="form-control" @bind-Value="courseForm.Code" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] courseForm.Code)" /[[GT]]
            [[LT]]/div[[GT]]

            [[LT]]div class="form-field form-field-wide"[[GT]]
                [[LT]]label for="course-description"[[GT]]Description[[LT]]/label[[GT]]
                [[LT]]InputTextArea id="course-description" class="form-control" @bind-Value="courseForm.Description" /[[GT]]
                [[LT]]ValidationMessage For="@(() [[ARROW]] courseForm.Description)" /[[GT]]
            [[LT]]/div[[GT]]
        [[LT]]/div[[GT]]

        [[LT]]div class="button-row"[[GT]]
            [[LT]]button type="submit" class="btn btn-primary"[[GT]]@(editingCourseId is null ? "Create Course" : "Save Changes")[[LT]]/button[[GT]]

            @if (editingCourseId is not null)
            {
                [[LT]]button type="button" class="btn btn-secondary" @onclick="CancelEdit"[[GT]]Cancel[[LT]]/button[[GT]]
            }
        [[LT]]/div[[GT]]
    [[LT]]/EditForm[[GT]]
[[LT]]/section[[GT]]

[[LT]]section class="crud-panel"[[GT]]
    [[LT]]div class="section-header"[[GT]]
        [[LT]]h2[[GT]]Courses[[LT]]/h2[[GT]]
        [[LT]]span class="record-count"[[GT]]@courses.Count course(s)[[LT]]/span[[GT]]
    [[LT]]/div[[GT]]

    @if (isLoading)
    {
        [[LT]]p[[GT]][[LT]]em[[GT]]Loading courses...[[LT]]/em[[GT]][[LT]]/p[[GT]]
    }
    else if (courses.Count == 0)
    {
        [[LT]]div class="empty-state"[[GT]]
            No courses exist yet. Use the form above to create the first course.
        [[LT]]/div[[GT]]
    }
    else
    {
        [[LT]]table class="table table-striped course-table"[[GT]]
            [[LT]]thead[[GT]]
                [[LT]]tr[[GT]]
                    [[LT]]th[[GT]]Name[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Code[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Assignments[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Updated[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Actions[[LT]]/th[[GT]]
                [[LT]]/tr[[GT]]
            [[LT]]/thead[[GT]]
            [[LT]]tbody[[GT]]
                @foreach (var course in courses)
                {
                    [[LT]]tr[[GT]]
                        [[LT]]td[[GT]]
                            [[LT]]strong[[GT]]@course.Name[[LT]]/strong[[GT]]
                            @if (!string.IsNullOrWhiteSpace(course.Description))
                            {
                                [[LT]]div class="muted-text"[[GT]]@course.Description[[LT]]/div[[GT]]
                            }
                        [[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@(string.IsNullOrWhiteSpace(course.Code) ? "—" : course.Code)[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@course.Assignments.Count[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@course.UpdatedAt.ToLocalTime().ToString("yyyy-MM-dd")[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]
                            [[LT]]a class="btn btn-sm btn-outline-primary" href="@($"/courses/{course.Id}")"[[GT]]Details[[LT]]/a[[GT]]
                            [[LT]]button type="button" class="btn btn-sm btn-outline-secondary" @onclick="() [[ARROW]] BeginEdit(course)"[[GT]]Edit[[LT]]/button[[GT]]
                            [[LT]]button type="button" class="btn btn-sm btn-outline-danger" @onclick="() [[ARROW]] DeleteCourseAsync(course.Id)"[[GT]]Delete[[LT]]/button[[GT]]
                        [[LT]]/td[[GT]]
                    [[LT]]/tr[[GT]]
                }
            [[LT]]/tbody[[GT]]
        [[LT]]/table[[GT]]
    }
[[LT]]/section[[GT]]

@code {
    private List[[LT]]Course[[GT]] courses = new();
    private CourseForm courseForm = new();
    private int? editingCourseId;
    private bool isLoading = true;
    private string? successMessage;
    private string? errorMessage;

    protected override async Task OnInitializedAsync()
    {
        await LoadCoursesAsync();
    }

    private async Task LoadCoursesAsync()
    {
        isLoading = true;
        courses = await CourseService.GetCoursesAsync();
        isLoading = false;
    }

    private async Task SaveCourseAsync()
    {
        ClearMessages();

        var course = new Course
        {
            Id = editingCourseId ?? 0,
            Name = courseForm.Name.Trim(),
            Code = string.IsNullOrWhiteSpace(courseForm.Code) ? null : courseForm.Code.Trim(),
            Description = string.IsNullOrWhiteSpace(courseForm.Description) ? null : courseForm.Description.Trim()
        };

        if (editingCourseId is null)
        {
            await CourseService.CreateCourseAsync(course);
            successMessage = "Course created successfully.";
        }
        else
        {
            var updated = await CourseService.UpdateCourseAsync(course);

            if (!updated)
            {
                errorMessage = "The selected course could not be found.";
                await LoadCoursesAsync();
                return;
            }

            successMessage = "Course updated successfully.";
        }

        courseForm = new CourseForm();
        editingCourseId = null;
        await LoadCoursesAsync();
    }

    private void BeginEdit(Course course)
    {
        ClearMessages();

        editingCourseId = course.Id;
        courseForm = new CourseForm
        {
            Name = course.Name,
            Code = course.Code,
            Description = course.Description
        };
    }

    private void CancelEdit()
    {
        ClearMessages();

        editingCourseId = null;
        courseForm = new CourseForm();
    }

    private async Task DeleteCourseAsync(int id)
    {
        ClearMessages();

        var deleted = await CourseService.DeleteCourseAsync(id);

        if (deleted)
        {
            successMessage = "Course deleted successfully.";
        }
        else
        {
            errorMessage = "The selected course could not be found.";
        }

        await LoadCoursesAsync();
    }

    private void ClearMessages()
    {
        successMessage = null;
        errorMessage = null;
    }

    private sealed class CourseForm
    {
        [Required(ErrorMessage = "Course name is required.")]
        [StringLength(80, MinimumLength = 2, ErrorMessage = "Course name must be between 2 and 80 characters.")]
        public string Name { get; set; } = string.Empty;

        [StringLength(20, ErrorMessage = "Course code must be 20 characters or fewer.")]
        public string? Code { get; set; }

        [StringLength(250, ErrorMessage = "Course description must be 250 characters or fewer.")]
        public string? Description { get; set; }
    }
}
""")

write("src/StudyTrack/Components/Pages/CourseDetails.razor", """
@page "/courses/{CourseId:int}"
@using StudyTrack.Models
@using StudyTrack.Services
@inject CourseService CourseService

[[LT]]PageTitle[[GT]]Course Details[[LT]]/PageTitle[[GT]]

@if (isLoading)
{
    [[LT]]p[[GT]][[LT]]em[[GT]]Loading course details...[[LT]]/em[[GT]][[LT]]/p[[GT]]
}
else if (course is null)
{
    [[LT]]h1[[GT]]Course Not Found[[LT]]/h1[[GT]]
    [[LT]]div class="alert alert-warning" role="alert"[[GT]]
        The requested course could not be found. It may have been deleted.
    [[LT]]/div[[GT]]
    [[LT]]a class="btn btn-primary" href="/courses"[[GT]]Back to Courses[[LT]]/a[[GT]]
}
else
{
    [[LT]]h1[[GT]]@course.Name[[LT]]/h1[[GT]]

    [[LT]]div class="details-panel"[[GT]]
        [[LT]]p[[GT]][[LT]]strong[[GT]]Code:[[LT]]/strong[[GT]] @(string.IsNullOrWhiteSpace(course.Code) ? "—" : course.Code)[[LT]]/p[[GT]]
        [[LT]]p[[GT]][[LT]]strong[[GT]]Description:[[LT]]/strong[[GT]] @(string.IsNullOrWhiteSpace(course.Description) ? "No description provided." : course.Description)[[LT]]/p[[GT]]
        [[LT]]p[[GT]][[LT]]strong[[GT]]Created:[[LT]]/strong[[GT]] @course.CreatedAt.ToLocalTime().ToString("yyyy-MM-dd HH:mm")[[LT]]/p[[GT]]
        [[LT]]p[[GT]][[LT]]strong[[GT]]Updated:[[LT]]/strong[[GT]] @course.UpdatedAt.ToLocalTime().ToString("yyyy-MM-dd HH:mm")[[LT]]/p[[GT]]
    [[LT]]/div[[GT]]

    [[LT]]h2[[GT]]Connected Assignments[[LT]]/h2[[GT]]

    @if (course.Assignments.Count == 0)
    {
        [[LT]]div class="empty-state"[[GT]]
            No assignments are currently connected to this course.
        [[LT]]/div[[GT]]
    }
    else
    {
        [[LT]]table class="table table-striped"[[GT]]
            [[LT]]thead[[GT]]
                [[LT]]tr[[GT]]
                    [[LT]]th[[GT]]Assignment[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Due Date[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Priority[[LT]]/th[[GT]]
                    [[LT]]th[[GT]]Status[[LT]]/th[[GT]]
                [[LT]]/tr[[GT]]
            [[LT]]/thead[[GT]]
            [[LT]]tbody[[GT]]
                @foreach (var assignment in course.Assignments)
                {
                    [[LT]]tr[[GT]]
                        [[LT]]td[[GT]]@assignment.Title[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@assignment.DueDate.ToString("yyyy-MM-dd")[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@assignment.Priority[[LT]]/td[[GT]]
                        [[LT]]td[[GT]]@assignment.Status[[LT]]/td[[GT]]
                    [[LT]]/tr[[GT]]
                }
            [[LT]]/tbody[[GT]]
        [[LT]]/table[[GT]]
    }

    [[LT]]a class="btn btn-primary" href="/courses"[[GT]]Back to Courses[[LT]]/a[[GT]]
}

@code {
    [Parameter]
    public int CourseId { get; set; }

    private Course? course;
    private bool isLoading = true;

    protected override async Task OnParametersSetAsync()
    {
        isLoading = true;
        course = await CourseService.GetCourseByIdAsync(CourseId);
        isLoading = false;
    }
}
""")

# Register service in Program.cs
program_path = Path("src/StudyTrack/Program.cs")
program = program_path.read_text(encoding="utf-8")

if "using StudyTrack.Services;" not in program:
    program = program.replace("using StudyTrack.Data;", "using StudyTrack.Data;\nusing StudyTrack.Services;")

if "builder.Services.AddScoped[[LT]]CourseService[[GT]]();" not in program and "builder.Services.AddScoped<CourseService>();" not in program:
    marker = 'builder.Services.AddDbContext<StudyTrackDbContext>(options =>\n    options.UseSqlite(builder.Configuration.GetConnectionString("StudyTrackDb")));'
    replacement = marker + "\n\nbuilder.Services.AddScoped<CourseService>();"
    program = program.replace(marker, replacement)

program_path.write_text(fix(program), encoding="utf-8")

# Append CSS
css_path = Path("src/StudyTrack/wwwroot/css/app.css")
css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

phase3_css = """
.crud-panel,
.details-panel {
    border: 1px solid #d6d5d5;
    border-radius: 0.75rem;
    padding: 1rem;
    margin-bottom: 1.25rem;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1rem;
}

.form-field {
    display: flex;
    flex-direction: column;
}

.form-field-wide {
    grid-column: 1 / -1;
}

.form-field label {
    font-weight: 600;
    margin-bottom: 0.35rem;
}

.button-row {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}

.section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.record-count,
.muted-text {
    color: #666666;
    font-size: 0.92rem;
}

.empty-state {
    border: 1px dashed #b6b6b6;
    border-radius: 0.5rem;
    padding: 1rem;
    color: #555555;
    background: #fafafa;
}

.course-table td {
    vertical-align: middle;
}

.course-table .btn {
    margin: 0.15rem;
}
"""

if ".crud-panel" not in css:
    css = css.rstrip() + "\n\n" + phase3_css.strip() + "\n"

css_path.write_text(css, encoding="utf-8")

# Docs
testing_path = Path("docs/TESTING_CHECKLIST.md")
testing = testing_path.read_text(encoding="utf-8")

if "## Phase 3 Checks" not in testing:
    testing += """

## Phase 3 Checks

- [ ] Courses page displays seeded courses
- [ ] Course create form appears
- [ ] Course name validation appears when name is missing
- [ ] New course can be created
- [ ] Existing course can be edited
- [ ] Course can be deleted
- [ ] Course details page opens
- [ ] Course details page shows connected assignments
- [ ] Success message appears after create/edit/delete
- [ ] Friendly not-found message appears for invalid course ID
- [ ] Project builds successfully
"""
testing_path.write_text(testing, encoding="utf-8")

devnotes_path = Path("docs/DEVELOPER_NOTES.md")
devnotes = devnotes_path.read_text(encoding="utf-8")

if "## Phase 3 Notes" not in devnotes:
    devnotes += """

## Phase 3 Notes

Phase 3 implements Course Management CRUD. CourseService handles database operations. Courses.razor provides list, create, edit, and delete workflows with validation and user feedback. CourseDetails.razor shows course metadata and assignments linked to the selected course.
"""
devnotes_path.write_text(devnotes, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")

if "## Phase 3 Course Management" not in readme:
    readme += """

## Phase 3 Course Management

Course management now supports:

- Viewing seeded courses
- Creating courses
- Editing courses
- Deleting courses
- Viewing course details
- Viewing assignments connected to a course
- Validation and user feedback
"""
readme_path.write_text(readme, encoding="utf-8")

print("Phase 3 patch applied successfully.")
