import numpy as np

from geordpy import rdp_filter


def run_example():
    points = [
        (0, 0),
        (-10, 10),
        (10, 20),
        (-20, 30),
        (20, 40),
        (-10, 50),
        (10, 60),
        (0, 70),
    ]

    radius = 1000

    mask = rdp_filter(points, threshold=0, radius=radius)
    assert all(mask)

    mask = rdp_filter(points, threshold=350, radius=radius)
    assert all(mask == [True, False, False, False, False, False, False, True])

    threshold = 346
    mask = rdp_filter(points, threshold=threshold, radius=radius)
    assert all(mask == [True, False, False, True, True, False, False, True])

    print(np.array(points)[mask])


if __name__ == "__main___":
    run_example()  # pragma: no cover
