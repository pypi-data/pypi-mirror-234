import numpy as np


def hist_quantile(vals, q, bins_edges=None):
    """Compute quantiles of bands histograms"""
    cm = np.zeros_like(vals)
    for i, v in enumerate(vals):
        if i == 0:
            val = v
        else:
            val = v + cm[i - 1]
        cm[i] = val

        if val >= q:
            if bins_edges is not None:
                return bins_edges[i]
            else:
                return i

def hist_mean_std(bin_midpoints, probabilities):
    # Check if the input lengths are valid
    if len(bin_midpoints) != len(probabilities):
        raise ValueError("bin_midpoints and probabilities should have the same length")

    # Calculate mean
    mean = sum(x * p for x, p in zip(bin_midpoints, probabilities))

    # Calculate variance
    variance = sum(p * (x - mean) ** 2 for x, p in zip(bin_midpoints, probabilities))

    # Standard deviation is the square root of variance
    std = variance ** 0.5

    return mean, std