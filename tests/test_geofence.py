"""Verifikasi: geofence menerima <= 50 m dan menolak > 50 m (uji nilai batas)."""

import math

import pytest

from presensi.aturan import JARI_JARI_BUMI, dalam_geofence, jarak_meter

# Titik contoh ruang kelas (koordinat ilustrasi di sekitar kampus ITERA)
LAT_KELAS, LON_KELAS = -5.3580, 105.3140


def geser_ke_utara(lat, meter):
    """Lintang baru setelah bergeser `meter` ke utara (bujur tetap)."""
    return lat + math.degrees(meter / JARI_JARI_BUMI)


def test_jarak_titik_yang_sama_nol():
    assert jarak_meter(LAT_KELAS, LON_KELAS, LAT_KELAS, LON_KELAS) == 0


def test_jarak_satu_derajat_bujur_di_khatulistiwa():
    # 1 derajat di khatulistiwa = 2*pi*R/360, sekitar 111,19 km
    assert jarak_meter(0, 0, 0, 1) == pytest.approx(111_194.93, abs=0.01)


@pytest.mark.parametrize("meter, diharapkan", [
    (0, True),
    (49, True),
    (50, True),    # tepat di batas (inklusif)
    (51, False),
    (500, False),  # di kos, bukan di kelas
])
def test_batas_geofence(meter, diharapkan):
    lat = geser_ke_utara(LAT_KELAS, meter)
    assert dalam_geofence(lat, LON_KELAS, LAT_KELAS, LON_KELAS) is diharapkan
