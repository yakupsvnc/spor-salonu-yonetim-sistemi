# =====================================================
# DOSYA: services/paket_service.py
# AÇIKLAMA: Üyelik Paketi iş kuralları — Business Layer
# =====================================================

from dal.paket_dal import PaketDAL


class PaketService:
    def __init__(self):
        self.dal = PaketDAL()

    def _validate(self, paket_adi, sure_gun, ucret):
        if not paket_adi or len(paket_adi.strip()) < 2:
            raise ValueError("Paket adı en az 2 karakter olmalıdır.")
        try:
            s = int(sure_gun)
            if s <= 0:
                raise ValueError("Süre 0'dan büyük olmalıdır.")
        except (TypeError, ValueError):
            raise ValueError("Geçerli bir süre (gün) giriniz.")
        try:
            u = float(ucret)
            if u <= 0:
                raise ValueError("Ücret 0'dan büyük olmalıdır.")
        except (TypeError, ValueError):
            raise ValueError("Geçerli bir ücret giriniz.")

    def listele(self):
        return self.dal.listele()

    def ekle(self, paket_adi, sure_gun, ucret, aciklama):
        self._validate(paket_adi, sure_gun, ucret)
        self.dal.ekle(paket_adi.strip(), int(sure_gun), float(ucret),
                      aciklama.strip() if aciklama else None)

    def guncelle(self, paket_id, paket_adi, sure_gun, ucret, aciklama, aktif_mi):
        self._validate(paket_adi, sure_gun, ucret)
        self.dal.guncelle(paket_id, paket_adi.strip(), int(sure_gun), float(ucret),
                          aciklama.strip() if aciklama else None, aktif_mi)

    def sil(self, paket_id):
        self.dal.sil(paket_id)
