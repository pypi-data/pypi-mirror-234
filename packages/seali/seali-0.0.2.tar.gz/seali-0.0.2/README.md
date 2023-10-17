# SeaLI 0.0.2

![](docs/logo.png)

Python Command Line Interface (CLI) and API to interact with a GDataSea instance.

**Usage**:

```console
$ sea [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Show version of the CLI
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `project`

## `sea project`

**Usage**:

```console
$ sea project [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `create`: Create a new project on GDataSea
* `delete`: Delete a new project on GDataSea

### `sea project create`

Create a new project on GDataSea

**Usage**:

```console
$ sea project create [OPTIONS] FILE
```

**Arguments**:

* `FILE`: EDA file to upload  [required]

**Options**:

* `--lyp-file TEXT`: Layer properties file for project (.lyp)
* `--name TEXT`: Project name
* `--description TEXT`
* `--base-url TEXT`: Base URL for GDataSea, e.g. https://gdatasea.example.com  [env var: GDATASEA_URL; default: http://localhost:3131]
* `--top-cell TEXT`: Define one or more top cells to extract. Each top cell gets an associated list of wildcards (see --wildcards) for device extraction. If the number of wildcards lists is shorter than the list of top cells, the associated wildcards will be [], meaning no devices except the top cell device will be created
* `--wildcards TEXT`: Lists of (partial) cell names to extract as devices below the top cell. This is a string list separated by spaces or commas.
* `--open`: Open project `cell_view` if successful
* `--help`: Show this message and exit.

### `sea project delete`

Delete a new project on GDataSea

**Usage**:

```console
$ sea project delete [OPTIONS] PROJECT_NAME
```

**Arguments**:

* `PROJECT_NAME`: [required]

**Options**:

* `--base-url TEXT`: Base URL for GDataSea, e.g. https://gdatasea.example.com  [env var: GDATASEA_URL; default: http://localhost:3131]
* `--help`: Show this message and exit.
