using SporSalonu.Business.Services;
using SporSalonu.DataAccess.Database;
using SporSalonu.DataAccess.Repositories;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");

if (string.IsNullOrWhiteSpace(connectionString))
{
    throw new InvalidOperationException("DefaultConnection bağlantı cümlesi bulunamadı.");
}

builder.Services.AddSingleton(new MySqlConnectionFactory(connectionString));

builder.Services.AddScoped<IUyeRepository, UyeRepository>();
builder.Services.AddScoped<IUyeService, UyeService>();

builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll", policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

app.UseHttpsRedirection();

app.UseCors("AllowAll");

app.MapControllers();

app.MapGet("/", () => "Spor Salonu API çalışıyor.");

app.Run();