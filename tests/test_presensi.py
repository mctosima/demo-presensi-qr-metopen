"""Uji integrasi: kedua aturan harus terpenuhi bersamaan."""

from presensi.aturan import presensi_sah
from tests.test_geofence import LAT_KELAS, LON_KELAS, geser_ke_utara


def test_di_kelas_dan_qr_berlaku_diterima():
    assert presensi_sah(0, 10, LAT_KELAS, LON_KELAS, LAT_KELAS, LON_KELAS)


def test_qr_kedaluwarsa_ditolak_walau_di_kelas():
    assert not presensi_sah(0, 45, LAT_KELAS, LON_KELAS, LAT_KELAS, LON_KELAS)


def test_qr_berlaku_tetapi_di_luar_geofence_ditolak():
    lat_kos = geser_ke_utara(LAT_KELAS, 500)
    assert not presensi_sah(0, 10, lat_kos, LON_KELAS, LAT_KELAS, LON_KELAS)
