# =====================================================
# DOSYA: dal/ders_kayit_dal.py
# AÇIKLAMA: Ders Kayıtları tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class DersKayitDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_ders_kayit_listele")

    def ekle(self, uye_id, ders_id, durum):
        self.db.call_procedure("sp_ders_kayit_ekle", (uye_id, ders_id, durum))

    def guncelle(self, ders_kayit_id, uye_id, ders_id, durum):
        self.db.call_procedure("sp_ders_kayit_guncelle", (ders_kayit_id, uye_id, ders_id, durum))

    def sil(self, ders_kayit_id):
        self.db.call_procedure("sp_ders_kayit_sil", (ders_kayit_id,))
