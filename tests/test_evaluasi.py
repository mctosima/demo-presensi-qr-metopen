"""Kode evaluasi riset juga diuji: angka di Bab 4 dihitung dari sini."""

import pytest

from presensi.evaluasi import proporsi, tingkat_lolos_curang, tingkat_tolak_sah


def test_angka_data_pilot():
    # Data pilot slide P10: QR statis vs QR dinamis + geofence
    assert tingkat_lolos_curang(18, 20) == pytest.approx(0.90)
    assert tingkat_lolos_curang(3, 20) == pytest.approx(0.15)
    assert tingkat_tolak_sah(1, 100) == pytest.approx(0.01)
    assert tingkat_tolak_sah(9, 100) == pytest.approx(0.09)


@pytest.mark.parametrize("kejadian, total", [(1, 0), (-1, 10), (11, 10)])
def test_tolak_masukan_tidak_masuk_akal(kejadian, total):  # uji negatif
    with pytest.raises(ValueError):
        proporsi(kejadian, total)
