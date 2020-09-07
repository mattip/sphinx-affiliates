# sphinx-affiliates

[![CI status](https://github.com/mattip/sphinx-affiliates/workflows/Tests/badge.svg)](https://github.com/mattip/sphinx-affiliates/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


Allow search to include documents from more than one [Sphinx
documentation](http://www.sphinx-doc.org) html site. 

This is useful when
you have a number of github repositories under one org, are using sphinx
to build documentation for all of them, and [github
pages](https://pages.github.com/) to serve the artifacts. When you configure
a [custom domain](https://docs.github.com/en/github/working-with-github-pages/about-custom-domains-and-github-pages),
say `https://my.site.org`, for one repo in the org, any other repo's github pages
(say repo2) will be visible as `https://my.site.org/repo2`. But the
`search.html` from the sites will not know about eachother: they will be
completely independent. This extension will solve that by
- changing the search engine to allow loading more than one index
- changing the search index generation process to generate an additional index
- add configuration options to add the additional indices, from affiliate
  sites, to the `search.html` page.


To use this, install it via `pip` and add something like this to your `conf.py`
```
extensions = [
    'sphinx_affiliates',   # Add the extension
]

# Where this site's build is hosted, this will be the URL for all the search
# results from this site.
affiliate_options = {
    'canonical_url': "https://affiliate_search.github.io",  
}

# Other sites to add to the search of this site
sphinx_affiliates = [
    'https://abc.com/affiliate_searchindex.js',  
    'https://def.com/affiliate_searchindex.js',
]
```
