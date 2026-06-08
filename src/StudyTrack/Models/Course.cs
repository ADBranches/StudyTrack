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
