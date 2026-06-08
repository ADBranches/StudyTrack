from pathlib import Path

def write(path, text):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.strip() + "\n", encoding="utf-8")

write("src/StudyTrack/Models/AssignmentStatus.cs", r'''
namespace StudyTrack.Models;

public enum AssignmentStatus
{
    Pending = 0,
    InProgress = 1,
    Completed = 2,
    Overdue = 3
}
''')

write("src/StudyTrack/Models/AssignmentPriority.cs", r'''
namespace StudyTrack.Models;

public enum AssignmentPriority
{
    Low = 0,
    Medium = 1,
    High = 2
}
''')

write("src/StudyTrack/Models/Course.cs", r'''
using System.ComponentModel.DataAnnotations;

namespace StudyTrack.Models;

public class Course
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Course name is required.")]
    [StringLength(80, MinimumLength = 2, ErrorMessage = "Course name must be between 2 and 80 characters.")]
    public string Name { get; set; } = string.Empty;

    [StringLength(20, ErrorMessage = "Course code must be 20 characters or fewer.")]
    public string? Code { get; set; }

    [StringLength(250, ErrorMessage = "Course description must be 250 characters or fewer.")]
    public string? Description { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    public List<AssignmentTask> Assignments { get; set; } = new();
}
''')

write("src/StudyTrack/Models/AssignmentTask.cs", r'''
using System.ComponentModel.DataAnnotations;

namespace StudyTrack.Models;

public class AssignmentTask
{
    public int Id { get; set; }

    [Required(ErrorMessage = "Assignment title is required.")]
    [StringLength(120, MinimumLength = 2, ErrorMessage = "Assignment title must be between 2 and 120 characters.")]
    public string Title { get; set; } = string.Empty;

    [StringLength(500, ErrorMessage = "Assignment description must be 500 characters or fewer.")]
    public string? Description { get; set; }
}
''')

print("Phase 2 patch applied successfully.")
