# =====================================================
# DOSYA: dal/ekipman_dal.py
# AÇIKLAMA: Salon Ekipmanları tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class EkipmanDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_ekipman_listele")

    def ekle(self, ekipman_adi, kategori, alim_tarihi, durum, aciklama):
        self.db.call_procedure("sp_ekipman_ekle", (ekipman_adi, kategori, alim_tarihi, durum, aciklama))

    def guncelle(self, ekipman_id, ekipman_adi, kategori, alim_tarihi, durum, aciklama):
        self.db.call_procedure("sp_ekipman_guncelle", (ekipman_id, ekipman_adi, kategori, alim_tarihi, durum, aciklama))

    def sil(self, ekipman_id):
        self.db.call_procedure("sp_ekipman_sil", (ekipman_id,))
