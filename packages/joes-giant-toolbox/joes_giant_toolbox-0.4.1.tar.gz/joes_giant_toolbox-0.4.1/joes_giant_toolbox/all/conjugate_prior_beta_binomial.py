def conjugate_prior_beta_binomial(
    prior_beta_a: float,
    prior_beta_b: float,
    n_successes: int,
    n_trials: int,
) -> dict:
    """
    Calculates the posterior distribution of the success probability parameter [p] of a binomial distribution, from observed data and a user-specified beta prior

    Parameters
    ----------
    prior_beta_a: float
        The first shape parameter (alpha) of the prior (beta) distribution
    prior_beta_b: float
        The second shape parameter (beta) of the prior (beta) distribution
    n_successes: int
        Number of observed trials on which a success (X=1) was observed
    n_trials: int
        Number of observed trials

    Returns
    -------
    dict
        {
            "posterior_beta_a": (float),
            "posterior_beta_b": (float),
        }
    """
    return {
        "posterior_beta_a": prior_beta_a + n_successes,
        "posterior_beta_b": prior_beta_b + n_trials - n_successes,
    }
