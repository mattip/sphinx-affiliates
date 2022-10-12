from __future__ import print_function
import codecs
import os
import shutil
import types
import sphinx

__version__ = "0.3.0"


def pre_2_replace(search, affiliates, line, lines):
    # pre-v2.0 sphinx has
    # jQuery(function() { Search.loadIndex("{{ pathto('<search>', 1) }}"); });
    # replace that with the more modern version
    # however, we are inside a '<script>' block, so make it two empty ones
    lines.append('  </script>\n')
    path = line.split(search)[0].split('loadIndex("')[1]
    fmt = '    <script src="%s%s" defer></script>\n'
    lines.append(fmt % (path, search))
    for affiliate in affiliates:
        lines.append(fmt % (path, affiliate))
    lines.append('  <script type="text/javascript">\n')


def add_affiliates(app):
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
    def dump_search_index(self):
        old()
        searchindexfn = os.path.join(self.outdir, self.searchindex_filename)
        affiliatefn = os.path.join(self.outdir, affiliate_filename)
        with open(searchindexfn) as fid_in:
            txt = fid_in.read()
            if txt.startswith('Search.setIndex({'):
                prefix = 'Search.setAffiliate({rootUrl="%s",' % rootUrl
            if self.indexer_dumps_unicode:
                with codecs.open(affiliatefn, 'w', encoding='utf-8') as fid_out:
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
                    if self.searchindex_filename in line:
                        if 'jQuery' in line:
                            # pre-v2.0 sphinx, special handling
                            pre_2_replace(self.searchindex_filename, affiliates,
                                          line, lines)
                        else:
                            lines.append(line)
                            for affiliate in affiliates:
                                txt = line.replace(self.searchindex_filename,
                                                   affiliate)
                                lines.append('{}s\n'.format(txt))
                    else:
                        lines.append(line)
            with codecs.open(search, 'w', encoding=encoding,
                             errors='xmlcharrefreplace') as f:
                for line in lines:
                    try:
                        f.write(line)
                    except UnicodeDecodeError as e:
                        print('error in line', str(e))
                        print(line)

        # Copy our version of searchtools.js
        my_searchtools = os.path.join(os.path.dirname(__file__), 'searchtools.js')
        your_searchtools = os.path.join(self.outdir, '_static', 'searchtools.js')
        if not os.path.exists(your_searchtools):
            raise ValueError('could not find "{}"'.format(your_searchtools))
        shutil.copyfile(my_searchtools, your_searchtools)

    builder.dump_search_index = types.MethodType(dump_search_index, builder)

def setup(app):
    app.add_config_value('sphinx_affiliates', [], '')
    app.add_config_value('affiliate_options', {}, '')
    app.connect("builder-inited", add_affiliates)

