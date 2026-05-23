using Microsoft.AspNetCore.Mvc;
using SporSalonu.Business.Services;
using SporSalonu.Entities.Models;

namespace SporSalonu.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UyelerController : ControllerBase
{
    private readonly IUyeService _uyeService;

    public UyelerController(IUyeService uyeService)
    {
        _uyeService = uyeService;
    }

    [HttpGet]
    public async Task<IActionResult> Listele()
    {
        var uyeler = await _uyeService.ListeleAsync();
        return Ok(uyeler);
    }

    [HttpPost]
    public async Task<IActionResult> Ekle([FromBody] Uye uye)
    {
        try
        {
            await _uyeService.EkleAsync(uye);
            return Ok(new { mesaj = "Üye başarıyla eklendi." });
        }
        catch (Exception ex)
        {
            return BadRequest(new { hata = ex.Message });
        }
    }

    [HttpPut("{id:int}")]
    public async Task<IActionResult> Guncelle(int id, [FromBody] Uye uye)
    {
        try
        {
            uye.UyeId = id;
            await _uyeService.GuncelleAsync(uye);
            return Ok(new { mesaj = "Üye başarıyla güncellendi." });
        }
        catch (Exception ex)
        {
            return BadRequest(new { hata = ex.Message });
        }
    }

    [HttpDelete("{id:int}")]
    public async Task<IActionResult> Sil(int id)
    {
        try
        {
            await _uyeService.SilAsync(id);
            return Ok(new { mesaj = "Üye başarıyla silindi." });
        }
        catch (Exception ex)
        {
            return BadRequest(new { hata = ex.Message });
        }
    }
}