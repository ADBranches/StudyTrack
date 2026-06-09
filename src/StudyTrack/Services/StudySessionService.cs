using Microsoft.EntityFrameworkCore;
using StudyTrack.Data;
using StudyTrack.Models;

namespace StudyTrack.Services;

public class StudySessionService
{
    private readonly StudyTrackDbContext _context;

    public StudySessionService(StudyTrackDbContext context)
    {
        _context = context;
    }

    public async Task<List<StudySession>> GetStudySessionsAsync()
    {
        return await _context.StudySessions
            .Include(session => session.AssignmentTask)
                .ThenInclude(assignment => assignment!.Course)
            .OrderBy(session => session.PlannedDate)
            .ToListAsync();
    }

    public async Task<StudySession?> GetStudySessionByIdAsync(int id)
    {
        return await _context.StudySessions
            .Include(session => session.AssignmentTask)
                .ThenInclude(assignment => assignment!.Course)
            .FirstOrDefaultAsync(session => session.Id == id);
    }

    public async Task<StudySession> CreateStudySessionAsync(StudySession session)
    {
        session.CreatedAt = DateTime.UtcNow;

        _context.StudySessions.Add(session);
        await _context.SaveChangesAsync();

        return session;
    }

    public async Task<bool> MarkCompletedAsync(int id)
    {
        var existingSession = await _context.StudySessions.FindAsync(id);

        if (existingSession is null)
        {
            return false;
        }

        existingSession.IsCompleted = true;
        await _context.SaveChangesAsync();

        return true;
    }

    public async Task<bool> ReopenAsync(int id)
    {
        var existingSession = await _context.StudySessions.FindAsync(id);

        if (existingSession is null)
        {
            return false;
        }

        existingSession.IsCompleted = false;
        await _context.SaveChangesAsync();

        return true;
    }

    public async Task<bool> DeleteStudySessionAsync(int id)
    {
        var existingSession = await _context.StudySessions.FindAsync(id);

        if (existingSession is null)
        {
            return false;
        }

        _context.StudySessions.Remove(existingSession);
        await _context.SaveChangesAsync();

        return true;
    }
}
