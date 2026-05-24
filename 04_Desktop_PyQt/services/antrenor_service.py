# =====================================================
# DOSYA: services/antrenor_service.py
# AÇIKLAMA: Antrenör iş kuralları — Business Layer
# =====================================================

from dal.antrenor_dal import AntrenorDAL


class AntrenorService:
    def __init__(self):
        self.dal = AntrenorDAL()

    def _validate(self, ad, soyad, telefon, maas):
        if not ad or len(ad.strip()) < 2:
            raise ValueError("Ad en az 2 karakter olmalıdır.")
        if not soyad or len(soyad.strip()) < 2:
            raise ValueError("Soyad en az 2 karakter olmalıdır.")
        if not telefon or len(telefon.strip()) < 7:
            raise ValueError("Geçerli bir telefon numarası giriniz.")
        try:
            m = float(maas)
            if m < 0:
                raise ValueError("Maaş negatif olamaz.")
        except (TypeError, ValueError):
            raise ValueError("Geçerli bir maaş değeri giriniz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, ad, soyad, telefon, email, uzmanlik_alani, maas, ise_baslama_tarihi):
        self._validate(ad, soyad, telefon, maas)
        self.dal.ekle(ad.strip(), soyad.strip(), telefon.strip(),
                      email.strip() if email else None,
                      uzmanlik_alani.strip(), float(maas), ise_baslama_tarihi)

    def guncelle(self, antrenor_id, ad, soyad, telefon, email, uzmanlik_alani, maas, ise_baslama_tarihi, aktif_mi):
        self._validate(ad, soyad, telefon, maas)
        self.dal.guncelle(antrenor_id, ad.strip(), soyad.strip(), telefon.strip(),
                          email.strip() if email else None,
                          uzmanlik_alani.strip(), float(maas), ise_baslama_tarihi, aktif_mi)

    def sil(self, antrenor_id):
        self.dal.sil(antrenor_id)
