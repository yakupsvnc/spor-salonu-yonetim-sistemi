# =====================================================
# DOSYA: dal/bakim_dal.py
# AÇIKLAMA: Ekipman Bakımları tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class BakimDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_bakim_listele")

    def ekle(self, ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti, bakim_durumu):
        self.db.call_procedure("sp_bakim_ekle", (ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti, bakim_durumu))

    def guncelle(self, bakim_id, ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti, bakim_durumu):
        self.db.call_procedure("sp_bakim_guncelle", (bakim_id, ekipman_id, bakim_tarihi, aciklama, bakim_maliyeti, bakim_durumu))

    def sil(self, bakim_id):
        self.db.call_procedure("sp_bakim_sil", (bakim_id,))
