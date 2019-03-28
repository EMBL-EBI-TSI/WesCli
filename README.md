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

5. `status --watch` requires [`watch`](https://en.wikipedia.org/wiki/Watch_(Unix)) to be installed.  
   You might already have it. Just check with:
    ```
    which watch
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

### Run spec file

The argument to `wes run` must be a yaml file with a specific format. You can find some examples [here](examples/).

You can:

* Run a workflow on a single site:

    ```yaml
    workflow: 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'

    input:
      input:
        class: File
        location: file:///data/tmp/README.md

    sites:
        - url: https://tes.tsi.ebi.ac.uk/ga4gh/wes/v1
    ```

* Run a workflow on multiple sites, with the same input:

    Just add more items to `sites`:

    ```yaml
    workflow: 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'

    input:
      input:
        class: File
        location: file:///data/tmp/README.md

    sites:
        - url: https://tes1.tsi.ebi.ac.uk/ga4gh/wes/v1
        - url: https://tes2.tsi.ebi.ac.uk/ga4gh/wes/v1
        - url: https://tes3.tsi.ebi.ac.uk/ga4gh/wes/v1
    ```

* Run a workflow on multiple sites, with the different inputs:

    ```yaml
    workflow: 'https://github.com/fgypas/cwl-example-workflows/blob/master/hashsplitter-workflow.cwl'

    input:
      input:
        class: File
        location: $input

    sites:
        - url:          http://localhost:8080/ga4gh/wes/v1
          inputParams:  { input: 'file:///tmp/hashSplitterInput/test1.txt' }
        - url:          http://localhost:8080/ga4gh/wes/v1
          inputParams:  { input: 'file:///tmp/hashSplitterInput/test2.txt' }
    ```

    Notice that the value of `location` was replaced by `$input`.  
    `$input` is a _variable_ -- the value of which must be provided for each site in the `inputParams` attribute.
