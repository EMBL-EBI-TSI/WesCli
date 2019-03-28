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

5. `status --watch` requires `watch` to be installed:
    ```
    sudo apt-get install watch
    ```

## Usage and examples

Here's what you can do so far:

* Run a workflow on a single site:
```
wes run examples/singleSite_real_cluster.yaml
```

* Run a workflow on a multiple sites:
```
wes run examples/sites.yaml
```

* Get status of all currently running workflows:
```
wes status
```

* Watch the status of all currently running workflows:
```
wes status --watch
```

### Workspace operations

* Browse the workspace:

    ```
    $ wes get https://tes.tsi.ebi.ac.uk/data/tmp/
    YO15EZ/                        (file://data/tmp/YO15EZ/)
    Z9BNOH/                        (file://data/tmp/Z9BNOH/)
    ZE4HDH/                        (file://data/tmp/ZE4HDH/)
    evil.json                      (file://data/tmp/evil.json)
    Hello.txt                      (file://data/tmp/Hello.txt)
    ```

* Get the contents of a file:
    ```
    $ wes get https://tes.tsi.ebi.ac.uk/data/tmp/Hello.txt
    Hello, world!
    ```
* Upload a file:
    ```
    wes upload https://tes.tsi.ebi.ac.uk/data/tmp/ README.md
    ```
