# =====================================================
# DOSYA: services/ders_service.py
# AÇIKLAMA: Ders iş kuralları — Business Layer
# =====================================================

from dal.ders_dal import DersDAL


class DersService:
    def __init__(self):
        self.dal = DersDAL()

    def _validate(self, ders_adi, antrenor_id, kontenjan):
        if not ders_adi or len(ders_adi.strip()) < 2:
            raise ValueError("Ders adı en az 2 karakter olmalıdır.")
        if not antrenor_id:
            raise ValueError("Antrenör seçilmelidir.")
        try:
            k = int(kontenjan)
            if k <= 0:
                raise ValueError("Kontenjan 0'dan büyük olmalıdır.")
        except (TypeError, ValueError):
            raise ValueError("Geçerli bir kontenjan giriniz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati):
        self._validate(ders_adi, antrenor_id, kontenjan)
        self.dal.ekle(ders_adi.strip(), antrenor_id, int(kontenjan), ders_gunu,
                      baslangic_saati, bitis_saati)

    def guncelle(self, ders_id, ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati, aktif_mi):
        self._validate(ders_adi, antrenor_id, kontenjan)
        self.dal.guncelle(ders_id, ders_adi.strip(), antrenor_id, int(kontenjan),
                          ders_gunu, baslangic_saati, bitis_saati, aktif_mi)

    def sil(self, ders_id):
        self.dal.sil(ders_id)

    def doluluk_orani(self, ders_id):
        return self.dal.doluluk_orani(ders_id) or 0
