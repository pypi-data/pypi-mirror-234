from dataclasses import dataclass
import typing

import matplotlib.pyplot as plt
import numpy as np
import scipy

from interpret.glassbox._ebm._utils import convert_to_intervals

###################################################################################################
# Put individual graphs to text
# Also has a datatype for graphs and various simple operations on this datatype.
###################################################################################################


# a low-level datastructure for the graphs of explainable boosting machines
@dataclass
class EBMGraph:
    feature_name: str
    feature_type: str
    x_vals: typing.List[
        typing.Tuple[float, float]
    ]
    scores: typing.List[float]
    stds: typing.List[float]


def extract_graph(
    ebm,
    feature_index,
    normalization="none",
    use_feature_bounds=True,
):
    """Extract a graph from an Explainable Boosting Machine.

    This is a low-level function.
    The purpose of this function is to extract the graph from the intervals of the EBM and return it in an easy format.

    :param ebm:
    :param feature_index:
    :param normalization: how to normalize the graph. possible values are: 'mean', 'min', 'none'
    :param use_feature_bounds: if True, the first and last bin are min and max value of the feature stored in the EBM. If false, the first and last value are -inf and inf, respectively.
    :return: EBMGraph
    """

    # read the variables from the ebm
    feature_name = ebm.feature_names_in_[feature_index]
    feature_type = ebm.feature_types_in_[feature_index]
    scores = ebm.term_scores_[feature_index][1:-1]  # Drop missing and unknown bins
    stds = ebm.standard_deviations_[feature_index][1:-1]

    # normalize the graph
    normalization_constant = None
    if normalization == "mean":
        normalization_constant = np.mean(scores)
    elif normalization == "min":
        normalization_constant = np.min(scores)
    elif normalization == "none":
        normalization_constant = 0
    else:
        raise Exception(f"Unknown normalization {normalization}")
    scores = scores - normalization_constant

    # read the x-axis bins from the ebm
    if feature_type == "continuous":
        x_vals = convert_to_intervals(ebm.bins_[feature_index][0])
        # feature bounds apply to continuous features only
        if use_feature_bounds:
            x_vals[0] = (ebm.feature_bounds_[feature_index][0], x_vals[0][1])
            x_vals[-1] = (x_vals[-1][0], ebm.feature_bounds_[feature_index][1])
    elif feature_type == "nominal":
        x_vals = ebm.bins_[feature_index][0]
        x_vals = {v - 1: k for k, v in x_vals.items()}
        x_vals = [x_vals[idx] for idx in range(len(x_vals.keys()))]
    else:
        raise Exception(
            f"Feature {feature_index} is of unknown feature_type {feature_type}."
        )
    assert len(x_vals) == len(scores), "The number of bins and scores does not match."

    return EBMGraph(feature_name, feature_type, x_vals, scores, stds)


def simplify_graph(graph: EBMGraph, min_variation_per_cent: float = 0.0):
    """Simplifies a graph. Removes redundant (flat) bins from the graph.

    With min_variation_per_cent>0 (default 0.0), the function simplifies the graph by removing bins
    that correspond to a less that min_variation_per_cent change in the score, considering the overal min/max difference of score for the feature as 100%.
    this can be useful to keep a query within the context limit. Empirically, removing changes of less than 2% simplifies graphs a lot
    in terms of the number of bins/tokens, but visually we can hardly see the difference.

    :param bins:
    :param scores:
    :return: EBMGraph. A new simplified graph.
    """
    assert graph.feature_type == "continuous", "Can only simplify continuous graphs."
    x_vals, scores, stds = graph.x_vals, graph.scores, graph.stds
    total_variation = np.max(scores) - np.min(scores)
    new_x_vals, new_scores, new_stds = [], [], []
    for idx, (b0, b1) in enumerate(x_vals):
        if idx == 0:
            new_x_vals.append((b0, b1))
            new_scores.append(scores[idx])
            new_stds.append(stds[idx])
        else:
            score_prev = new_scores[-1]
            if (
                np.abs(float(score_prev) - float(scores[idx]))
                <= total_variation * min_variation_per_cent
            ):
                # extend the previous bin to b1
                new_x_vals[-1] = (new_x_vals[-1][0], b1)
                # guarantee that the the confidence bands of the simplified graph cover the original graph as well as its confidence bands
                new_stds[-1] = max(new_stds[-1], stds[idx])
            else:
                new_x_vals.append((b0, b1))
                new_scores.append(scores[idx])
                new_stds.append(stds[idx])
    return EBMGraph(
        graph.feature_name, graph.feature_type, new_x_vals, new_scores, new_stds
    )


def plot_graph(graph: EBMGraph):
    x_vals, scores, stds = graph.x_vals, graph.scores, graph.stds
    if graph.feature_type == "continuous":
        x, y, y_lower, y_upper = [], [], [], []
        for idx, bin in enumerate(x_vals):
            if bin[0] == -np.inf or bin[1] == np.inf:
                continue
            # left part of the bin
            x.append(bin[0] + 1e-12)
            y.append(scores[idx])
            y_lower.append(scores[idx] - stds[idx])
            y_upper.append(scores[idx] + stds[idx])
            # right part of the bin
            x.append(bin[1])
            y.append(scores[idx])
            y_lower.append(scores[idx] - stds[idx])
            y_upper.append(scores[idx] + stds[idx])
        # plot
        fig = plt.figure()
        plt.plot(x, y)
        plt.fill_between(x, y_lower, y_upper, alpha=0.2)
    elif (
        graph.feature_type == "nominal"
        or graph.feature_type == "boolean"
        or graph.feature_type == "categorical"
    ):
        # plot bins for the categorical features
        fig = plt.figure()
        plt.bar(x_vals, scores, yerr=stds)
    else:
        raise Exception(f"Unknown graph feature type {graph.feature_type}.")
    plt.xlabel(graph.feature_name)
    plt.title(f"{graph.feature_name} ({graph.feature_type})")
