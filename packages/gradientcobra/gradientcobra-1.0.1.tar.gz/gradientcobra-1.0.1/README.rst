gradientcobra
=============

|Travis Status| |Coverage Status| |Python39|

Introduction
------------

``gradientcobra`` is the ``python`` package implementation of `S. Has (2023) <https://jdssv.org/index.php/jdssv/article/view/70>`__, which is a Kernel-based consensual aggregation method for regression problems. 
Is is a regular kernel-based version of `Cobra` method of `Biau et al. (2016) <https://www.sciencedirect.com/science/article/pii/S0047259X15000950>`__. 
It is theoretically shown that consistency inheritance property also holds for this kernel-based configuration, and the same convergence rate is achieved.
Moreoever, gradient descent algorithm is applied to efficiently estimate the bandwidth parameter of the method.

Installation
------------

In terminal, run: ``pip install gradientcobra`` to download and install from PyPI.

Citation
--------

If you find ``gradientcobra`` helpful, please consider citing the following papaers:

- S., Has (2023), `Gradient COBRA: A kernel-based consensual aggregation for regression <https://jdssv.org/index.php/jdssv/article/view/70>`__.

- Biau, Fischer, Guedj and Malley (2016), `COBRA: A combined regression strategy <https://doi.org/10.1016/j.jmva.2015.04.007>`__.


Documentation and Examples
--------------------------

Dependencies
------------

-  Python 3.9+
-  numpy, scipy, scikit-learn, matplotlib, pandas, seaborn

References
----------

-  HAS, S. (2023). A Gradient COBRA: A kernel-based consensual aggregation for regression. 
   Journal of Data Science, Statistics, and Visualisation, 3(2). 
   Retrieved from `<https://jdssv.org/index.php/jdssv/article/view/70>`__.
-  G. Biau, A. Fischer, B. Guedj and J. D. Malley (2016), COBRA: A
   combined regression strategy, Journal of Multivariate Analysis.
-  M. Mojirsheibani (1999), Combining Classifiers via Discretization,
   Journal of the American Statistical Association.

.. |Travis Status| image:: https://img.shields.io/travis/hassothea/gradientcobra.svg?branch=master
   :target: https://travis-ci.org/hassothea/gradientcobra

.. |Python39| image:: https://img.shields.io/badge/python-3.9-green.svg
   :target: https://pypi.python.org/pypi/gradientcobra

.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/hassothea/gradientcobra.svg
   :target: https://codecov.io/gh/hassothea/gradientcobra
