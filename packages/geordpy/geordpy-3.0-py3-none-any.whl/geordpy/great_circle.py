import numpy as np


def to_vec(*, lat, lon):
    cos_lat = np.cos(lat)
    cos_lon = np.cos(lon)
    sin_lat = np.sin(lat)
    sin_lon = np.sin(lon)
    return np.stack([cos_lat * cos_lon, cos_lat * sin_lon, sin_lat], axis=-1)


def batched_dot(a, b):
    a = np.expand_dims(a, 1)
    b = np.expand_dims(b, 2)
    return np.matmul(a, b).squeeze(-1).squeeze(-1)


def cos_distance(*, lat1, lat2, dlon):
    cos_lat1 = np.cos(lat1)
    sin_lat1 = np.sin(lat1)

    cos_lat2 = np.cos(lat2)
    sin_lat2 = np.sin(lat2)

    cos_dlon = np.cos(dlon)

    return sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_dlon


def cos_distance_segment(lat, lon, *, lat1, lon1, lat2, lon2, eps=1e-5):
    x = to_vec(lat=lat, lon=lon)
    a, b = to_vec(
        lat=np.stack([lat1, lat2], axis=0), lon=np.stack([lon1, lon2], axis=0)
    )

    n = np.cross(a, b)
    cos_gamma = np.dot(a, b)
    n /= max(np.sqrt((1.0 - cos_gamma) * (1.0 + cos_gamma)), np.nextafter(0.0, 1.0))

    s = x @ n

    sel = np.abs(s) < 1.0 - np.pi**2 / 8.0 * eps**2  # rel. error < eps
    s = np.expand_dims(s[sel], -1)

    c = np.ones_like(x) * b
    c[sel] = (x[sel] - np.outer(s, n)) / np.sqrt((1.0 - s) * (1.0 + s))

    cos_alpha = c @ b
    cos_beta = c @ a

    closest_point = np.ones_like(x) * b

    sel = cos_gamma < np.min((cos_alpha, cos_beta), axis=0)  # gamma < max(alpha, beta)
    closest_point[sel] = c[sel]

    sel = ~sel & (cos_beta >= cos_alpha)  # beta <= alpha
    closest_point[sel] = a

    return batched_dot(x, closest_point)
