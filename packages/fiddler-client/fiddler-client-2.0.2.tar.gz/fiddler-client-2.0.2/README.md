# Fiddler Python client

## Pre Release

As we get ready for distribution of the updated python client we need to ensure that all the associated downstream artifacts are updated.

1. Inform on `#releases` slack channel of the impending python client release with release notes.
1. [`Fiddler Docs`](https://docs.fiddler.ai/docs) needs updating.
2. Quick start and other notebooks linked to in fiddler docs need updating.
3. Ensure that the customer success team is appraised of the impending changes and possible impact.
4. In case of breaking changes, eg: changes to request/response, the following is a must
   - All quick start notebooks in fiddler docs need updation.
   - The code snippets in [`Fiddler Docs`](https://docs.fiddler.ai/docs) needs updating
   - If it's a new feature appropriate care has to be taken to
   - Customer Success needs to sign off on the changes and they need to plan for customer update

## Distribution

The Fiddler Python client is published as
[`fiddler-client`](https://pypi.org/project/fiddler-client/) in the Python
Package Index.

1. Set the new semantic version number in `fiddler/_version.py`, e.g. `1.4.3`;
2. Update `PUBLIC.md` with release notes for the new version;
3. Raise a PR;
4. Once the PR is merged, create a new annotated tag on the `main` branch. For
   example:

   ```bash
   git checkout main
   git pull
   git tag -a 1.4.3 -m 'The one that fixes event publishing'
   git push --tag
   ```

This triggers a pipeline that will automatically build and publish the new
version of the client to PyPI.

Note: dev versions may be published from any branch at any time by using a
`.devN` affix, as described in [PEP-440](https://peps.python.org/pep-0440/). For
example: `1.4.3.dev5`.

## Post Release

1. Inform on `#releases` slack channel of the python client release with release notes.
1. Verify:
   1. [`Fiddler Docs`](https://docs.fiddler.ai/docs) docs reflect the changes
   1. All the quick start guides are working (installing the python client from PyPI)


