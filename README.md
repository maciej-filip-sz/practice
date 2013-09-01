Build and test setup for my practice projects website. Based on angular-seed.

The dependencies are a bit ridiculous:
    bash
    chrome
    chromedriver
    nodejs
        jasmine
        karma
    python2
        splinter
        selenium
        pytest
    python3
        jinja2
    ruby
        watchr


To automatically build html, run:
    `scripts/watchr.rb`
This will watch projects for new and changed `.yaml` files, as well as changes to `templates/project.template`. The rendered HTML files will have the same basename, and be placed in `app`.

To automatically run unit tests, run:
    `scripts/test.sh`
Karma monitors changes to `.js` files in `app/js`, as well as unit tests in `test/unit`.

For end-to-end tests, you need an HTTP server on localhost port 8000:
    `python -m SimpleHTTPServer`
then you can run:
    `py.test test/e2e/`
