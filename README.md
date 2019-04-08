# Multi-WES CLI client

[![Build Status](https://travis-ci.com/EMBL-EBI-TSI/WesCli.svg?token=u11Aix2T7c5M2Hxs5pyA&branch=master)](https://travis-ci.com/EMBL-EBI-TSI/WesCli)


## Installation

1. Requirements

    * Python 3.6+
    * virtualenv
    * [pipenv](http://pipenv.org/)
        * Ubuntu:
        ```
        pip install --user pipenv
        ```

        * MacOS:
        ```
		brew install pipenv
        ```

    * [`watch`](https://en.wikipedia.org/wiki/Watch_(Unix))

        * Ubuntu:

        You probably already have it. You can check with:
        ```
        which watch
        ```

        * MacOS:
        ```
        brew install watch
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

    Notice that the value of `location` changed to `$input`.  
    `$input` is a _variable_ -- the value of which must be provided for each site in the `inputParams` attribute.
