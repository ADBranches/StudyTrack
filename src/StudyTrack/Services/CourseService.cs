using Microsoft.EntityFrameworkCore;
using StudyTrack.Data;
using StudyTrack.Models;

namespace StudyTrack.Services;

public class CourseService
{
    private readonly StudyTrackDbContext _context;

    public CourseService(StudyTrackDbContext context)
    {
        _context = context;
    }

    public async Task<List<Course>> GetCoursesAsync()
    {
        return await _context.Courses
            .Include(course => course.Assignments)
            .OrderBy(course => course.Name)
            .ToListAsync();
    }

    public async Task<Course?> GetCourseByIdAsync(int id)
    {
        return await _context.Courses
            .Include(course => course.Assignments.OrderBy(assignment => assignment.DueDate))
            .FirstOrDefaultAsync(course => course.Id == id);
    }

    public async Task<Course> CreateCourseAsync(Course course)
    {
        course.CreatedAt = DateTime.UtcNow;
        course.UpdatedAt = DateTime.UtcNow;

        _context.Courses.Add(course);
        await _context.SaveChangesAsync();

        return course;
    }

    public async Task<bool> UpdateCourseAsync(Course updatedCourse)
    {
        var existingCourse = await _context.Courses.FindAsync(updatedCourse.Id);

        if (existingCourse is null)
        {
            return false;
        }

        existingCourse.Name = updatedCourse.Name;
        existingCourse.Code = updatedCourse.Code;
        existingCourse.Description = updatedCourse.Description;
        existingCourse.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> DeleteCourseAsync(int id)
    {
        var existingCourse = await _context.Courses
            .Include(course => course.Assignments)
            .FirstOrDefaultAsync(course => course.Id == id);

        if (existingCourse is null)
        {
            return false;
        }

        _context.Courses.Remove(existingCourse);
        await _context.SaveChangesAsync();

        return true;
    }
}
