using System.Data;
using MySqlConnector;
using SporSalonu.DataAccess.Database;
using SporSalonu.Entities.Models;

namespace SporSalonu.DataAccess.Repositories;

public class UyeRepository : IUyeRepository
{
    private readonly MySqlConnectionFactory _connectionFactory;

    public UyeRepository(MySqlConnectionFactory connectionFactory)
    {
        _connectionFactory = connectionFactory;
    }

    public async Task<List<Uye>> ListeleAsync()
    {
        var uyeler = new List<Uye>();

        await using var connection = _connectionFactory.CreateConnection();
        await connection.OpenAsync();

        await using var command = connection.CreateCommand();
        command.CommandText = "sp_uye_listele";
        command.CommandType = CommandType.StoredProcedure;

        await using var reader = await command.ExecuteReaderAsync();

        while (await reader.ReadAsync())
        {
            var uye = new Uye
            {
                UyeId = reader.GetInt32("uye_id"),
                Ad = reader.GetString("ad"),
                Soyad = reader.GetString("soyad"),
                Telefon = reader.GetString("telefon"),
                Email = reader.IsDBNull("email") ? null : reader.GetString("email"),
                Cinsiyet = reader.GetString("cinsiyet"),
                DogumTarihi = reader.IsDBNull("dogum_tarihi") ? null : reader.GetDateTime("dogum_tarihi"),
                KayitTarihi = reader.GetDateTime("kayit_tarihi"),
                AktifMi = reader.GetBoolean("aktif_mi")
            };

            uyeler.Add(uye);
        }

        return uyeler;
    }

    public async Task<int> EkleAsync(Uye uye)
    {
        await using var connection = _connectionFactory.CreateConnection();
        await connection.OpenAsync();

        await using var command = connection.CreateCommand();
        command.CommandText = "sp_uye_ekle";
        command.CommandType = CommandType.StoredProcedure;

        command.Parameters.AddWithValue("p_ad", uye.Ad);
        command.Parameters.AddWithValue("p_soyad", uye.Soyad);
        command.Parameters.AddWithValue("p_telefon", uye.Telefon);
        command.Parameters.AddWithValue("p_email", uye.Email);
        command.Parameters.AddWithValue("p_cinsiyet", uye.Cinsiyet);
        command.Parameters.AddWithValue("p_dogum_tarihi", uye.DogumTarihi);

        return await command.ExecuteNonQueryAsync();
    }

    public async Task<int> GuncelleAsync(Uye uye)
    {
        await using var connection = _connectionFactory.CreateConnection();
        await connection.OpenAsync();

        await using var command = connection.CreateCommand();
        command.CommandText = "sp_uye_guncelle";
        command.CommandType = CommandType.StoredProcedure;

        command.Parameters.AddWithValue("p_uye_id", uye.UyeId);
        command.Parameters.AddWithValue("p_ad", uye.Ad);
        command.Parameters.AddWithValue("p_soyad", uye.Soyad);
        command.Parameters.AddWithValue("p_telefon", uye.Telefon);
        command.Parameters.AddWithValue("p_email", uye.Email);
        command.Parameters.AddWithValue("p_cinsiyet", uye.Cinsiyet);
        command.Parameters.AddWithValue("p_dogum_tarihi", uye.DogumTarihi);
        command.Parameters.AddWithValue("p_aktif_mi", uye.AktifMi);

        return await command.ExecuteNonQueryAsync();
    }

    public async Task<int> SilAsync(int uyeId)
    {
        await using var connection = _connectionFactory.CreateConnection();
        await connection.OpenAsync();

        await using var command = connection.CreateCommand();
        command.CommandText = "sp_uye_sil";
        command.CommandType = CommandType.StoredProcedure;

        command.Parameters.AddWithValue("p_uye_id", uyeId);

        return await command.ExecuteNonQueryAsync();
    }
}