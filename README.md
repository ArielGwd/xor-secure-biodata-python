# Sistem CRUD Biodata dengan FastAPI + MySQL (XOR Encryption)

Aplikasi ini ialah sistem CRUD (Create, Read, Update, Delete) untuk data biodata menggunakan FastAPI, SQLAlchemy, dan MySQL.

Aplikasi juga menggunakan kriptografi simetris **Stream XOR** untuk mengenkripsi field sensitif seperti email, phone, dan address.

> Metode enkripsi XOR ini hanya untuk tujuan edukasi dan tidak disarankan untuk penggunaan produksi yang memerlukan keamanan tinggi.
---

## 1. Persyaratan Sistem

Sebelum instalasi, pastikan sistem memiliki:

### **Software Minimum**

* Python 3.10+
* MySQL 8+
* pip (Python package manager)
* Git (opsional)


## 2. Instalasi & Pengaturan

#### **1. Clone Project**

```bash
git clone https://github.com/ArielGwd/xor-secure-biodata-python.git

cd xor-secure-biodata-python
```

#### **2. Install Dependencies**

```bash
pip install fastapi uvicorn python-dotenv mysql-connector-python sqlalchemy jinja2
```

## 3. Konfigurasi Environment

Aplikasi menggunakan file `.env` untuk menyimpan konfigurasi penting.

Buat file: `.env` di file projek dengan menyalin dari `.env.example` atau hapus `.example`. 


```bash
APP_SECRET_XOR_KEY=YOUR_APP_SECRET_XOR_KEY_HERE
MYSQL_HOST=YOUR_MYSQL_HOST_HERE
MYSQL_USER=YOUR_MYSQL_USER_HERE
MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD_HERE
MYSQL_DB=YOUR_MYSQL_DB_NAME_HERE
```

**Catatan:**

* `APP_SECRET_XOR_KEY` dipakai untuk proses enkripsi XOR.
* Jika `APP_SECRET_XOR_KEY` berubah → server harus di-restart karena `.env` dibaca saat server berjalan diawal.

## 4. Database

Pastikan MySQL berjalan, lalu buat database:

```sql
CREATE DATABASE db_secure_xor;
```
**-- or --** 

kemudian import dari file [db_secure_xor.sql](./db_secure_xor.sql) yang ada di root project untuk membuat tabel.

atau jalankan perintah membuat table berikut di terminal:

```sql
CREATE TABLE biodata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    address VARCHAR(255) NULL,
    gender ENUM('male', 'female') NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 5. Menjalankan Aplikasi

Gunakan:

```bash
uvicorn main:app --reload
```

Aplikasi dapat diakses pada:

```
http://localhost:8000
```

Gambar berikut menunjukkan contoh pengaturan file `.env` yang benar:
![env yang benar](/docs/env_old.png)

ketika di ubah env maka hasilnya terenkripsi seperti berikut:
![env yang terenkripsi](/docs/env_change.png)

> Pastikan ketika env diubah, server di-restart agar perubahan diterapkan.

## 6. Struktur Endpoint

| **Method** | **Endpoint**  | **Deskripsi**                |
| ------ | ----------------- | ---------------------------- |
| GET    | /api/biodata      | Ambil semua biodata          |
| GET    | /api/biodata/{id} | Ambil biodata berdasarkan ID |
| POST   | /api/biodata      | Tambah biodata               |
| PUT    | /api/biodata/{id} | Update biodata               |
| DELETE | /api/biodata/{id} | Hapus biodata                |

### **Format JSON POST/PUT**

```json
{
  "name": "John Doe",
  "email": "john@gmail.com",
  "phone": "08123456789",
  "address": "Jl. Merdeka No.1",
  "gender": "Laki-laki"
}
```

---

## 🔐 8. Penjelasan Kriptografi Simetris: Stream XOR

Aplikasi ini menggunakan **Stream XOR Encryption**, yaitu metode enkripsi simetris yang bekerja dengan:

```
cipher = plaintext XOR key
plaintext = cipher XOR key
```

### **Artinya:**

* Enkripsi dan dekripsi memakai kunci yang sama.
* Operasi XOR (bitwise exclusive OR) digunakan pada setiap karakter/byte.

### **Cara Kerja Singkat**

Jika:

```
plaintext = A
key = K
```

Maka:

```
cipher = A XOR K
```

Untuk membuka kembali:

```
plaintext = cipher XOR K
```

Karena XOR memiliki sifat unik:

```
(A XOR B) XOR B = A
```

### 8.1 Penjelasan Kode XOR Encryption

Berikut penjelasan fungsi Python yang digunakan dalam aplikasi untuk melakukan enkripsi dan dekripsi menggunakan metode **Stream XOR**.

```python
import base64

def xor_encrypt(text: str, key: str) -> str:
    if text is None:
        return None

    cipher_bytes = bytes([ord(c) ^ ord(key[i % len(key)]) for i, c in enumerate(text)])
    return base64.b64encode(cipher_bytes).decode()

def xor_decrypt(encoded_cipher: str, key: str) -> str:
    if encoded_cipher is None:
        return None

    cipher_bytes = base64.b64decode(encoded_cipher)
    original_chars = [chr(b ^ ord(key[i % len(key)])) for i, b in enumerate(cipher_bytes)]
    return ''.join(original_chars)
```

---

### **Penjelasan Fungsi `xor_encrypt`**

Fungsi ini mengubah plaintext menjadi ciphertext menggunakan operasi XOR.

#### **Langkah-langkah:**

1. **Cek input:** jika `text` adalah `None`, fungsi langsung mengembalikan `None`.
2. **Proses XOR:**

   ```python
   ord(c) ^ ord(key[i % len(key)])
   ```

   * `ord(c)` → mengubah karakter plaintext menjadi kode ASCII.
   * Kunci digunakan secara berulang dengan indeks `% len(key)`.
   * Hasil XOR menghasilkan byte terenkripsi.
3. **Konversi ke Base64:** ciphertext diubah menjadi string base64 agar aman disimpan di database.

---

### **Penjelasan Fungsi `xor_decrypt`**

Fungsi ini membuka kembali ciphertext menjadi plaintext.

#### **Langkah-langkah:**

1. Jika input `None`, langsung mengembalikan `None`.
2. **Decode Base64:**

   ```python
   cipher_bytes = base64.b64decode(encoded_cipher)
   ```
3. **Operasi XOR ulang:**

   ```python
   chr(b ^ ord(key[i % len(key)]))
   ```

   Karena XOR bersifat reversible, plaintext akan kembali.
4. Hasil karakter digabung menjadi string asli.


### **Inti Logika XOR dalam Kode**

* XOR memiliki sifat unik:
  **(A XOR B) XOR B = A**
* Dengan menggunakan kunci yang sama, proses enkripsi dan dekripsi akan menghasilkan teks asli kembali.
* Base64 hanya berperan sebagai pembungkus agar ciphertext berupa string yang dapat disimpan.



---

## 👍 Kelebihan Stream XOR

* Implementasi mudah
* Cocok untuk field pendek (email, nomor telepon)
* Kunci mudah diganti (cukup ubah APP_SECRET_XOR_KEY)
* Tidak membutuhkan library besar

## 👎 Kekurangan Stream XOR

* Tidak aman untuk data besar → pola XOR bisa ditebak
* Jika key terlalu pendek → bisa diprediksi
* Tidak cocok untuk data yang memerlukan enkripsi profesional-level

---

## 📌 9. Catatan Sistem

* Perubahan file `.env` membutuhkan restart server FastAPI.
* Jangan commit `.env` ke repository.
* Ganti `APP_SECRET` secara berkala.



