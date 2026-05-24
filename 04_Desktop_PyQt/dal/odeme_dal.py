# =====================================================
# DOSYA: dal/odeme_dal.py
# AÇIKLAMA: Ödemeler tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class OdemeDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_odeme_listele")

    def ekle(self, uyelik_id, tutar, odeme_yontemi, odeme_durumu, aciklama):
        self.db.call_procedure("sp_odeme_ekle", (uyelik_id, tutar, odeme_yontemi, odeme_durumu, aciklama))

    def guncelle(self, odeme_id, uyelik_id, tutar, odeme_yontemi, odeme_durumu, aciklama):
        self.db.call_procedure("sp_odeme_guncelle", (odeme_id, uyelik_id, tutar, odeme_yontemi, odeme_durumu, aciklama))

    def sil(self, odeme_id):
        self.db.call_procedure("sp_odeme_sil", (odeme_id,))
