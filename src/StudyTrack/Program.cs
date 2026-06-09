using Microsoft.EntityFrameworkCore;
using StudyTrack.Components;
using StudyTrack.Data;
using StudyTrack.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddDbContext<StudyTrackDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("StudyTrackDb")));

builder.Services.AddScoped<CourseService>();
builder.Services.AddScoped<AssignmentService>();
builder.Services.AddScoped<DashboardService>();
builder.Services.AddScoped<StudySessionService>();

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

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
