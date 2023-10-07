import numpy as np


def refine_bounds(f, *, bounds, n_samples):
    a, b = bounds
    x = np.linspace(a, b, n_samples, axis=0)
    y = f(x)

    i = np.argmin(y, axis=0)
    low = np.maximum(0, i - 1)
    high = np.minimum(n_samples - 1, i + 1)

    return np.take_along_axis(x, np.stack((low, high), axis=0), axis=0)


def minimize(f, *, bounds, n_iterations, n_samples):
    for _ in range(n_iterations):
        bounds = refine_bounds(f, bounds=bounds, n_samples=n_samples)

    y = f(bounds)
    return np.min(y, axis=0)


def igd(x):
    return np.arcsinh(np.tan(x))


def cos_distance(*, sin_latA, sin_latB, cos_latA, cos_latB, cos_lonAB):
    return sin_latA * sin_latB + cos_latA * cos_latB * cos_lonAB


def cos_distance_lon(x, *, lat, lon, lat1, lat2, lon1, lon2):
    igd_lat1 = igd(lat1)
    igd_lat2 = igd(lat2)

    igd_latB = igd_lat1 + (x - lon1) / (lon2 - lon1) * (igd_lat2 - igd_lat1)

    return cos_distance(
        cos_latA=np.cos(lat),
        sin_latA=np.sin(lat),
        cos_latB=1.0 / np.cosh(igd_latB),
        sin_latB=np.tanh(igd_latB),
        cos_lonAB=np.cos(lon - x),
    )


def cos_distance_lat(x, *, lat, lon, lat1, lat2, lon1, lon2):
    igd_x = igd(x)
    igd_lat1 = igd(lat1)
    igd_lat2 = igd(lat2)

    lonB = lon1 + (igd_x - igd_lat1) / (igd_lat2 - igd_lat1) * (lon2 - lon1)

    return cos_distance(
        cos_latA=np.cos(lat),
        sin_latA=np.sin(lat),
        cos_latB=np.cos(x),
        sin_latB=np.sin(x),
        cos_lonAB=np.cos(lon - lonB),
    )


def cos_distance_segment(
    lat, lon, *, lat1, lon1, lat2, lon2, n_iterations, n_samples, eps=1e-10
):
    lat12 = abs(lat1 - lat2)
    lon12 = abs(np.arctan2(np.sin(lon1 - lon2), np.cos(lon1 - lon2)))

    if max(lat12, lon12) < eps:
        return cos_distance(
            sin_latA=np.sin(lat),
            sin_latB=np.sin(lat2),
            cos_latA=np.cos(lat),
            cos_latB=np.cos(lat2),
            cos_lonAB=np.cos(lon12),
        )

    if lat12 < lon12:
        f = cos_distance_lon
        bounds = np.full_like(lon, lon1), np.full_like(lon, lon2)
    else:
        f = cos_distance_lat
        bounds = np.full_like(lat, lat1), np.full_like(lat, lat2)

    return -minimize(
        lambda x: -f(x, lat=lat, lon=lon, lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2),
        bounds=bounds,
        n_iterations=n_iterations,
        n_samples=n_samples,
    )
