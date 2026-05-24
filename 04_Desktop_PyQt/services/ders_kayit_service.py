# =====================================================
# DOSYA: services/ders_kayit_service.py
# AÇIKLAMA: Ders Kayıt iş kuralları — Business Layer
# =====================================================

from dal.ders_kayit_dal import DersKayitDAL


class DersKayitService:
    def __init__(self):
        self.dal = DersKayitDAL()

    def _validate(self, uye_id, ders_id):
        if not uye_id:
            raise ValueError("Üye seçilmelidir.")
        if not ders_id:
            raise ValueError("Ders seçilmelidir.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, uye_id, ders_id, durum):
        self._validate(uye_id, ders_id)
        self.dal.ekle(uye_id, ders_id, durum)

    def guncelle(self, ders_kayit_id, uye_id, ders_id, durum):
        self._validate(uye_id, ders_id)
        self.dal.guncelle(ders_kayit_id, uye_id, ders_id, durum)

    def sil(self, ders_kayit_id):
        self.dal.sil(ders_kayit_id)
