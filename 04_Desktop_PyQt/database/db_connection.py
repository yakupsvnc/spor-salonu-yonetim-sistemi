# =====================================================
# Data Access Layer — MySQL bağlantı yönetimi
# Tüm CRUD işlemleri yalnızca Stored Procedure ile yapılır.
# =====================================================

import os
import sys

import mysql.connector
from mysql.connector import Error

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import DB_CONFIG
except ImportError:
    from config_example import DB_CONFIG


class DBConnection:
    """MySQL bağlantı yönetimi — singleton."""

    _instance = None

    def __init__(self):
        self._connection = None
        self._config = dict(DB_CONFIG)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = DBConnection()
        return cls._instance

    def configure(self, host=None, port=None, user=None, password=None, database=None):
        """Bağlantı ayarlarını güncelle (giriş ekranından)."""
        if host:
            self._config["host"] = host
        if port:
            self._config["port"] = int(port)
        if user:
            self._config["user"] = user
        if password is not None:
            self._config["password"] = password
        if database:
            self._config["database"] = database

    def connect(self, host=None, port=None, user=None, password=None, database=None):
        """Veritabanına bağlan. Başarı durumunu (bool, mesaj) olarak döndürür."""
        if any(v is not None for v in (host, port, user, password, database)):
            self.configure(host, port, user, password, database)
        try:
            if self._connection and self._connection.is_connected():
                self._connection.close()
            self._connection = mysql.connector.connect(**self._config)
            return True, "Bağlantı başarılı."
        except Error as e:
            self._connection = None
            return False, str(e)

    def get_connection(self):
        """Aktif bağlantıyı döndür; gerekirse yeniden bağlan."""
        if self._connection is None or not self._connection.is_connected():
            ok, msg = self.connect()
            if not ok:
                raise ConnectionError(msg)
        return self._connection

    def is_connected(self):
        try:
            return self._connection is not None and self._connection.is_connected()
        except Exception:
            return False

    def call_procedure(self, proc_name, args=()):
        """Stored Procedure çağır — DAL katmanının tek DB erişim noktası."""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc(proc_name, args)
            results = []
            for result in cursor.stored_results():
                results.extend(result.fetchall())
            conn.commit()
            return results
        except Error as e:
            raise RuntimeError(f"SP hatası ({proc_name}): {e}")
        finally:
            cursor.close()

    def call_function(self, func_name, args=()):
        """MySQL Function çağır — SELECT fn_...(args) AS result."""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            placeholders = ", ".join(["%s"] * len(args))
            query = f"SELECT {func_name}({placeholders}) AS result"
            cursor.execute(query, args)
            row = cursor.fetchone()
            return row["result"] if row else None
        except Error as e:
            raise RuntimeError(f"Function hatası ({func_name}): {e}")
        finally:
            cursor.close()

    def close(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None


# Geriye dönük uyumluluk
db = DBConnection.get_instance()
