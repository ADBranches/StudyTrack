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

    public async Task<List<AssignmentTask>> GetAssignmentsAsync()
    {
        return await _context.AssignmentTasks
            .Include(assignment => assignment.Course)
            .OrderBy(assignment => assignment.DueDate)
            .ThenByDescending(assignment => assignment.Priority)
            .ToListAsync();
    }

    public async Task<AssignmentTask?> GetAssignmentByIdAsync(int id)
    {
        return await _context.AssignmentTasks
            .Include(assignment => assignment.Course)
            .Include(assignment => assignment.StudySessions.OrderBy(session => session.PlannedDate))
            .FirstOrDefaultAsync(assignment => assignment.Id == id);
    }

    public async Task<AssignmentTask> CreateAssignmentAsync(AssignmentTask assignment)
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

    public async Task<bool> UpdateAssignmentAsync(AssignmentTask updatedAssignment)
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

    public async Task<bool> DeleteAssignmentAsync(int id)
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

    public async Task<bool> MarkCompletedAsync(int id)
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

    public async Task<bool> ReopenAssignmentAsync(int id)
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
