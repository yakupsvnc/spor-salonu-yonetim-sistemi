# =====================================================
# DOSYA: services/uye_service.py
# AÇIKLAMA: Üye iş kuralları — Business Layer
# =====================================================

import re
from dal.uye_dal import UyeDAL


class UyeService:
    def __init__(self):
        self.dal = UyeDAL()

    def _validate(self, ad, soyad, telefon, email=""):
        if not ad or len(ad.strip()) < 2:
            raise ValueError("Ad en az 2 karakter olmalıdır.")
        if not soyad or len(soyad.strip()) < 2:
            raise ValueError("Soyad en az 2 karakter olmalıdır.")
        if not telefon or len(telefon.strip()) < 7:
            raise ValueError("Geçerli bir telefon numarası giriniz.")
        if email and email.strip() and "@" not in email:
            raise ValueError("Geçerli bir e-posta adresi giriniz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, ad, soyad, telefon, email, cinsiyet, dogum_tarihi):
        self._validate(ad, soyad, telefon, email)
        self.dal.ekle(ad.strip(), soyad.strip(), telefon.strip(),
                      email.strip() if email else None, cinsiyet, dogum_tarihi or None)

    def guncelle(self, uye_id, ad, soyad, telefon, email, cinsiyet, dogum_tarihi, aktif_mi):
        self._validate(ad, soyad, telefon, email)
        self.dal.guncelle(uye_id, ad.strip(), soyad.strip(), telefon.strip(),
                          email.strip() if email else None, cinsiyet,
                          dogum_tarihi or None, aktif_mi)

    def sil(self, uye_id):
        try:
            self.dal.sil(uye_id)
        except RuntimeError as e:
            msg = str(e).lower()
            if "1451" in msg or "foreign key" in msg:
                raise ValueError(
                    "Üye silinemedi — bağlı kayıtlar (üyelik, ders kaydı) var.\n\n"
                    "MySQL Workbench'te şu dosyayı çalıştırın:\n"
                    "02_Database/07_sp_uye_sil_guncelleme.sql"
                ) from e
            raise

    def toplam_odeme(self, uye_id):
        return self.dal.toplam_odeme(uye_id) or 0
