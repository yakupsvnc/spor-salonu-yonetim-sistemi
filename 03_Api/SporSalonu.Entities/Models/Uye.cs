namespace SporSalonu.Entities.Models;

public class Uye
{
    public int UyeId { get; set; }

    public string Ad { get; set; } = string.Empty;

    public string Soyad { get; set; } = string.Empty;

    public string Telefon { get; set; } = string.Empty;

    public string? Email { get; set; }

    public string Cinsiyet { get; set; } = "Belirtmek İstemiyor";

    public DateTime? DogumTarihi { get; set; }

    public DateTime KayitTarihi { get; set; }

    public bool AktifMi { get; set; }
}