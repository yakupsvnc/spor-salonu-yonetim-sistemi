# =====================================================
# DOSYA: services/ekipman_service.py
# AÇIKLAMA: Ekipman iş kuralları — Business Layer
# =====================================================

from dal.ekipman_dal import EkipmanDAL


class EkipmanService:
    def __init__(self):
        self.dal = EkipmanDAL()

    def _validate(self, ekipman_adi, kategori):
        if not ekipman_adi or len(ekipman_adi.strip()) < 2:
            raise ValueError("Ekipman adı en az 2 karakter olmalıdır.")
        if not kategori or len(kategori.strip()) < 1:
            raise ValueError("Kategori boş bırakılamaz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, ekipman_adi, kategori, alim_tarihi, durum, aciklama):
        self._validate(ekipman_adi, kategori)
        self.dal.ekle(ekipman_adi.strip(), kategori.strip(),
                      alim_tarihi or None, durum,
                      aciklama.strip() if aciklama else None)

    def guncelle(self, ekipman_id, ekipman_adi, kategori, alim_tarihi, durum, aciklama):
        self._validate(ekipman_adi, kategori)
        self.dal.guncelle(ekipman_id, ekipman_adi.strip(), kategori.strip(),
                          alim_tarihi or None, durum,
                          aciklama.strip() if aciklama else None)

    def sil(self, ekipman_id):
        self.dal.sil(ekipman_id)
