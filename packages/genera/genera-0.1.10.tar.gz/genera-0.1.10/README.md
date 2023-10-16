# Genera

## Design principles:
- Structured: clearly separated `UI`, `Algo`, `Plot`, `Data`, `Device` classes in separate files and folders. The objects only come together in the `App` class.
- Readable: The `_ui.py`, `_algo.py`, `_plot.py`, `_data.py`, `_device.py` files are easy to read and understand because they don't access each other. The main `_app.py` file in the root folder of the app is the only place that imports the various components.
- Testable: Without overlapping functionality, each component can reach 100% test coverage.
- Softcoded: Everything that is a parameter is stored in `app.json`, `ui.json`, `algo.json`, `plot.json`, `data.json`, `device.json`.
- Modular: `import genera` gives you access to developer tools, but it also provides access to existing apps. This way we can easily leverage features of existing apps via `genera.apps` in new apps.

## App folder structure:
~~~
    root folder
    ├── primer_generator_app.py # contains the main class called PrimerGeneratorApp
    ├── app.json
    ├── README.md
    ├── __init__.py # Has a single line: "from .primer_generator_app import PrimerGeneratorApp". This allows us to skip "primer_generator_app" when we instantiate the app with genera.apps.PrimerGeneratorApp()
    ├── ui
        ├── primer_generator_app.py # this file specifies the UI
        ├── ui.json # we don't hardcode in .py files, so this contains a lot of strings that are displayed in the UI
        └── __init__.py # Has a single line: "from .primer_generator_ui import PrimerGeneratorUI". This allows us to skip "primer_generator_ui" when we import the UI class via ".ui.PrimerGeneratorUI"
    ├── algo
        ├── primer_generator_algo.py # this function should contain the calculation functions that this app needs
        ├── algo.json
        └── __init__.py
    ├── plot
        ├── primer_generator_plot.py # stores the data for plotting and does the plot and updates to the plot
        ├── plot.json
        └── __init__.py
    ├── data
        ├── primer_generator_data.py # provides data I/O functions. In other examples, this would provide database access
        ├── data.json
        └── __init__.py
    ├── device
        ├── primer_generator_device.py # In the future, this will provide a convenient interface to hardware functions. It only enables hardware access to what this app really needs
        ├── device.json
        ├── xxx.h # this app doesn't need device driver APIs
        ├── xxx.dll # this app doesn't need device driver APIs
        └── __init__.py
    └── test
        └── # put test files here that execute automatically for CI/CD
~~~

## Developer features
- You can find commonly used functionality for creating a new app under `genera.utils`, e.g. `genera.utils.settings.load()`.
- You can inherit from pre-defined `UI`, `Algo`, `Plot`, `Data`, `Device` classes via `genera.classes.UI`, etc.
- In the future, we can add a common UI framework that will be accessible under `genera.ui`.