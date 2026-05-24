# =====================================================
# DOSYA: dal/ders_dal.py
# AÇIKLAMA: Dersler tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class DersDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_ders_listele")

    def ekle(self, ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati):
        self.db.call_procedure("sp_ders_ekle", (ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati))

    def guncelle(self, ders_id, ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati, aktif_mi):
        self.db.call_procedure("sp_ders_guncelle", (ders_id, ders_adi, antrenor_id, kontenjan, ders_gunu, baslangic_saati, bitis_saati, aktif_mi))

    def sil(self, ders_id):
        self.db.call_procedure("sp_ders_sil", (ders_id,))

    def doluluk_orani(self, ders_id):
        return self.db.call_function("fn_ders_doluluk_orani", (ders_id,))
