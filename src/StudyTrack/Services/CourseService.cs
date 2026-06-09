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
        if (id <= 0)
        {
            return null;
        }

        return await _context.Courses
            .Include(course => course.Assignments.OrderBy(assignment => assignment.DueDate))
            .FirstOrDefaultAsync(course => course.Id == id);
    }

    public async Task<Course> CreateCourseAsync(Course course)
    {
        if (string.IsNullOrWhiteSpace(course.Name))
        {
            throw new ArgumentException("Course name is required.", nameof(course));
        }

        course.Name = course.Name.Trim();
        course.Code = string.IsNullOrWhiteSpace(course.Code) ? null : course.Code.Trim();
        course.Description = string.IsNullOrWhiteSpace(course.Description) ? null : course.Description.Trim();
        course.CreatedAt = DateTime.UtcNow;
        course.UpdatedAt = DateTime.UtcNow;

        _context.Courses.Add(course);
        await _context.SaveChangesAsync();

        return course;
    }

    public async Task<bool> UpdateCourseAsync(Course updatedCourse)
    {
        if (updatedCourse.Id <= 0 || string.IsNullOrWhiteSpace(updatedCourse.Name))
        {
            return false;
        }

        var existingCourse = await _context.Courses.FindAsync(updatedCourse.Id);

        if (existingCourse is null)
        {
            return false;
        }

        existingCourse.Name = updatedCourse.Name.Trim();
        existingCourse.Code = string.IsNullOrWhiteSpace(updatedCourse.Code) ? null : updatedCourse.Code.Trim();
        existingCourse.Description = string.IsNullOrWhiteSpace(updatedCourse.Description) ? null : updatedCourse.Description.Trim();
        existingCourse.UpdatedAt = DateTime.UtcNow;

        await _context.SaveChangesAsync();
        return true;
    }

    public async Task<bool> DeleteCourseAsync(int id)
    {
        if (id <= 0)
        {
            return false;
        }

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
