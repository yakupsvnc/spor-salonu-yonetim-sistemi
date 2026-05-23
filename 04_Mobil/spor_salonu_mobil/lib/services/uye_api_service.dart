import 'dart:convert';

import 'package:http/http.dart' as http;
import '../models/uye.dart';

class UyeApiService {
  static const String baseUrl = 'http://localhost:5193/api/uyeler';

  Future<List<Uye>> uyeleriGetir() async {
    final response = await http.get(Uri.parse(baseUrl));

    if (response.statusCode == 200) {
      final List<dynamic> jsonList = jsonDecode(response.body);

      return jsonList
          .map((json) => Uye.fromJson(json as Map<String, dynamic>))
          .toList();
    } else {
      throw Exception('Üyeler getirilemedi. Hata kodu: ${response.statusCode}');
    }
  }

  Future<void> uyeEkle({
    required String ad,
    required String soyad,
    required String telefon,
    required String email,
    required String cinsiyet,
    required String dogumTarihi,
  }) async {
    final response = await http.post(
      Uri.parse(baseUrl),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'ad': ad,
        'soyad': soyad,
        'telefon': telefon,
        'email': email,
        'cinsiyet': cinsiyet,
        'dogumTarihi': dogumTarihi,
        'aktifMi': true,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Üye eklenemedi. Hata: ${response.body}');
    }
  }

  Future<void> uyeGuncelle({
    required int uyeId,
    required String ad,
    required String soyad,
    required String telefon,
    required String email,
    required String cinsiyet,
    required String dogumTarihi,
    required bool aktifMi,
  }) async {
    final response = await http.put(
      Uri.parse('$baseUrl/$uyeId'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'uyeId': uyeId,
        'ad': ad,
        'soyad': soyad,
        'telefon': telefon,
        'email': email,
        'cinsiyet': cinsiyet,
        'dogumTarihi': dogumTarihi,
        'aktifMi': aktifMi,
      }),
    );

    if (response.statusCode != 200) {
      throw Exception('Üye güncellenemedi. Hata: ${response.body}');
    }
  }

  Future<void> uyeSil(int uyeId) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/$uyeId'),
    );

    if (response.statusCode != 200) {
      throw Exception('Üye silinemedi. Hata: ${response.body}');
    }
  }
}