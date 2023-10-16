import joes_giant_toolbox.stats


def test_expected_output_single_example():
    result = joes_giant_toolbox.stats.conjugate_prior_beta_binomial(
        prior_beta_a=1, prior_beta_b=1, n_successes=3, n_trials=3
    )
    assert (
        result["posterior_beta_a"] == 4 and result["posterior_beta_b"] == 1
    ), f"known example (prior_beta_a=1, prior_beta_b=1, n_successes=3, n_trials=3) produced incorrect output posterior_beta_a={result['posterior_beta_a']} posterior_beta_b={result['posterior_beta_b']}. Expected posterior_beta_a=4 posterior_beta_b=1"
