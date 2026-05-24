# =====================================================
# DOSYA: dal/uye_dal.py
# AÇIKLAMA: Üyeler tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class UyeDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_uye_listele")

    def ekle(self, ad, soyad, telefon, email, cinsiyet, dogum_tarihi):
        self.db.call_procedure("sp_uye_ekle", (ad, soyad, telefon, email, cinsiyet, dogum_tarihi))

    def guncelle(self, uye_id, ad, soyad, telefon, email, cinsiyet, dogum_tarihi, aktif_mi):
        self.db.call_procedure("sp_uye_guncelle", (uye_id, ad, soyad, telefon, email, cinsiyet, dogum_tarihi, aktif_mi))

    def sil(self, uye_id):
        self.db.call_procedure("sp_uye_sil", (uye_id,))

    def toplam_odeme(self, uye_id):
        return self.db.call_function("fn_uye_toplam_odeme", (uye_id,))
