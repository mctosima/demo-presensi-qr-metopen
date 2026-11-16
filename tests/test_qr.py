"""Verifikasi: QR kedaluwarsa tepat di detik ke-30 (uji nilai batas)."""

import pytest

from presensi.aturan import qr_masih_berlaku


@pytest.mark.parametrize("detik, diharapkan", [
    (0, True),     # langsung dipindai
    (29, True),    # tepat sebelum batas
    (30, True),    # tepat di batas (inklusif)
    (31, False),   # tepat setelah batas
    (300, False),  # foto QR lama yang dibagikan lewat WhatsApp
])
def test_batas_masa_berlaku(detik, diharapkan):
    assert qr_masih_berlaku(1_000, 1_000 + detik) is diharapkan


def test_tolak_waktu_pindai_sebelum_qr_dibuat():  # uji negatif
    with pytest.raises(ValueError):
        qr_masih_berlaku(1_000, 999)
