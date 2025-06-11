# N-BEATS: Neural Basis Expansion Analysis for Interpretable Time Series Forecasting

**Year:** 2020

**Paper:** [arXiv](https://arxiv.org/pdf/1905.10437)

## 🧠 Summary
Basis expansion is used to augment a set of features in order to model non-linear relationships, e.g. polynomial or Fourier basis. Here, the model is trained to find the best basis expansion method.

**Input:** univariate time series.

**Architecture:** A *block* consists of 4 fully-connected layers. It finds *theta* (expansion coefficients), performs *g* (basis expansion), and produces *forecast* (future) and *backcast* (history). Each *block* gets the residuals coming from the previous one, i.e. only the information that was not captured previously. A *stack* combines together different *blocks*, and outputs a partial prediction. The combination of all *stacks* results in the final forecast.

The basis expansion is either learnable (*generic*) or constrained (*interpretable*), e.g. expressing the trend or seasonality component.

![Figure](../figures/n-beats-neural-basis-expansion-analysis-for-interpretable-time-series-forecasting.png)

## 🏷️ Topics

