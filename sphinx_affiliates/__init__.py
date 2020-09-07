import os
import shutil
import types
import sphinx

__version__ = "0.0.1"

# For type annotations
if False:
    from sphinx.application import Sphinx

def add_affiliates(app: "Sphinx") -> None:
    builder = app.builder
    if 'canonical_url' in app.config.html_theme_options:
        rootUrl = app.config.html_theme_options['canonical_url']
    elif (hasattr(app.config, 'affiliate_options') and
          'canonical_url' in app.config.affiliate_options):
        rootUrl = app.config.affiliate_options['canonical_url']
    else:
        raise ValueError('sphinx_affiliates extension" missing config value '
                         '"canonical_url" in "afffiliate_options" dict')
    if not hasattr(builder, 'searchindex_filename'):
        return
    affiliate_filename = 'affiliate_' + builder.searchindex_filename
    old = builder.dump_search_index
    def dump_search_index(self: "Sphinx") -> None:
        old()
        searchindexfn = os.path.join(self.outdir, self.searchindex_filename)
        affiliatefn = os.path.join(self.outdir, affiliate_filename)
        with open(searchindexfn) as fid_in:
            txt = fid_in.read()
            if txt.startswith('Search.setIndex({'):
                prefix = 'Search.setAffiliate({rootUrl="%s",' % rootUrl
                if self.indexer_dumps_unicode:
                    with open(affiliatefn, 'w', encoding='utf-8') as fid_out:
                        fid_out.write(prefix + txt[17:])
                else:
                    with open(affiliatefn, 'wb') as fid_out:
                        fid_out.write(prefix + txt[17:])
        # The search.html file has already been written, add other affiliate
        # indices to it
        affiliates = self.config.sphinx_affiliates
        if affiliates:
            search = self.get_outfilename('search')
            encoding = self.config.html_output_encoding
            lines = []
            with open(search) as fid:
                for line in fid:
                    lines.append(line)
                    if self.searchindex_filename in line:
                        for affiliate in affiliates:
                            txt = line.replace(self.searchindex_filename,
                                               affiliate)
                            lines.append(f'{txt}s\n')
            with open(search, 'w', encoding=encoding,
                      errors='xmlcharrefreplace') as f:
                for line in lines:
                    f.write(line)
        # Copy our version of searchtools.js
        my_searchtools = os.path.join(os.path.dirname(__file__), 'searchtools.js')
        your_searchtools = os.path.join(self.outdir, '_static', 'searchtools.js')
        if not os.path.exists(your_searchtools):
            raise ValueError(f'could not find "{your_searchtools}"')
        shutil.copyfile(my_searchtools, your_searchtools)

    builder.dump_search_index = types.MethodType(dump_search_index, builder)

def setup(app: "Sphinx") -> None:
    app.add_config_value('sphinx_affiliates', [], '')
    app.add_config_value('affiliate_options', {}, '')
    app.connect("builder-inited", add_affiliates)

