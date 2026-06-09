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

    [Required(ErrorMessage = "Due date is required.")]
    public DateTime DueDate { get; set; }

    public AssignmentPriority Priority { get; set; } = AssignmentPriority.Medium;

    public AssignmentStatus Status { get; set; } = AssignmentStatus.Pending;

    public int CourseId { get; set; }

    public Course? Course { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    public DateTime? CompletedAt { get; set; }

    public List<StudySession> StudySessions { get; set; } = new();
}
