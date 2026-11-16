"""Kode evaluasi riset: menghitung metrik dari data pilot.

Kode evaluasi juga harus diuji. Salah hitung di sini = salah kesimpulan di Bab 4.
"""


def proporsi(kejadian: int, total: int) -> float:
    """Proporsi kejadian dari total, mis. 18 titip absen lolos dari 20 -> 0.9."""
    if total <= 0:
        raise ValueError("total harus lebih dari 0")
    if not 0 <= kejadian <= total:
        raise ValueError("kejadian harus di antara 0 dan total")
    return kejadian / total


def tingkat_lolos_curang(lolos: int, total_curang: int) -> float:
    """Proporsi presensi curang (titip absen) yang diterima sistem. Makin kecil makin baik."""
    return proporsi(lolos, total_curang)


def tingkat_tolak_sah(ditolak: int, total_sah: int) -> float:
    """Proporsi mahasiswa yang benar-benar hadir tetapi ditolak sistem. Makin kecil makin baik."""
    return proporsi(ditolak, total_sah)
