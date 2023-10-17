This repository contains Python library with useful helper functions for Machine vision and Image processing (BI-SVZ) coursework taught at [FIT CTU](https://fit.cvut.cz/en). For more details, see [main course page](https://github.com/ImprolabFIT/BI-SVZ-coursework).

### How to deploy a new version
This repository uses GitLab CI/CD Pipelines to deploy improutils package either to production or test PyPI.

#### Steps to release a new version to production PyPI
 - Update version.py file with a new version number with respect to [semantic versioning rules](https://semver.org/)
 - Commit your local changes
	 - ```git commit -m "Add awesome AI feature" ```
 - Create a tagged version based on version.py
	 - ```git tag -a $(python3 setup.py --version)```
 - Push tag to origin
	 - ```git push --tags```
 - Wait for the package to be deployed and then check new version at [PyPI](https://pypi.org/project/improutils/)

#### Steps to release a new version to test PyPI
Almost same as above, but the **push tag step** must be skipped. Testing version is available at [test PyPI](https://test.pypi.org/project/improutils/).


#### Installing on Windows in developer mode
This is discussed more in detail in [installDevWin.md](./doc/installDevWin.md).

#### Running the tests
You must run the tests from the `improutils_package` directory.
An example command for running the test may be as follows:
```
python tests\test_preprocessing.py
```

> Note: running the test from the `tests` directory itself will result in errors
