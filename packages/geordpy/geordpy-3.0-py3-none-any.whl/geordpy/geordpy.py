from functools import partial

import numpy as np

from geordpy import great_circle, rhumb_line


def _filter(points, *, threshold, metric):
    n_points = points.shape[0]
    if n_points <= 2:
        return np.full(n_points, True)

    mask = np.full(n_points, True)
    stack = [(0, n_points - 1)]

    while stack:
        first, last = stack.pop()
        if last - first < 2:
            continue

        dist = metric(
            points[first + 1 : last, 0],
            points[first + 1 : last, 1],
            lat1=points[first, 0],
            lon1=points[first, 1],
            lat2=points[last, 0],
            lon2=points[last, 1],
        )
        i_max = np.argmax(dist) + 1  # dist[i] = dist(points[i+1], line seg.)
        dist_max = dist[i_max - 1]

        if dist_max < threshold:
            mask[first + 1 : last] = False
        else:
            stack.append((first, first + i_max))
            stack.append((first + i_max, last))

    return mask


def rdp_filter(
    points,
    threshold,
    radius=6_371_000,
    rhumb_line_interpolation=False,
    n_samples=2048,
    n_iterations=3,
):
    """
    Simplify a geodetic-coordinate polyline using the Ramer-Douglas-Peucker algorithm.

    This function applies the Ramer-Douglas-Peucker (RDP) algorithm to a list of geodetic-coordinate points,
    aiming to simplify the polyline while keeping the error below a specified threshold. The algorithm
    works by approximating the original polyline with a reduced number of points that lie close to the
    original curve. By default, the segments of the polyline are interpolated with a great-circle. Optionally,
    this can be changed to rhumb lines. For both options, the great-circle distance is used for finding the
    smallest distance between the interpolated segment and a given geodetic-coordinate point.

    Args:
        points (list of tuple): A list of latitude and longitude pairs (given in degrees) representing the
                               geodetic-coordinate polyline points to be simplified.

        threshold (float): The maximum allowable error, specified as an arc length along great circle segments.
                          Points that deviate from the simplified curve by more than this threshold will be kept.

        radius (float, optional): The radius of the sphere used for calculations. Defaults to Earth's mean radius
                                 in meters (6371000). The threshold is interpreted based on this radius.

        rhumb_line_interpolation (bool, optional): Interpolate the segments of the polyline with rhumb lines instead
                                                  of great-circle segments.

        n_samples (int, optional): Number of samples used to estimate the minimum distance between a rhumb line segment
                                  and a geodetic-coordinate.

        n_iterations (int, optional): Number of iterations used to estimate the minimum distance between a rhumb line
                                     segment and a geodetic-coordinate.

    Returns:
        list of bool: A binary mask indicating whether each point in the input list should be kept or discarded
                      based on the RDP simplification. The mask has the same length as the input 'points' list,
                      where a value of True indicates that the corresponding point should be kept, and False
                      indicates that the point can be discarded.

    Note:
        - The input 'points' list should have at least two points to define a valid polyline.
        - The value of 'threshold' must be greater than zero.
        - The 'radius' value should be set appropriately to match the units of the threshold. For example, if the
          radius is set to 1, then the threshold corresponds to the arc length on the unit sphere.
        - The values of 'threshold', 'n_samples', and 'n_iterations' must be greater than zero if provided.
        - The values of 'n_samples' and 'n_iterations' have no effect on the precision of the result if great-circles
          are used for interpolating segments of the polyline.
    """
    if len(points) == 0:
        return np.empty(0, dtype=bool)

    points = np.deg2rad(np.array(points))
    threshold = 1.0 - np.cos(threshold / radius)  # negate to make it a distance

    f = (
        great_circle.cos_distance_segment
        if not rhumb_line_interpolation
        else partial(
            rhumb_line.cos_distance_segment,
            n_samples=n_samples,
            n_iterations=n_iterations,
        )
    )

    return _filter(
        points,
        threshold=threshold,
        metric=lambda *args, **kwargs: 1 - f(*args, **kwargs),
    )
