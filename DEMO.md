# Naskah Demo Kelas — Uji Otomatis & Agen AI (±20 menit)

Metodologi Penelitian IF25-41029, Pertemuan 10. Dipakai setelah latihan individu QR dinamis.
Pesan inti: **uji otomatis adalah bukti verifikasi yang tercatat; agen AI boleh menulis kode, tetapi peneliti yang menentukan ujinya.**

---

## A. Persiapan (H-1)

| # | Langkah | Cek |
|---|---|---|
| 1 | Repo publik `mctosima/demo-presensi-qr-metopen` sudah ada dan `main` ter-push | Tab **Actions**: run `uji` hijau |
| 2 | Ruleset proteksi `main`: *Require status checks to pass* → `uji` (README Langkah 5) | Tombol merge PR merah terkunci |
| 3 | Buat **Issue #1** "Validasi format NIM sebelum presensi dicatat" (teks di README Langkah 6). **Jangan di-assign dulu.** | Issue terbuka |
| 4 | Pastikan **Copilot** muncul di *Assignees* issue | Bila tidak ada → pakai Rencana B |
| 5 | **Gladi** Langkah 3: `/demo-refaktor-qr bug` → `perbaiki` → `reset`. Lalu assign issue cadangan (#2, isi sama) ke Copilot, tunggu PR selesai, ambil tangkapan layar PR + diff + hasil Actions, lalu tutup PR & issue #2 | Tangkapan layar tersimpan |
| 6 | Laptop: clone repo, `.venv` siap, `pytest` → `20 passed`; `gh auth status` OK | Terminal & VS Code font besar |
| 7 | Tab browser: repo, Actions, Issue #1, Settings → Rules | — |

## B. Alur di kelas

### Langkah 0 — Jalankan agen saat latihan dimulai (1 menit, slide 33)
Lakukan di **menit 1–2 latihan individu** (slide 33), ketika mahasiswa sudah mulai mengerjakan; jangan proyeksikan layar.
Buka Issue #1 → **Assignees → Copilot** → (opsional prompt: *"Ikuti .github/copilot-instructions.md"*) → konfirmasi.
Agen punya ±45 menit sampai slide 50, jadi draft PR biasanya sudah siap saat demo.
Bila Copilot tidak muncul di Assignees, lewati langkah ini dan pakai Rencana B (bagian C).

### Langkah 1 — Dari latihan ke kode (3 menit)
1. Buka `presensi/aturan.py`: tunjukkan `MASA_BERLAKU_QR = 30`, `RADIUS_GEOFENCE = 50.0`, dan operator `<=`.
2. Buka `tests/test_qr.py` dan `tests/test_geofence.py`: kasus **29 / 30 / 31 detik** dan **49 / 50 / 51 m**.
   > "Ini jawaban soal 2 latihan tadi: uji nilai batas sebagai **verifikasi**, ditulis sebagai kode."
3. Buka `tests/test_evaluasi.py`: `tingkat_lolos_curang(18, 20) == 0.90`.
   > "Kode yang menghitung angka Bab 4 juga harus diuji."
4. Terminal: `pytest` → **20 passed**.

### Langkah 2 — Workflow GitHub Actions (2 menit)
1. Buka `.github/workflows/uji.yml`: `on` (kapan), `runs-on` (mesin bersih di server GitHub), empat `steps`.
2. Tab **Actions** → run terakhir → hijau.
   > "Setiap push diuji di mesin bersih, bukan hanya 'jalan di laptop saya'. Riwayatnya tersimpan dan bisa diaudit pembimbing."

### Langkah 3 — CI menangkap bug buatan agen AI (5 menit)
Di terminal kedua, sesi Claude Code sudah terbuka di folder repo (perintah lokal dosen `/demo-refaktor-qr`, di luar repo ini).

```text
/demo-refaktor-qr bug        # agen "merapikan" qr_masih_berlaku, push, buka PR, pantau CI
/demo-refaktor-qr perbaiki   # agen membaca log CI, memperbaiki kode (bukan uji), CI hijau
/demo-refaktor-qr reset      # setelah kelas/gladi: tutup PR tanpa merge, hapus branch
```
1. Tunjukkan diff agen: `<=` menjadi `<`, dan klaim PR *"Tidak ada perubahan perilaku."*
2. Tunjukkan run **merah** dan log: `FAILED tests/test_qr.py::test_batas_masa_berlaku[30-True]`, serta tombol merge yang **terkunci** oleh ruleset.
3. **Tanya kelas:** *"Kalau bug ini lolos ke eksperimen, metrik mana yang berubah?"*
   → Mahasiswa yang memindai tepat di detik ke-30 ditolak, sehingga **tingkat tolak sah naik**. Kesimpulan riset bisa salah karena implementasi, bukan karena perlakuannya. Itu **ancaman validitas internal**.
4. `perbaiki`: agen memperbaiki **kode**, bukan uji (uji = spesifikasi), menjalankan `pytest` dulu, lalu push → run **hijau**. PR tidak di-merge.
5. Jujur ke kelas: skenario disiapkan agar bug pasti muncul, tetapi salah satu angka di nilai batas (*off-by-one*) adalah kesalahan nyata yang umum, pada manusia maupun agen. Klaim agen bukan bukti; uji yang lulus adalah bukti.

Cadangan manual (tanpa agen):
```bash
git switch -c refactor/cek-qr
# edit presensi/aturan.py: ubah  <=  menjadi  <  di qr_masih_berlaku
git commit -am "refactor(qr): sederhanakan cek masa berlaku"
git push -u origin refactor/cek-qr
gh pr create --fill
gh pr checks --watch
```

### Langkah 4 — Meninjau kerja agen AI (6 menit)
1. Buka PR dari Copilot (tertaut di timeline Issue #1). Bila belum selesai, pakai tangkapan layar gladi.
2. Tunjukkan workflow **belum berjalan** → klik **Approve and run workflows**.
   > "GitHub sengaja meminta manusia menyetujui. Kode dari agen tidak langsung dipercaya."
3. Tinjau diff bersama kelas dengan checklist (README):
   - Apakah ada uji untuk **8 / 9 / 10 digit**, huruf, spasi di tengah, string kosong, spasi di tepi?
   - Apakah hasil yang diharapkan berasal dari **issue**, atau sekadar menyalin perilaku fungsi?
   - Apakah ada uji lama yang diubah?
4. Bila ada kriteria yang belum diuji, berkomentar di PR:
   `@copilot tambahkan uji untuk NIM "12214 0001" (spasi di tengah) yang harus ditolak`
   (agen menanggapi dengan reaksi 👀 lalu menambah commit; lanjutkan diskusi sambil menunggu).

### Langkah 5 — Penutup diskusi (3 menit)
- **CI hijau ≠ hipotesis terbukti.** CI = verifikasi. Hipotesis dijawab oleh eksperimen (validasi).
- Agen AI boleh menulis kode dan uji, tetapi **peneliti yang bertanggung jawab** atas *oracle* uji: hasil yang diharapkan harus berasal dari spesifikasi/kriteria.
- Penggunaan agen dicatat di **AI Disclosure Statement** (Pertemuan 11).
- Untuk TA: uji minimal fungsi metrik, pembagian data (tidak ada ID yang sama di latih dan uji), dan pemuatan konfigurasi.

## C. Rencana B

| Masalah | Tindakan |
|---|---|
| Copilot tidak muncul di *Assignees* / kuota habis | Pakai agen lokal (Copilot agent mode di VS Code atau Claude Code) dengan prompt di README, lalu push branch & buat PR sendiri |
| Agen terlalu lama | Lanjut ke Langkah 5, tunjukkan tangkapan layar gladi; buka PR lagi di akhir kelas |
| Internet lambat | Jalankan Langkah 3 secara lokal saja (`pytest` merah → perbaiki → hijau) + tangkapan layar Actions |

## D. Setelah kelas
- Tutup/merge PR Copilot sesuai hasil tinjauan; hapus branch demo.
- Untuk kelas berikutnya: buka kembali Issue #1 (atau buat ulang) dan pastikan `main` hijau.
