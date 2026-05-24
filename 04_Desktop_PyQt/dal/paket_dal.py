# =====================================================
# DOSYA: dal/paket_dal.py
# AÇIKLAMA: Üyelik Paketleri tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class PaketDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_uyelik_paketi_listele")

    def ekle(self, paket_adi, sure_gun, ucret, aciklama):
        self.db.call_procedure("sp_uyelik_paketi_ekle", (paket_adi, sure_gun, ucret, aciklama))

    def guncelle(self, paket_id, paket_adi, sure_gun, ucret, aciklama, aktif_mi):
        self.db.call_procedure("sp_uyelik_paketi_guncelle", (paket_id, paket_adi, sure_gun, ucret, aciklama, aktif_mi))

    def sil(self, paket_id):
        self.db.call_procedure("sp_uyelik_paketi_sil", (paket_id,))
