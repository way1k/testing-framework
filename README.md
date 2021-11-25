# Test Framework

- Stack: `python`+`pytest`+`selenium`+`docker`+`selenoid-ui`+`allure-server`
- Ready-made solution for `ui/api` testing
- Implemented `selenium` wrapper, integration with `allure-server` and `selenoid/ggr`
- Various clients are implemented, such as `http-client`, `orm`, `imap`, `ssh`, `greylog`
- Tests are run in parallel, each in its own container
- Remote launch tests by `gitlab-ci`