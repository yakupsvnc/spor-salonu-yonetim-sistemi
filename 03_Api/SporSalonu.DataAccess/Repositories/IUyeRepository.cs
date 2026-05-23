using SporSalonu.Entities.Models;

namespace SporSalonu.DataAccess.Repositories;

public interface IUyeRepository
{
    Task<List<Uye>> ListeleAsync();

    Task<int> EkleAsync(Uye uye);

    Task<int> GuncelleAsync(Uye uye);

    Task<int> SilAsync(int uyeId);
}