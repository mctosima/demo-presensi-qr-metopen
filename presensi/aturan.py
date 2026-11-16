"""Aturan presensi yang menjadi *perlakuan* dalam riset QR dinamis.

Rancangan (lihat RQ di README):
- QR berlaku sejak dibuat sampai tepat 30 detik (inklusif).
- Mahasiswa harus berada paling jauh 50 m dari titik ruang kelas (inklusif).
"""

import math

MASA_BERLAKU_QR = 30  # detik
RADIUS_GEOFENCE = 50.0  # meter
JARI_JARI_BUMI = 6_371_000  # meter


def qr_masih_berlaku(waktu_dibuat: float, waktu_pindai: float,
                     masa_berlaku: float = MASA_BERLAKU_QR) -> bool:
    """True bila QR dipindai paling lambat `masa_berlaku` detik setelah dibuat."""
    if waktu_pindai < waktu_dibuat:
        raise ValueError("waktu pindai tidak boleh sebelum QR dibuat")
    return waktu_pindai - waktu_dibuat <= masa_berlaku


def jarak_meter(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Jarak dua titik GPS (rumus haversine), dibulatkan ke sentimeter."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    jarak = 2 * JARI_JARI_BUMI * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(jarak, 2)


def dalam_geofence(lat: float, lon: float, lat_kelas: float, lon_kelas: float,
                   radius: float = RADIUS_GEOFENCE) -> bool:
    """True bila posisi mahasiswa paling jauh `radius` meter dari ruang kelas."""
    return jarak_meter(lat, lon, lat_kelas, lon_kelas) <= radius


def presensi_sah(waktu_dibuat: float, waktu_pindai: float,
                 lat: float, lon: float, lat_kelas: float, lon_kelas: float) -> bool:
    """Presensi diterima bila QR masih berlaku DAN posisi di dalam geofence."""
    return (qr_masih_berlaku(waktu_dibuat, waktu_pindai)
            and dalam_geofence(lat, lon, lat_kelas, lon_kelas))
