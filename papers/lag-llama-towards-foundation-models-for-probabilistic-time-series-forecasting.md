# Lag-Llama: Towards Foundation Models for Probabilistic Time Series Forecasting

**Year:** 2024

**Paper:** [arXiv](https://arxiv.org/pdf/2310.08278)

## 🧠 Summary
Foundation model for univariate probabilistic time series forecasting using a decoder-only transformer-based architecture.

**Preprocessing:** robust scaling of windows.

**Input:** lagged features + date time features (frequencies) + summary statistics (mean and variance) as covariates.

**Output:** distribution parameters of the next time step(s).

**Architecture:** tokens -> projection -> masked [ensures that each token can only attend to the previous tokens in the sequence, preventing information leakage from the future] decoder layers -> distribution head.

**Training:** minimizing the negative log-likelihood of the predicted distribution of all predicted timesteps.

## 🏷️ Topics
`FM`, `Covariates`
