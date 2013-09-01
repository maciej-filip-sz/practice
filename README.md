Build and test setup for [my practice projects website](http://maciej-filip-sz.github.io/practice). Based on angular-seed.
    
    
The dependencies are a bit ridiculous:

* bash
* chrome
* chromedriver
* nodejs
    * jasmine
    * karma
* python2
    * splinter
    * selenium
    * pytest
* python3
    * jinja2
* ruby
    * watchr
    
    
Watchr will monitor `projects` for new and changed `.yaml` files, as well as changes to `templates/project.template`, automatically rendering them to HTML and placing in `app` with the same basename as the project. The rendered HTML files will have the same basename, and be placed in `app`.

* run `scripts/watchr.rb` to start watchr
    
    
Karma monitors changes to `.js` files in `app/js`, as well as unit tests in `test/unit`.

* run `scripts/test.sh` to start it
       
       
For end-to-end tests, you need an HTTP server on localhost port 8000:

* run `python -m SimpleHTTPServer` in the `practice` root
* `py.test test/e2e/` will run all available e2e tests in chrome
