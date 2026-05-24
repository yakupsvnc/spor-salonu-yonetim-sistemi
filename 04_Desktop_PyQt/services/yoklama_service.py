# =====================================================
# DOSYA: services/yoklama_service.py
# AÇIKLAMA: Yoklama iş kuralları — Business Layer
# =====================================================

from dal.yoklama_dal import YoklamaDAL


class YoklamaService:
    def __init__(self):
        self.dal = YoklamaDAL()

    def _validate(self, ders_kayit_id, yoklama_tarihi):
        if not ders_kayit_id:
            raise ValueError("Ders kaydı seçilmelidir.")
        if not yoklama_tarihi:
            raise ValueError("Yoklama tarihi girilmelidir.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, ders_kayit_id, yoklama_tarihi, katilim_durumu, aciklama):
        self._validate(ders_kayit_id, yoklama_tarihi)
        self.dal.ekle(ders_kayit_id, yoklama_tarihi, katilim_durumu,
                      aciklama.strip() if aciklama else None)

    def guncelle(self, yoklama_id, ders_kayit_id, yoklama_tarihi, katilim_durumu, aciklama):
        self._validate(ders_kayit_id, yoklama_tarihi)
        self.dal.guncelle(yoklama_id, ders_kayit_id, yoklama_tarihi, katilim_durumu,
                          aciklama.strip() if aciklama else None)

    def sil(self, yoklama_id):
        self.dal.sil(yoklama_id)
