import os
import pytest


@pytest.mark.sphinx('html', testroot='basic/')
def test_build_html(app, status, warning):
    app.builder.build_all()
    build = os.path.join(app.env.srcdir, '_build', 'html')
    with open(os.path.join(build, 'search.html')) as fid:
        lines = []
        for line in fid:
            if 'affiliate_searchindex' in line:
                lines.append(line)
        assert len(lines) == 2

    files = os.listdir(build)
    assert 'affiliate_searchindex.js' in files
