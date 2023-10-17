# -*- coding: utf-8 -*-

from typing import Final

import cv2
from numpy.typing import NDArray

from cvlayer.cv.border import DEFAULT_BORDER_TYPE
from cvlayer.cv.depth import DEFAULT_OUTPUT_DEPTH, validate_depth_combinations

DEFAULT_KERNEL_SIZE: Final[int] = 1
"""
Aperture size used to compute the second-derivative filters.
See getDerivKernels for details.
The size must be positive and odd.
"""

DEFAULT_SCALE: Final[float] = 1.0
"""
scale factor for the computed Laplacian values.
By default, no scaling is applied.
See getDerivKernels for details.
"""

DEFAULT_DELTA: Final[float] = 0.0
"""delta value that is added to the results prior to storing them in dst."""


def laplacian(
    src: NDArray,
    output_depth=DEFAULT_OUTPUT_DEPTH,
    kernel_size=DEFAULT_KERNEL_SIZE,
    scale=DEFAULT_SCALE,
    delta=DEFAULT_DELTA,
    border_type=DEFAULT_BORDER_TYPE,
) -> NDArray:
    assert kernel_size % 2 == 1
    assert kernel_size >= 1

    validate_depth_combinations(src.dtype, output_depth.value)

    if border_type.value == cv2.BORDER_WRAP:
        raise ValueError("Unsupported border type: BORDER_WRAP")

    return cv2.Laplacian(
        src=src,
        ddepth=output_depth.value,
        dst=None,
        ksize=kernel_size,
        scale=scale,
        delta=delta,
        borderType=border_type.value,
    )


class CvlLaplacian:
    @staticmethod
    def cvl_laplacian(
        src: NDArray,
        output_depth=DEFAULT_OUTPUT_DEPTH,
        kernel_size=DEFAULT_KERNEL_SIZE,
        scale=DEFAULT_SCALE,
        delta=DEFAULT_DELTA,
        border_type=DEFAULT_BORDER_TYPE,
    ):
        return laplacian(src, output_depth, kernel_size, scale, delta, border_type)
