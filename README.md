# BIOL68400 Programming project
## OpenPrescribing Trends
Scripts and tools for identifying trends in OpenPrescribing data for the BIOL68400 Programming module for the STP in Bioinformatics (Genomics).

### What is OpenPrescribing?
[OpenPrescribing](https://openprescribing.net/) is a website that provides a simple to use search interface for the prescribing data published by NHS England. An API is also available making it easy to automatically grab information from the site. 

### What this repository includes
In this repository, you will find two python scripts and 3 Jupyter notebooks. Below is information regarding these scripts.

#### api<span>.py
api<span>.py contains most of the functions that are called in the Jupyter notebooks, as well as in make_heatmap.py. All functions are commented and contain docstrings making them easily callable in your own scripts.

#### make_heatmap.py
make_heatmap.py is an interactive that script that allows you to generate heatmaps for a given year showing number of prescriptions on a colour scale. An example of a generated plot is shown below. Should be fairly self explanatory when ran however any issues please raise an issue on github. Further information regarding the use of this script can be found in docs/make_heatmap_instructions.md

![Image of heatmap example](https://github.com/clarek20/Programming-project/raw/master/2018_14L_5.1.png)

## Boxplot.ipynb

Boxplot.ipynb contains a script that will generate a boxplot for a given year showing trends across a clinical commisioning group (CCG). Outliers are plotted on the graph as open circles, in future these should be coloured to identify the offending practice.

![Image of boxplot example](https://github.com/clarek20/Programming-project/raw/master/boxplot.png)

## Min Max.ipynb

Contains a script that can draw a graph which plots the minimum practice, maximum practive and the mean values for items prescribed per patient. Also shows a region of mean ± standard deviation

![Image of minmax graph](https://github.com/clarek20/Programming-project/raw/master/min_max_mean.png)

## Scatterplot correlation.ipynb

Contains a script to plot a scatterplot with aims to find associations across months. For a specific practice. Future versions should have the option to group months by season, rather than chronological order. This would likely show more of a trend than the way it currently is.

![scatterplot graph](https://github.com/clarek20/Programming-project/raw/master/scatterplot_correlation.png)
