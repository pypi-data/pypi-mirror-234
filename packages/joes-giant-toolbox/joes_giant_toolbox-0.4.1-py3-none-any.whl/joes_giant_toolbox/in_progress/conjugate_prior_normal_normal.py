def conjugate_prior_normal_normal(
    prior_mean: float,
    prior_variance: float,
    known_data_variance: float,
    data_sample_size: int,
    observed_data_mean: float,
) -> dict:
    """
    Calculates the (gaussian) posterior distribution of the of the mean by combining a normal prior distribution with observed data

    Notes
    -----
    The observed data X=x_1,x_2,...,x_n are assumed to have been generated as a random draw from the distribution x_i|mu ~ Normal(mean=mu, variance=s2)
    The prior distribution is specified as Normal

    Parameters
    ----------
    prior_mean: float
        TODO
    prior_variance: float
        TODO
    known_data_variance: float
        TODO
    data_sample_size: int
        TODO
    observed_data_mean: float
        TODO

    Returns
    -------
    dict
        {
            "posterior_mean": (float),
            "posterior_variance": (float),
        }

    Example Usage
    -------------

    # shrinking each subgroup mean towards the global mean:

    """
    return {
        "posterior_mean": -99,
        "posterior_variance": -99,
    }
