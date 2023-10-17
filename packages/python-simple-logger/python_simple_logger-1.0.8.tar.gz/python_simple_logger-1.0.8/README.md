# Simple Python logger

A simple logger for console/file logging with duplicate logs filter support

## Release new version

### requirements

* Export GitHub token

```bash
export GITHUB_TOKEN=<your_github_token>
```

* [release-it](https://github.com/release-it/release-it)

Run the following once (execute outside repository dir for example `~/`):

```bash
sudo npm install --global release-it
npm install --save-dev @release-it/bumper
```

### usage

* Create a release

```bash
git pull
release-it # Follow the instructions
```

## Usage

```python
from simple_logger.logger import get_logger
logger = get_logger(name=__name__, level=logging.DEBUG, filename="my-log.log")
logger.info("This is INFO log")
```
