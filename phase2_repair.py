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

write("src/StudyTrack/Models/AssignmentStatus.cs", """
namespace StudyTrack.Models;

public enum AssignmentStatus
{
    Pending = 0,
    InProgress = 1,
    Completed = 2,
    Overdue = 3
}
""")

write("src/StudyTrack/Models/AssignmentPriority.cs", """
namespace StudyTrack.Models;

public enum AssignmentPriority
{
    Low = 0,
    Medium = 1,
    High = 2
}
""")

write("src/StudyTrack/Models/Course.cs", """
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

    public List[[LT]]AssignmentTask[[GT]] Assignments { get; set; } = new();
}
""")

write("src/StudyTrack/Models/AssignmentTask.cs", """
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

    [Required]
    public DateTime DueDate { get; set; }

    public AssignmentPriority Priority { get; set; } = AssignmentPriority.Medium;

    public AssignmentStatus Status { get; set; } = AssignmentStatus.Pending;

    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

    public DateTime? CompletedAt { get; set; }

    [Range(1, int.MaxValue, ErrorMessage = "A course must be selected.")]
    public int CourseId { get; set; }

    public Course? Course { get; set; }

    public List[[LT]]StudySession[[GT]] StudySessions { get; set; } = new();
}
""")

write("src/StudyTrack/Models/StudySession.cs", """
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
""")

write("src/StudyTrack/Data/StudyTrackDbContext.cs", """
using Microsoft.EntityFrameworkCore;
using StudyTrack.Models;

namespace StudyTrack.Data;

public class StudyTrackDbContext : DbContext
{
    public StudyTrackDbContext(DbContextOptions[[LT]]StudyTrackDbContext[[GT]] options)
        : base(options)
    {
    }

    public DbSet[[LT]]Course[[GT]] Courses [[ARROW]] Set[[LT]]Course[[GT]]();

    public DbSet[[LT]]AssignmentTask[[GT]] AssignmentTasks [[ARROW]] Set[[LT]]AssignmentTask[[GT]]();

    public DbSet[[LT]]StudySession[[GT]] StudySessions [[ARROW]] Set[[LT]]StudySession[[GT]]();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity[[LT]]Course[[GT]]()
            .HasMany(course [[ARROW]] course.Assignments)
            .WithOne(assignment [[ARROW]] assignment.Course)
            .HasForeignKey(assignment [[ARROW]] assignment.CourseId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity[[LT]]AssignmentTask[[GT]]()
            .HasMany(assignment [[ARROW]] assignment.StudySessions)
            .WithOne(session [[ARROW]] session.AssignmentTask)
            .HasForeignKey(session [[ARROW]] session.AssignmentTaskId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
""")

write("src/StudyTrack/Data/SeedData.cs", """
using Microsoft.EntityFrameworkCore;
using StudyTrack.Models;

namespace StudyTrack.Data;

public static class SeedData
{
    public static void Initialize(IServiceProvider serviceProvider)
    {
        using var scope = serviceProvider.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService[[LT]]StudyTrackDbContext[[GT]]();

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

        var assignments = new List[[LT]]AssignmentTask[[GT]]
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
""")

write("src/StudyTrack/appsettings.json", """
{
  "ConnectionStrings": {
    "StudyTrackDb": "Data Source=StudyTrack.db"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning"
    }
  },
  "AllowedHosts": "*"
}
""")

write("src/StudyTrack/Program.cs", """
using Microsoft.EntityFrameworkCore;
using StudyTrack.Components;
using StudyTrack.Data;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddDbContext[[LT]]StudyTrackDbContext[[GT]](options [[ARROW]]
    options.UseSqlite(builder.Configuration.GetConnectionString("StudyTrackDb")));

var app = builder.Build();

SeedData.Initialize(app.Services);

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();
app.UseAntiforgery();

app.MapRazorComponents[[LT]]App[[GT]]()
    .AddInteractiveServerRenderMode();

app.Run();
""")

print("Phase 2 repair completed successfully.")
