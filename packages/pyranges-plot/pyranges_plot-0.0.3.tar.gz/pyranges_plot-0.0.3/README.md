# pyranges_plot
Gene visualization package for dataframe objects generated with PyRanges.


## Overview
The goal is getting a plot displaying a series of genes contained in a dataframe from
a PyRanges object. It displays the genes in its corresponding chromosome subplot. The 
user can choose whether the plot is based on Matplotlib or Plotly by setting the engine. 

Pyranges plot offers a wide versatility for coloring. The data feature (column) according
to which the genes will be colored is by default the gene ID, but this “color column” can 
be selected manually. Color specifications can be left as the default colormap or be 
provided as dictionaries, lists and color objects from either Matplotlib or Plotly 
regardless of the chosen engine. When a colormap or list of colors is specified, the 
color of the genes will iterate over the given colors following the color column pattern. 
In the case of concrete color instructions such as dictionary, the genes will be colored 
according to it while the non-specified ones will be colored in black(??).


## Installation
PyRanges-Plot can be installed using pip:

```
pip install pyranges-plot
```


## Examples

