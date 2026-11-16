# demo-presensi-qr-metopen

> **Proyek contoh untuk keperluan perkuliahan.** Repositori ini dibuat khusus untuk mata kuliah
> **Metodologi Penelitian (IF25-41029)**, Program Studi Teknik Informatika, Institut Teknologi Sumatera (ITERA),
> Semester Ganjil 2026/2027, **Pertemuan 10: Verifikasi, Validasi, Pengujian (VV&T) & Test Plan**.
> Ini **bukan** sistem presensi resmi ITERA dan tidak dipakai untuk presensi sungguhan.
> Kasus, aturan, koordinat, dan angka data pilot di dalamnya adalah **ilustrasi** untuk latihan di kelas.

Tujuannya menunjukkan, dari **perspektif riset**, bagaimana:

1. **Verifikasi** (apakah perlakuan riset diimplementasikan sesuai rancangan) ditulis sebagai uji `pytest`;
2. uji itu dijalankan **otomatis** oleh **GitHub Actions** setiap push dan pull request;
3. **agen AI** (GitHub Copilot cloud agent atau agen lokal) boleh membantu menulis kode, tetapi tetap dijaga oleh uji dan tinjauan peneliti.

Materi pendamping: slide Pertemuan 10 di halaman kuliah [mctm.web.id/metopen](https://mctm.web.id/metopen).

## Konteks riset

Titip absen marak karena foto QR statis dibagikan lewat WhatsApp. Riset ini menguji sebuah *perlakuan*:
**QR dinamis** (berlaku 30 detik) + **geofence** (≤ 50 m dari ruang kelas).

> **RQ:** Apakah QR dinamis + geofence menurunkan presensi curang dibanding QR statis,
> tanpa banyak menolak mahasiswa yang benar-benar hadir?

Repositori ini **tidak** menjawab RQ. Repositori ini memastikan bahwa **perlakuan diimplementasikan sesuai rancangan**
(verifikasi) dan bahwa **kode evaluasi menghitung metrik dengan benar**. Menjawab RQ adalah urusan *validasi*: eksperimen di kelas nyata.

| Berkas | Isi |
|---|---|
| `presensi/aturan.py` | Aturan perlakuan: `qr_masih_berlaku`, `jarak_meter`, `dalam_geofence`, `presensi_sah` |
| `presensi/evaluasi.py` | Kode evaluasi riset: `tingkat_lolos_curang`, `tingkat_tolak_sah` |
| `tests/` | Uji unit (nilai batas + negatif), uji integrasi, uji kode evaluasi |
| `.github/workflows/uji.yml` | Menjalankan `pytest` otomatis setiap push dan pull request |
| `.github/copilot-instructions.md` | Aturan main untuk agen AI di repositori ini |
| `DEMO.md` | Naskah demo kelas langkah demi langkah (untuk dosen/asisten) |

---

## Langkah 1 — Jalankan uji di laptop

```bash
git clone https://github.com/mctosima/demo-presensi-qr-metopen.git
cd demo-presensi-qr-metopen
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
```

Hasil yang diharapkan: `20 passed`.

Pakai `uv`? Cukup: `uv run --with pytest pytest`.

## Langkah 2 — Pahami jenis uji yang ada

| Uji | Contoh di repo | Konsep P10 |
|---|---|---|
| Nilai batas | QR dipindai di detik **29 / 30 / 31**; jarak **49 / 50 / 51 m** | Batas ditulis tepat di tepi rentang |
| Negatif | Waktu pindai sebelum QR dibuat; `proporsi(1, 0)` | Masukan buruk harus ditolak |
| Integrasi | `presensi_sah` = QR berlaku **dan** di dalam geofence | Sambungan antaraturan |
| Kode evaluasi | `tingkat_lolos_curang(18, 20) == 0.90` | Angka di Bab 4 dihitung dengan benar |

Buka `tests/test_qr.py`: setiap baris `parametrize` adalah satu **kasus uji** dengan **hasil yang diharapkan**, persis seperti tabel test plan.

## Langkah 3 — Aktifkan GitHub Actions

1. Buat repositori sendiri: **Use this template** / fork, atau `gh repo create` lalu `git push`.
2. Berkas `.github/workflows/uji.yml` sudah ada, sehingga GitHub langsung menjalankannya setelah push.
3. Buka tab **Actions** → run `uji` → harus **hijau** (✓).

```yaml
on:
  push:
    branches: [main]
  pull_request:
jobs:
  uji:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install -r requirements-dev.txt
      - run: pytest
```

## Langkah 4 — Lihat CI menangkap bug

```bash
git switch -c refactor/cek-qr
# di presensi/aturan.py ubah  <=  menjadi  <  pada qr_masih_berlaku
git commit -am "refactor(qr): sederhanakan cek masa berlaku"
git push -u origin refactor/cek-qr
gh pr create --fill
gh pr checks --watch
```

Hasil yang diharapkan: run **merah** (✗), gagal di `test_batas_masa_berlaku[30-True]`.
Artinya mahasiswa yang memindai tepat di detik ke-30 akan **ditolak**, sehingga *tingkat tolak sah* di eksperimen ikut naik.
Bug kecil di kode = **ancaman validitas** pada hasil riset. Kembalikan `<=`, push lagi, dan run kembali **hijau**.

## Langkah 5 — Larang merge bila uji merah

**Settings → Rules → Rulesets → New ruleset → New branch ruleset**

- *Enforcement status*: **Active**
- *Target branches*: **Include default branch**
- Centang **Require a pull request before merging**
- Centang **Require status checks to pass** → **Add checks** → pilih **`uji`**
- **Create**

Sekarang tombol merge terkunci selama uji gagal.

## Langkah 6 — Minta agen AI mengerjakan issue (Copilot cloud agent)

Membutuhkan paket GitHub Copilot yang menyertakan agen cloud. Cek apakah **Copilot** muncul di daftar *Assignees* sebuah issue.

1. **Issues → New issue**, tulis issue dengan **kriteria penerimaan** yang terukur, contoh:

   > **Judul:** Validasi format NIM sebelum presensi dicatat
   >
   > Tambahkan fungsi `nim_valid(nim: str) -> bool` di `presensi/aturan.py`.
   >
   > **Kriteria penerimaan**
   > - Diterima: tepat 9 digit angka, mis. `"122140001"`.
   > - Spasi di awal/akhir dibuang sebelum diperiksa.
   > - Ditolak: 8 digit, 10 digit, mengandung huruf/spasi di tengah/tanda baca, string kosong.
   > - Ada uji pytest untuk **setiap** kriteria, termasuk nilai batas 8 / 9 / 10 digit.
   > - Uji lama tidak boleh diubah.

2. Di sidebar issue: **Assignees → Copilot**. Pada dialog *Assign to Copilot* boleh menambah *Optional prompt*, lalu konfirmasi.
3. Copilot membuat **draft pull request** dan mengerjakannya di latar belakang (beberapa menit).
4. Di PR tersebut workflow **tidak berjalan otomatis**. Klik **Approve and run workflows** di kotak merge.
5. **Tinjau** perubahannya (lihat bagian berikut). Minta revisi dengan berkomentar di PR, misalnya:
   `@copilot tambahkan uji untuk NIM "12214 0001" (spasi di tengah) yang harus ditolak`.
6. Merge **hanya** bila uji hijau **dan** uji tersebut memang mencerminkan kriteria penerimaan.

### Alternatif: agen lokal

Bila agen cloud tidak tersedia, pakai agen di editor/terminal (mis. **Copilot agent mode** di VS Code atau **Claude Code**) dengan prompt yang sama:

```text
Baca .github/copilot-instructions.md. Kerjakan issue berikut: <tempel isi issue>.
Tulis ujinya dulu dari kriteria penerimaan, jalankan pytest, baru tulis fungsinya.
Jangan mengubah uji yang sudah ada.
```

Lalu jalankan `pytest` sendiri, commit, push ke branch baru, buat PR, dan biarkan GitHub Actions memeriksa.

### Checklist meninjau kerja agen AI

- [ ] Setiap kriteria penerimaan punya **minimal satu uji**, termasuk batas 8 / 9 / 10 digit.
- [ ] Hasil yang diharapkan di uji berasal dari **spesifikasi**, bukan disalin dari keluaran fungsi.
- [ ] **Tidak ada uji lama** yang diubah, dilonggarkan, atau dihapus.
- [ ] Tidak ada `skip`/`xfail` yang diselipkan.
- [ ] Anda bisa menjelaskan setiap baris kode yang akan di-merge.
- [ ] Penggunaan AI dicatat untuk *AI Disclosure Statement* (Pertemuan 11).

**CI hijau ≠ hipotesis terbukti.** CI hanya membuktikan kode sesuai uji. Apakah ujinya benar, dan apakah perlakuannya berhasil di kelas nyata, tetap tanggung jawab peneliti.

---

## Latihan mandiri

1. Tambahkan aturan: QR **ditolak bila NIM sudah presensi** di sesi yang sama. Tulis ujinya dulu.
2. Tambahkan fungsi evaluasi `selisih_proporsi(a, b)` beserta uji untuk data pilot (90% → 15%).
3. Ubah `uji.yml` agar menguji di Python 3.10 dan 3.12 sekaligus (`strategy.matrix`).

Lisensi: MIT. Dibuat oleh Tim Dosen Metodologi Penelitian, Teknik Informatika ITERA, untuk keperluan perkuliahan.
