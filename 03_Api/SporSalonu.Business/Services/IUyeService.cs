using SporSalonu.Entities.Models;

namespace SporSalonu.Business.Services;

public interface IUyeService
{
    Task<List<Uye>> ListeleAsync();

    Task<int> EkleAsync(Uye uye);

    Task<int> GuncelleAsync(Uye uye);

    Task<int> SilAsync(int uyeId);
}