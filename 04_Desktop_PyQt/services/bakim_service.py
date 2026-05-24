# =====================================================
# DOSYA: services/bakim_service.py
# AÇIKLAMA: Bakım iş kuralları — Business Layer
# =====================================================

from dal.bakim_dal import BakimDAL


class BakimService:
    def __init__(self):
        self.dal = BakimDAL()

    def _validate(self, ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti):
        if not ekipman_id:
            raise ValueError("Ekipman seçilmelidir.")
        if not bakim_tarihi:
            raise ValueError("Bakım tarihi girilmelidir.")
        if not aciklama or len(aciklama.strip()) < 1:
            raise ValueError("Bakım açıklaması boş bırakılamaz.")
        try:
            m = float(bakim_maliyeti)
            if m < 0:
                raise ValueError("Bakım maliyeti negatif olamaz.")
        except (TypeError, ValueError):
            raise ValueError("Geçerli bir bakım maliyeti giriniz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti, bakim_durumu):
        self._validate(ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti)
        self.dal.ekle(ekipman_id, bakim_tarihi, aciklama.strip(),
                      float(bakim_maliyeti), bakim_durumu)

    def guncelle(self, bakim_id, ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti, bakim_durumu):
        self._validate(ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti)
        self.dal.guncelle(bakim_id, ekipman_id, bakim_tarihi, aciklama.strip(),
                          float(bakim_maliyeti), bakim_durumu)

    def sil(self, bakim_id):
        self.dal.sil(bakim_id)
