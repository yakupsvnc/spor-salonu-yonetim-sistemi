using SporSalonu.DataAccess.Repositories;
using SporSalonu.Entities.Models;

namespace SporSalonu.Business.Services;

public class UyeService : IUyeService
{
    private readonly IUyeRepository _uyeRepository;

    public UyeService(IUyeRepository uyeRepository)
    {
        _uyeRepository = uyeRepository;
    }

    public async Task<List<Uye>> ListeleAsync()
    {
        return await _uyeRepository.ListeleAsync();
    }

    public async Task<int> EkleAsync(Uye uye)
    {
        UyeKontrolEt(uye);

        return await _uyeRepository.EkleAsync(uye);
    }

    public async Task<int> GuncelleAsync(Uye uye)
    {
        if (uye.UyeId <= 0)
        {
            throw new ArgumentException("Güncellenecek üye ID değeri geçerli olmalıdır.");
        }

        UyeKontrolEt(uye);

        return await _uyeRepository.GuncelleAsync(uye);
    }

    public async Task<int> SilAsync(int uyeId)
    {
        if (uyeId <= 0)
        {
            throw new ArgumentException("Silinecek üye ID değeri geçerli olmalıdır.");
        }

        return await _uyeRepository.SilAsync(uyeId);
    }

    private static void UyeKontrolEt(Uye uye)
    {
        if (string.IsNullOrWhiteSpace(uye.Ad))
        {
            throw new ArgumentException("Üye adı boş bırakılamaz.");
        }

        if (string.IsNullOrWhiteSpace(uye.Soyad))
        {
            throw new ArgumentException("Üye soyadı boş bırakılamaz.");
        }

        if (string.IsNullOrWhiteSpace(uye.Telefon))
        {
            throw new ArgumentException("Telefon numarası boş bırakılamaz.");
        }

        if (uye.Ad.Length < 2)
        {
            throw new ArgumentException("Üye adı en az 2 karakter olmalıdır.");
        }

        if (uye.Soyad.Length < 2)
        {
            throw new ArgumentException("Üye soyadı en az 2 karakter olmalıdır.");
        }
    }
}