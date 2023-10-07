# visplotlib

[![flake8 Actions Status](https://github.com/VisiumCH/visplotlib/actions/workflows/lint.yml/badge.svg)](https://github.com/VisiumCH/visplotlib/actions) [![PyPI version](https://badge.fury.io/py/visplotlib.svg)](https://badge.fury.io/py/visplotlib)

Standardized plot styling for Visium SA.

## Installation

To plot with **visplotlib**, you need to install the library into your environment:

```bash
pip install visplotlib
```

You can then use the following import statements:

```python
import visplotlib as vpl
from visplotlib.pyplot import mpl, plt  # <-- Wrapped Matplotlib and Pyplot
from visplotlib.seaborn import sns  # <-- Wrapped Seaborn
from visplotlib_test.plotly import go, px # <-- Wrapped Plotly
```

## Example

We want to make your plots beautiful. We don't want to change your coding practices with long and annoying procedures.

All you need to do is call `plt.format()`(for matplotlib and seaborn) when making a plot. That's it.

```python
fig, ax = plt.subplots()

iris = sns.load_dataset('iris')

sns.scatterplot(data=iris, x='sepal_length', y='petal_length', ax=ax)
ax.set_title('Sepal vs. Petal length')

plt.format()  # All we need to do is call plt.format()!
plt.show()
```

or `plotly.format()`(for plotly)

```python
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="A Plotly Express Figure")

plotly.format(fig)  # All we need to do is call plt.format()!
fig.show()
```

If you want to use the plotly template specifically created for the google slides you can use the `template_type` option (That takes the values `fullsize`, `halfsize`, or `default`):
```python
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="A Plotly Express Figure")

plotly.format(fig, template_type="fullsize")  # All we need to do is call plotly.format()!
fig.show()
```

## Loom demonstration



https://user-images.githubusercontent.com/32436482/124758979-6c65cd00-df2f-11eb-8b3e-fc156d441913.mp4

