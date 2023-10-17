<div align="center">
    <h1><a href="">Pluto</a></h1>
    Visualization library built on top of Seaborn and Matplotlib.
    <br>
    <i>Easier plotting</i>
    <br>
</div>
<br>
<hr>

#### How to run
```
$ pip install pluto
```

```
# create custom bar_plot
bar_plot = Barplot()
# configuring custom bar_plot
bar_plot.shape(dim=(10, 5))
    .create('x_col', 'y_col', table, hue='z_col', c=None)
    .grid()
    .spine()
    .tick(left=True, labelleft=True, bottom=True, labelbottom=True)
    .label('x axis', 'y axis', 'title')
    .render()

```
#### Illustrations
- *TBI*

