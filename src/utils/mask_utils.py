import cv2
import numpy as np


def combine_masks(dimensions: tuple[int, int], *masks: np.ndarray) -> np.ndarray:
    """Combines the provided masks into a single mask."""
    combined_mask = np.zeros(dimensions, dtype=np.uint8)

    for mask in masks:
        combined_mask = cv2.bitwise_or(combined_mask, mask)

    return combined_mask
