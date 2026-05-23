class Uye {
  final int uyeId;
  final String ad;
  final String soyad;
  final String telefon;
  final String? email;
  final String cinsiyet;
  final String? dogumTarihi;
  final String kayitTarihi;
  final bool aktifMi;

  Uye({
    required this.uyeId,
    required this.ad,
    required this.soyad,
    required this.telefon,
    required this.email,
    required this.cinsiyet,
    required this.dogumTarihi,
    required this.kayitTarihi,
    required this.aktifMi,
  });

  factory Uye.fromJson(Map<String, dynamic> json) {
    return Uye(
      uyeId: json['uyeId'],
      ad: json['ad'],
      soyad: json['soyad'],
      telefon: json['telefon'],
      email: json['email'],
      cinsiyet: json['cinsiyet'],
      dogumTarihi: json['dogumTarihi'],
      kayitTarihi: json['kayitTarihi'],
      aktifMi: json['aktifMi'],
    );
  }
}