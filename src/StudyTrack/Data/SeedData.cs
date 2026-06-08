using Microsoft.EntityFrameworkCore;
using StudyTrack.Models;

namespace StudyTrack.Data;

public static class SeedData
{
    public static void Initialize(IServiceProvider serviceProvider)
    {
        using var scope = serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<StudyTrackDbContext>();

        context.Database.Migrate();

        if (context.Courses.Any())
        {
            return;
        }

        var cse325 = new Course
        {
            Name = "CSE 325",
            Code = "CSE325",
            Description = ".NET Software Development"
        };

        var security = new Course
        {
            Name = "Computer Security",
            Code = "SEC401",
            Description = "Security concepts and applied protection tasks"
        };

        var forensics = new Course
        {
            Name = "Digital Forensics",
            Code = "FOR350",
            Description = "Investigation, evidence handling, and reporting"
        };

        context.Courses.AddRange(cse325, security, forensics);
        context.SaveChanges();

        var assignments = new List<AssignmentTask>
        {
            new()
            {
                Title = "Build StudyTrack Dashboard",
                Description = "Create dashboard cards for upcoming, overdue, completed, and high-priority assignments.",
                CourseId = cse325.Id,
                DueDate = DateTime.Today.AddDays(5),
                Priority = AssignmentPriority.High,
                Status = AssignmentStatus.InProgress
            },
            new()
            {
                Title = "Complete Group Project Documentation",
                Description = "Update README, user guide, developer notes, and testing checklist.",
                CourseId = cse325.Id,
                DueDate = DateTime.Today.AddDays(7),
                Priority = AssignmentPriority.High,
                Status = AssignmentStatus.Pending
            },
            new()
            {
                Title = "Review Security Validation Rules",
                Description = "Review form validation, friendly errors, and user feedback.",
                CourseId = security.Id,
                DueDate = DateTime.Today.AddDays(3),
                Priority = AssignmentPriority.Medium,
                Status = AssignmentStatus.Pending
            },
            new()
            {
                Title = "Draft Forensics Report Outline",
                Description = "Prepare a report outline for investigation documentation.",
                CourseId = forensics.Id,
                DueDate = DateTime.Today.AddDays(-2),
                Priority = AssignmentPriority.Medium,
                Status = AssignmentStatus.Overdue
            },
            new()
            {
                Title = "Submit Week 06 Checkpoint",
                Description = "Submit project checkpoint update with board task reference.",
                CourseId = cse325.Id,
                DueDate = DateTime.Today.AddDays(-1),
                Priority = AssignmentPriority.Low,
                Status = AssignmentStatus.Completed,
                CompletedAt = DateTime.UtcNow.AddDays(-1)
            }
        };

        context.AssignmentTasks.AddRange(assignments);
        context.SaveChanges();

        context.StudySessions.AddRange(
            new StudySession
            {
                AssignmentTaskId = assignments[0].Id,
                PlannedDate = DateTime.Today.AddDays(1).AddHours(18),
                DurationMinutes = 90,
                Notes = "Focus on dashboard layout and summary-card logic."
            },
            new StudySession
            {
                AssignmentTaskId = assignments[1].Id,
                PlannedDate = DateTime.Today.AddDays(2).AddHours(17),
                DurationMinutes = 60,
                Notes = "Review README and testing checklist."
            }
        );

        context.SaveChanges();
    }
}
