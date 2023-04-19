# shinyswatch

[Bootswatch](https://bootswatch.com/) + Bootstrap 5 themes for [Shiny](https://shiny.rstudio.com/py/).


Here are just three of the 25 themes in shinyswatch:

| ![Minty](readme_minty.png) | ![Sketchy](readme_sketchy.png) | ![Superhero](readme_superhero.png) |
|----------------------------|--------------------------------|------------------------------------|
| Minty                      | Sketchy                        | Superhero                          |


## Installation

```sh
pip install shinyswatch
```

To install the latest development version from this repository:

```sh
pip install https://github.com/rstudio/py-shinyswatch/tarball/main
```

## Usage

To use a theme, call the theme function and add it to your App's UI definition.

```python
# Darkly theme
shinyswatch.theme.darkly()

# Sketchy theme
shinyswatch.theme.sketchy()
```

Example Shiny application:

```python
# File: app.py
from shiny import App, Inputs, Outputs, Session, render, ui

import shinyswatch

app_ui = ui.page_fluid(
    # Theme code - start
    shinyswatch.theme.darkly(),
    # Theme code - end
    ui.input_slider("num", "Number:", min=10, max=100, value=30),
    ui.output_text_verbatim("slider_val"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def slider_val():
        return f"{input.num()}"


app = App(app_ui, server)
```

![darkly theme](readme_darkly.png)

## Development

If you want to do development on shinyswatch for Python:

```sh
pip install -e ".[dev,test]"
```

### Examples

There are three examples in the shinyswatch repo.

<!-- You can view them online at: [shinyswatch.theme.darkly](http://rstudio.github.io/py-shinyswatch/reference/theme.darkly.html) and [get_theme](http://rstudio.github.io/py-shinyswatch/reference/get_theme.html). -->

To run the demos locally, you can run the examples by calling:

```sh
python3 -m shiny run examples/basic-darkly/app.py
# or
python3 -m shiny run examples/big-sketchy/app.py
# or
python3 -m shiny run examples/components/app.py
```
