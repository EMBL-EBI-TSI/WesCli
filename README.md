# Multi-WES CLI client

## Instalation

1. Install [pipenv](http://pipenv.org/)
    ```
    pip install --user pipenv
    ```

2. Clone this repo.

3. Run
    ```
    ./init
    ```

4. Create a symlink to the executable somewhere in your `$PATH`:
    ```
    ln -svf "$(pipenv --venv)/bin/wes" "somewhere/in/PATH"
    ```
    (or: edit `./install` and run it)

## Usage and examples

Here's what you can do so far:

* Run a workflow on a single site:
```
wes run examples/singleSite.yaml
```

* Run a workflow on a multiple sites:
```
wes run examples/sites.yaml
```

* Get status of all currently running workflows:
```
wes status
```
