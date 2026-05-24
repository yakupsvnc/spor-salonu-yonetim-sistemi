# =====================================================
# DOSYA: services/uyelik_service.py
# AÇIKLAMA: Üyelik iş kuralları — Business Layer
# =====================================================

from datetime import date
from dal.uyelik_dal import UyelikDAL


class UyelikService:
    def __init__(self):
        self.dal = UyelikDAL()

    def _validate(self, uye_id, paket_id, baslangic_tarihi, bitis_tarihi):
        if not uye_id:
            raise ValueError("Üye seçilmelidir.")
        if not paket_id:
            raise ValueError("Paket seçilmelidir.")
        if baslangic_tarihi and bitis_tarihi:
            if bitis_tarihi < baslangic_tarihi:
                raise ValueError("Bitiş tarihi başlangıç tarihinden önce olamaz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum):
        self._validate(uye_id, paket_id, baslangic_tarihi, bitis_tarihi)
        self.dal.ekle(uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum)

    def guncelle(self, uyelik_id, uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum):
        self._validate(uye_id, paket_id, baslangic_tarihi, bitis_tarihi)
        self.dal.guncelle(uyelik_id, uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum)

    def sil(self, uyelik_id):
        self.dal.sil(uyelik_id)

    def kalan_gun(self, uyelik_id):
        return self.dal.kalan_gun(uyelik_id) or 0
