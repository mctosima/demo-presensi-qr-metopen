# Instruksi untuk agen AI (GitHub Copilot)

- Bahasa kode dan komentar: Indonesia. Fungsi di `presensi/`, uji di `tests/`.
- Setiap fungsi baru WAJIB disertai uji pytest, termasuk **uji nilai batas** dan **uji negatif**.
- Turunkan kasus uji dari **kriteria penerimaan di issue**, bukan dari implementasi yang Anda tulis.
- Jangan mengubah atau menghapus uji yang sudah ada agar lulus. Bila uji lama perlu berubah, jelaskan alasannya di deskripsi PR.
- Jalankan `pytest` sebelum menyelesaikan pekerjaan; semua uji harus lulus.
