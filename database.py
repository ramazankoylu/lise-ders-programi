import sqlite3

class Database:
    def __init__(self, db_name="ders_programi.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Veritabanı tablolarını oluşturur"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ogrenciler (
                id INTEGER PRIMARY KEY,
                ad TEXT NOT NULL,
                soyad TEXT NOT NULL,
                ogrenci_notu TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS programlar (
                id INTEGER PRIMARY KEY,
                ogrenci_id INTEGER,
                gun TEXT,
                ders TEXT,
                konu TEXT,
                saat INTEGER,
                FOREIGN KEY (ogrenci_id) REFERENCES ogrenciler(id)
            )
        ''')
        self.conn.commit()

    def insert_ogrenci(self, ad, soyad, ogrenci_notu):
        self.cursor.execute("INSERT INTO ogrenciler (ad, soyad, ogrenci_notu) VALUES (?, ?, ?)", (ad, soyad, ogrenci_notu))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_program(self, ogrenci_id, gun, ders, konu, saat):
        self.cursor.execute("INSERT INTO programlar (ogrenci_id, gun, ders, konu, saat) VALUES (?, ?, ?, ?, ?)",
                            (ogrenci_id, gun, ders, konu, saat))
        self.conn.commit()

    def get_ogrenciler(self):
        self.cursor.execute("SELECT * FROM ogrenciler")
        return self.cursor.fetchall()

    def get_program_by_ogrenci(self, ogrenci_id):
        self.cursor.execute("SELECT gun, ders, konu, saat FROM programlar WHERE ogrenci_id = ?", (ogrenci_id,))
        return self.cursor.fetchall()

    def get_ogrenci_id(self, ad, soyad):
        self.cursor.execute("SELECT id FROM ogrenciler WHERE ad = ? AND soyad = ?", (ad, soyad))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete_ogrenci(self, ogrenci_id):
        """Öğrenciyi ve onunla ilgili tüm ders programlarını siler"""
        self.cursor.execute("DELETE FROM ogrenciler WHERE id = ?", (ogrenci_id,))
        self.cursor.execute("DELETE FROM programlar WHERE ogrenci_id = ?", (ogrenci_id,))
        self.conn.commit()
