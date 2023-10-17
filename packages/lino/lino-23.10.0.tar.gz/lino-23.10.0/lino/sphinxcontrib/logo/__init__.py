# -*- coding: UTF-8 -*-
# Copyright 2013-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""Sets the `html_logo` and `html_favicon` for all Lino-related sites.

Using this extension currently means that you cannot set these config
settings yourself.

Also adds some css styling.

"""

from pathlib import Path


def builder_inited(app, config):
    """Define certain settings
    """
    # raise Exception("20230616")
    static_path = (Path(__file__).parent / 'static').absolute()
    config.html_static_path.append(str(static_path))

    # config.html_logo = str(static_path / 'logo_web3.png')
    # config.html_favicon = str(static_path / 'favicon.ico')

    tpl_path = (Path(__file__).parent / 'templates').absolute()
    assert (tpl_path / "footer.html").exists()
    # pth = Path("../docs/.templates").resolve()
    config.templates_path.insert(0, str(tpl_path))
    config.html_sidebars = { '**' : []}

    # for logo_file in ['synodalsoft-logo.svg']:
    #     tpl_path /
    #     src_dir = Path('../docs/dl').resolve()
    #     static_dir = Path('../docs/.static').resolve()
    #     static_logo_file = static_dir / logo_file
    #     if not static_logo_file.exists():
    #         static_logo_file.symlink_to(src_dir / logo_file)


def setup(app):
    # app.add_css_file('linodocs.css')
    # app.add_stylesheet('centeredlogo.css')
    # app.connect('builder-inited', builder_inited)
    app.connect('config-inited', builder_inited)
