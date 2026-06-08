using System.ComponentModel.DataAnnotations;

namespace StudyTrack.Models;

public class StudySession
{
    public int Id { get; set; }

    [Required]
    public DateTime PlannedDate { get; set; }

    [Range(1, 600, ErrorMessage = "Duration must be between 1 and 600 minutes.")]
    public int DurationMinutes { get; set; }

    [StringLength(500, ErrorMessage = "Notes must be 500 characters or fewer.")]
    public string? Notes { get; set; }

    public bool IsCompleted { get; set; }

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    [Range(1, int.MaxValue, ErrorMessage = "An assignment must be selected.")]
    public int AssignmentTaskId { get; set; }

    public AssignmentTask? AssignmentTask { get; set; }
}
