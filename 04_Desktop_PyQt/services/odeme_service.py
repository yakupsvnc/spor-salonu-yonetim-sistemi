# =====================================================
# DOSYA: services/odeme_service.py
# AÇIKLAMA: Ödeme iş kuralları — Business Layer
# =====================================================

from dal.odeme_dal import OdemeDAL


class OdemeService:
    def __init__(self):
        self.dal = OdemeDAL()

    def _validate(self, uyelik_id, tutar):
        if not uyelik_id:
            raise ValueError("Üyelik seçilmelidir.")
        try:
            t = float(tutar)
            if t <= 0:
                raise ValueError("Ödeme tutarı 0'dan büyük olmalıdır.")
        except (TypeError, ValueError):
            raise ValueError("Geçerli bir tutar giriniz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, uyelik_id, tutar, odeme_yontemi, odeme_durumu, aciklama):
        self._validate(uyelik_id, tutar)
        self.dal.ekle(uyelik_id, float(tutar), odeme_yontemi, odeme_durumu,
                      aciklama.strip() if aciklama else None)

    def guncelle(self, odeme_id, uyelik_id, tutar, odeme_yontemi, odeme_durumu, aciklama):
        self._validate(uyelik_id, tutar)
        self.dal.guncelle(odeme_id, uyelik_id, float(tutar), odeme_yontemi, odeme_durumu,
                          aciklama.strip() if aciklama else None)

    def sil(self, odeme_id):
        self.dal.sil(odeme_id)
