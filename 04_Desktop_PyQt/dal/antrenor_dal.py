# =====================================================
# DOSYA: dal/antrenor_dal.py
# AÇIKLAMA: Antrenörler tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class AntrenorDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_antrenor_listele")

    def ekle(self, ad, soyad, telefon, email, uzmanlik_alani, maas, ise_baslama_tarihi):
        self.db.call_procedure("sp_antrenor_ekle", (ad, soyad, telefon, email, uzmanlik_alani, maas, ise_baslama_tarihi))

    def guncelle(self, antrenor_id, ad, soyad, telefon, email, uzmanlik_alani, maas, ise_baslama_tarihi, aktif_mi):
        self.db.call_procedure("sp_antrenor_guncelle", (antrenor_id, ad, soyad, telefon, email, uzmanlik_alani, maas, ise_baslama_tarihi, aktif_mi))

    def sil(self, antrenor_id):
        self.db.call_procedure("sp_antrenor_sil", (antrenor_id,))
