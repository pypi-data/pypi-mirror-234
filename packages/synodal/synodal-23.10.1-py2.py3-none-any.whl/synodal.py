# Copyright 2019-2023 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import collections

REPOS_DICT = {}
REPOS_LIST = KNOWN_REPOS = []
PUBLIC_SITES = []

field_names = "nickname package_name git_repo settings_module front_end extra_deps public_url"
Repository = collections.namedtuple('Repository', field_names,
    defaults=['', '', '', [], ''])
# print(help(Repository))

def add(*args, **kwargs):
    r = Repository(*args, **kwargs)

    KNOWN_REPOS.append(r)
    REPOS_DICT[r.nickname] = r
    if r.front_end:
        # add an alias because front ends are looked up using their full package name
        REPOS_DICT[r.front_end] = r

# tools to be installed with --clone because they are required for a complete contributor environment:
add("synodal", "synodal", "https://gitlab.com/lino-framework/synodal.git")

add("atelier", "atelier", "https://gitlab.com/lino-framework/atelier.git", public_url='https://atelier.lino-framework.org')
add("rstgen", "rstgen", "https://gitlab.com/lino-framework/rstgen.git")
add("etgen", "etgen", "https://github.com/lino-framework/etgen")
add("eid", "eidreader", "https://github.com/lino-framework/eidreader")

add("cd", "commondata", "https://github.com/lsaffre/commondata")
add("be", "commondata.be", "https://github.com/lsaffre/commondata-be")
add("ee", "commondata.ee", "https://github.com/lsaffre/commondata-ee")
add("eg", "commondata.eg", "https://github.com/lsaffre/commondata-eg")

add("getlino", "getlino", "https://gitlab.com/lino-framework/getlino.git",
    public_url='https://getlino.lino-framework.org')
add("lino", "lino", "https://gitlab.com/lino-framework/lino.git", "", "lino.modlib.extjs")
add("xl", "lino-xl", "https://gitlab.com/lino-framework/xl.git")
add("welfare", "lino-welfare", "https://gitlab.com/lino-framework/welfare.git",
    public_url='https://welfare.lino-framework.org')

add("react", "lino-react", "https://gitlab.com/lino-framework/react.git", "", "lino_react.react")
add("openui5", "lino-openui5", "https://gitlab.com/lino-framework/openui5.git", "", "lino_openui5.openui5")

add("book", "lino-book", "https://gitlab.com/lino-framework/book.git", public_url='https://dev.lino-framework.org/')
add("cg", "", "https://gitlab.com/lino-framework/cg.git", public_url='https://community.lino-framework.org/')
add("ug", "", "https://gitlab.com/lino-framework/ug.git", public_url='https://using.lino-framework.org/')
add("hg", "", "https://gitlab.com/lino-framework/hg.git", public_url='https://hosting.lino-framework.org/')
add("lf", "", "https://gitlab.com/lino-framework/lf.git", public_url='https://www.lino-framework.org/')
add("ss", "", "https://gitlab.com/synodalsoft/www.git", public_url='https://www.synodalsoft.net/')

add("algus", "", "https://gitlab.com/lino-framework/algus.git")

# experimental: applications that have no repo on their own
add("min1", "", "", "lino_book.projects.min1.settings")
add("min2", "", "", "lino_book.projects.min2.settings")
add("polls", "", "", "lino_book.projects.polls.mysite.settings")
add("cosi_ee", "", "", "lino_book.projects.cosi_ee.settings.demo")
add("lydia", "", "", "lino_book.projects.lydia.settings.demo")
add("noi1e", "", "", "lino_book.projects.noi1e.settings.demo")
add("chatter", "", "", "lino_book.projects.chatter.settings")
add("polly", "", "", "lino_book.projects.polly.settings")

# e.g. for installing a non-Lino site like mailman
add("std", "", "", "lino.projects.std.settings")


def add2(*args, **kwargs):
    kwargs.update(extra_deps="lino xl".split())
    add(*args, **kwargs)

add2("amici", "lino-amici", "https://gitlab.com/lino-framework/amici", "lino_amici.lib.amici.settings")
add2("avanti", "lino-avanti", "https://gitlab.com/lino-framework/avanti", "lino_avanti.lib.avanti.settings")
add2("cms", "lino-cms", "https://gitlab.com/lino-framework/cms", "lino_cms.lib.cms.settings")
add2("care", "lino-care", "https://gitlab.com/lino-framework/care", "lino_care.lib.care.settings")
add2("cosi", "lino-cosi", "https://gitlab.com/lino-framework/cosi", "lino_cosi.lib.cosi.settings")
add2("mentori", "lino-mentori", "https://gitlab.com/lino-framework/mentori", "lino_mentori.lib.mentori.settings")
add2("noi", "lino-noi", "https://gitlab.com/lino-framework/noi", "lino_noi.lib.noi.settings")
add2("presto", "lino-presto", "https://gitlab.com/lino-framework/presto", "lino_presto.lib.presto.settings")
add2("pronto", "lino-pronto", "https://gitlab.com/lino-framework/pronto", "lino_pronto.lib.pronto.settings")
add2("tera", "lino-tera", "https://gitlab.com/lino-framework/tera", "lino_tera.lib.tera.settings")
add2("shop", "lino-shop", "https://gitlab.com/lino-framework/shop", "lino_shop.lib.shop.settings")
add2("vilma", "lino-vilma", "https://gitlab.com/lino-framework/vilma", "lino_vilma.lib.vilma.settings")
add2("voga", "lino-voga", "https://gitlab.com/lino-framework/voga", "lino_voga.lib.voga.settings")
# add2("ciao", "lino-ciao", "https://github.com/lino-framework/ciao", "lino_ciao.lib.ciao.settings")

def add2(*args, **kwargs):
    kwargs.update(extra_deps="lino xl welfare".split())
    add(*args, **kwargs)

add2("weleup", "lino-weleup", "https://gitlab.com/lino-framework/weleup", "lino_weleup.settings")
add2("welcht", "lino-welcht", "https://gitlab.com/lino-framework/welcht", "lino_welcht.settings")


APPNAMES = [a.nickname for a in KNOWN_REPOS if a.settings_module]
FRONT_ENDS = [a for a in KNOWN_REPOS if a.front_end]

field_names = "url settings_module default_ui"
PublicSite = collections.namedtuple('PublicSite', field_names)

def add(*args, **kwargs):
    ps = PublicSite(*args, **kwargs)
    PUBLIC_SITES.append(ps)

add("https://voga1r.lino-framework.org", "lino_voga.lib.voga.settings", 'lino.modlib.extjs')
add("https://voga1e.lino-framework.org", "lino_voga.lib.voga.settings", 'lino_react.react')
add("https://cosi1e.lino-framework.org", "lino_cosi.lib.cosi.settings", 'lino.modlib.extjs')
add("https://noi1r.lino-framework.org", "lino_noi.lib.noi.settings", 'lino_react.react')
add("https://weleup1.mylino.net", "lino_weleup.settings", 'lino.modlib.extjs')
add("https://welcht1.mylino.net", "lino_welcht.settings", 'lino.modlib.extjs')

SPHINX_EXTLINKS = {
    'ticket' : ('https://jane.mylino.net/#/api/tickets/PublicTickets/%s', '#%s')
}
