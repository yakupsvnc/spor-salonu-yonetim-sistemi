# =====================================================
# DOSYA: dal/yoklama_dal.py
# AÇIKLAMA: Yoklamalar tablosu — sadece CALL sp_... kullanılır
# =====================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import DBConnection


class YoklamaDAL:
    def __init__(self):
        self.db = DBConnection.get_instance()

    def listele(self):
        return self.db.call_procedure("sp_yoklama_listele")

    def ekle(self, ders_kayit_id, yoklama_tarihi, katilim_durumu, aciklama):
        self.db.call_procedure("sp_yoklama_ekle", (ders_kayit_id, yoklama_tarihi, katilim_durumu, aciklama))

    def guncelle(self, yoklama_id, ders_kayit_id, yoklama_tarihi, katilim_durumu, aciklama):
        self.db.call_procedure("sp_yoklama_guncelle", (yoklama_id, ders_kayit_id, yoklama_tarihi, katilim_durumu, aciklama))

    def sil(self, yoklama_id):
        self.db.call_procedure("sp_yoklama_sil", (yoklama_id,))
