# BIOL68400 Programming project
## OpenPrescribing Trends
Scripts and tools for identifying trends in OpenPrescribing data for the BIOL68400 Programming module for the STP in Bioinformatics (Genomics).

### What is OpenPrescribing?
[OpenPrescribing](https://openprescribing.net/) is a website that provides a simple to use search interface for the prescribing data published by NHS England. An API is also available making it easy to automatically grab information from the site. 

### What this repository includes
In this repository, you will find two python scripts and 4 Jupyter notebooks. Below is information regarding these scripts.

#### api<span>.py
api<span>.py contains most of the functions that are called in the Jupyter notebooks, as well as in make_heatmap.py. All functions are commented and contain docstrings making them easily callable in your own scripts.

#### make_heatmap.py
make_heatmap.py is an interactive that script that allows you to generate heatmaps for a given year showing number of prescriptions on a colour scale. An example is shown below.

![Image of heatmap example](https://github.com/clarek20/Programming-project/raw/master/2018_14L_5.1.png)

## Boxplot.ipynb

Boxplot.ipynb contains a script that will generate a boxplot for a given year showing trends across a clinical commisioning group (CCG).

![Image of boxplot example](https://github.com/clarek20/Programming-project/raw/master/boxplot.png)