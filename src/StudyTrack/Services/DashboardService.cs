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

    public async Task<DashboardSummary> GetDashboardSummaryAsync()
    {
        var today = DateTime.Today;
        var upcomingLimit = today.AddDays(7);

        var assignments = await _context.AssignmentTasks
            .Include(assignment => assignment.Course)
            .OrderBy(assignment => assignment.DueDate)
            .ToListAsync();

        var pendingAssignments = assignments
            .Where(assignment => assignment.Status != AssignmentStatus.Completed)
            .ToList();

        return new DashboardSummary
        {
            TotalAssignments = assignments.Count,
            PendingCount = pendingAssignments.Count,
            CompletedCount = assignments.Count(assignment => assignment.Status == AssignmentStatus.Completed),
            OverdueCount = assignments.Count(assignment =>
                assignment.Status != AssignmentStatus.Completed &&
                assignment.DueDate.Date < today),
            HighPriorityCount = pendingAssignments.Count(assignment => assignment.Priority == AssignmentPriority.High),
            UpcomingAssignments = pendingAssignments
                .Where(assignment => assignment.DueDate.Date >= today && assignment.DueDate.Date <= upcomingLimit)
                .OrderBy(assignment => assignment.DueDate)
                .Take(5)
                .ToList(),
            OverdueAssignments = pendingAssignments
                .Where(assignment => assignment.DueDate.Date < today)
                .OrderBy(assignment => assignment.DueDate)
                .Take(5)
                .ToList(),
            HighPriorityAssignments = pendingAssignments
                .Where(assignment => assignment.Priority == AssignmentPriority.High)
                .OrderBy(assignment => assignment.DueDate)
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

    public List<AssignmentTask> UpcomingAssignments { get; set; } = new();
    public List<AssignmentTask> OverdueAssignments { get; set; } = new();
    public List<AssignmentTask> HighPriorityAssignments { get; set; } = new();
}
