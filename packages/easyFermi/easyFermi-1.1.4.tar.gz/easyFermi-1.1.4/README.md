# easyFermi
The easiest way to analyze Fermi-LAT data.

# Requirements
_easyFermi_ relies on Python 3, _Fermitools_ and _Fermipy_. 

We recommend the user to install Miniconda 3 or Anaconda 3 before proceeding.

To install _Fermitools_ and _Fermipy_ with conda, do:

<pre><code>$ conda create --name fermi -c conda-forge -c fermi python=3.9 "fermitools>=2.2.0" healpy gammapy
</code></pre>

Then activate the fermi environment:

<pre><code>$ conda activate fermi
</code></pre>

And simply install Fermipy and easyFermi with pip:

<pre><code>$ pip install fermipy ipython easyFermi
</code></pre>


# Usage

While in the fermi environment, do:

<pre><code>$ ipython
>>> import easyFermi
</code></pre>


# Tutorials

You can find more details about _easyFermi_ on https://github.com/ranieremenezes/easyFermi, and check the _easyFermi_ tutorials on YouTube:

https://www.youtube.com/channel/UCeLCfEoWasUKky6CPNN_opQ

# Fermipy V1.0.1 light curve problem

In the old version of _Fermipy_ (i.e. V1.0.1, Python 3), the users face a "KeyError: 'fit_success'" issue when trying to build the light curves. 

This issue is solved here:
https://github.com/fermiPy/fermipy/issues/368

