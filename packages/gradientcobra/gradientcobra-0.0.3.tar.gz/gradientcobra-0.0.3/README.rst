# gradientcobra

This is the `python` package implementation of `Gradient COBRA` method by [S. Has (2023)](https://jdssv.org/index.php/jdssv/article/view/70). 

## Summary

Gradient COBRA is a kernel-based consensual aggregation for regression problem that extends the naive kernel-based of Biau et al. (2016) to a more general regular kernel-based configuration. It is theoretically shown that Gradient COBRA inherits the consistency of the consistent basic estimator in the list, and the same rate of convergence is archived for exponentially tail-delaying kernel functions. On top of that, gradient descent algorithm is proposed to efficiently estimate the bandwidth parameter of the aggregation method. It is shown to be up to hundred times faster than the classical method and `python` package [pycobra](https://arxiv.org/abs/1707.00558).