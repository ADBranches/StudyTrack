using Microsoft.EntityFrameworkCore;
using StudyTrack.Models;

namespace StudyTrack.Data;

public class StudyTrackDbContext : DbContext
{
    public StudyTrackDbContext(DbContextOptions<StudyTrackDbContext> options)
        : base(options)
    {
    }

    public DbSet<Course> Courses => Set<Course>();

    public DbSet<AssignmentTask> AssignmentTasks => Set<AssignmentTask>();

    public DbSet<StudySession> StudySessions => Set<StudySession>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Course>()
            .HasMany(course => course.Assignments)
            .WithOne(assignment => assignment.Course)
            .HasForeignKey(assignment => assignment.CourseId)
            .OnDelete(DeleteBehavior.Cascade);

        modelBuilder.Entity<AssignmentTask>()
            .HasMany(assignment => assignment.StudySessions)
            .WithOne(session => session.AssignmentTask)
            .HasForeignKey(session => session.AssignmentTaskId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
