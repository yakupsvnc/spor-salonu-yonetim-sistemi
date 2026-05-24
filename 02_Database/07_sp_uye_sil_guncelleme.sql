-- Üye silme: bağlı kayıtları önce temizler (MySQL Workbench'te çalıştırın)
USE spor_salonu_db;

DROP PROCEDURE IF EXISTS sp_uye_sil;
DELIMITER $$
CREATE PROCEDURE sp_uye_sil (IN p_uye_id INT)
BEGIN
  DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
    ROLLBACK;
    RESIGNAL;
  END;

  START TRANSACTION;

  DELETE y FROM yoklamalar y
  INNER JOIN ders_kayitlari dk ON y.ders_kayit_id = dk.ders_kayit_id
  WHERE dk.uye_id = p_uye_id;

  DELETE FROM ders_kayitlari WHERE uye_id = p_uye_id;

  DELETE o FROM odemeler o
  INNER JOIN uyelikler u ON o.uyelik_id = u.uyelik_id
  WHERE u.uye_id = p_uye_id;

  DELETE FROM uyelikler WHERE uye_id = p_uye_id;
  DELETE FROM uyeler WHERE uye_id = p_uye_id;

  COMMIT;
END $$
DELIMITER ;
