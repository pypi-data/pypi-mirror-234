# Tyba API Client

## Examples
For examples see [https://github.com/Tyba-Energy/tyba-client-notebooks](https://github.com/Tyba-Energy/tyba-client-notebooks).
The script examples in tyba-python-client/examples will be deprecated eventually.

## Development
### Docs
We use [`sphinx`](https://github.com/sphinx-doc/sphinx) and
[`autodoc-pydantic`](https://github.com/mansenfranzen/autodoc_pydantic) to manage the documentation for the client.
Source .rst files can be found in docs/source.

To generate/update documentation for the Tyba client, first make sure
your poetry environment includes the latest versions of all the dependency packages included in the docs. For example,
if `generation-models` was recently updated and pushed to pypi, you should run `poetry update` (or if you are concerned
about changing other packages, just `poetry add generation-models==x.x.x` where `x.x.x` is the latest version).
Then, `cd` into the docs directory and run the makefile that generates the HTML documentation
```bash
# Assuming you are already in the tyba-python-client directory
$ cd docs
$ poetry run make html
```
The HTML documentation can be found in docs/build/html.

This HTML documentation now needs to be uploaded to s3, so it
can be served at [https://docs.tybaenergy.com/api/](https://docs.tybaenergy.com/api/). We have a python script to do this
```bash
poetry run python docs/upload_to_s3.py
```



