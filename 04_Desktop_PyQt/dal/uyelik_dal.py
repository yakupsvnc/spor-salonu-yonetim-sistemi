# =====================================================
# DOSYA: dal/uyelik_dal.py
# AÇIKLAMA: Üyelikler tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class UyelikDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_uyelik_listele")

    def ekle(self, uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum):
        self.db.call_procedure("sp_uyelik_ekle", (uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum))

    def guncelle(self, uyelik_id, uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum):
        self.db.call_procedure("sp_uyelik_guncelle", (uyelik_id, uye_id, paket_id, baslangic_tarihi, bitis_tarihi, durum))

    def sil(self, uyelik_id):
        self.db.call_procedure("sp_uyelik_sil", (uyelik_id,))

    def kalan_gun(self, uyelik_id):
        return self.db.call_function("fn_uyelik_kalan_gun", (uyelik_id,))
