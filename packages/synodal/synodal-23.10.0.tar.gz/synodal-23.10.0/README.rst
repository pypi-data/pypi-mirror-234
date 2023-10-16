=======================
The ``synodal`` package
=======================

A lightweight Python package with metadata about the code repositories of the
`Synodalsoft project <https://www.synodalsoft.net>`__.

Source code repository: https://gitlab.com/lino-framework/synodal

Usage examples:

>>> import synodal
>>> # help(synodal.Repository)
>>> from synodal import KNOWN_REPOS, REPOS_DICT, FRONT_ENDS, PUBLIC_SITES
>>> r = REPOS_DICT['synodal']
>>> print(r.git_repo)
https://gitlab.com/lino-framework/synodal.git

>>> synodal.Repository._fields
('nickname', 'package_name', 'git_repo', 'settings_module', 'front_end', 'extra_deps', 'public_url')
>>> synodal.PublicSite._fields
('url', 'settings_module', 'default_ui')

>>> for r in FRONT_ENDS:
...     print("{r.nickname} : {r.front_end}".format(r=r))
lino : lino.modlib.extjs
react : lino_react.react
openui5 : lino_openui5.openui5


>>> from importlib import import_module
>>> for ps in PUBLIC_SITES:
...     m = import_module(ps.settings_module)
...     print("{ps.url} : {m.Site.verbose_name} using {ps.default_ui}".format(
...        ps=ps, m=m))
https://voga1r.lino-framework.org : Lino Voga using lino.modlib.extjs
https://voga1e.lino-framework.org : Lino Voga using lino_react.react
https://cosi1e.lino-framework.org : Lino Così using lino.modlib.extjs
https://noi1r.lino-framework.org : Lino Noi using lino_react.react
https://weleup1.mylino.net : Lino Welfare Eupen using lino.modlib.extjs
https://welcht1.mylino.net : Lino Welfare Châtelet using lino.modlib.extjs

>>> from lino.utils.code import analyze_rst
>>> packages = [r.package_name.replace("-","_") for r in KNOWN_REPOS if r.package_name]
>>> print(analyze_rst(*packages))  #doctest: +SKIP
=============== ============ =========== =============== =============
 name            code lines   doc lines   comment lines   total lines
--------------- ------------ ----------- --------------- -------------
 synodal         101          0           10              134
 atelier         1.1k         812         386             3k
 rstgen          1.4k         910         672             4k
 etgen           509          720         300             1.9k
 eidreader       95           112         44              292
 commondata      61           4           3               88
 commondata.be   3k           70          36              3k
 commondata.ee   5k           0           70              5k
 commondata.eg   107          0           19              156
 getlino         538          1.1k        237             2k
 lino            39k          21k         10k             85k
 lino_xl         42k          13k         11k             79k
 lino_welfare    22k          9k          4k              41k
 lino_amici      3k           221         382             4k
 lino_avanti     1.2k         407         555             3k
 lino_cms        174          86          55              431
 lino_care       819          371         807             2k
 lino_cosi       411          155         213             1.0k
 lino_mentori    399          276         227             1.2k
 lino_noi        1.1k         387         733             3k
 lino_presto     983          594         531             3k
 lino_pronto     292          127         110             691
 lino_tera       1.7k         649         1.2k            5k
 lino_shop       355          132         98              756
 lino_vilma      440          185         263             1.1k
 lino_voga       1.2k         976         552             3k
 lino_weleup     188          74          95              433
 lino_welcht     781          180         341             1.7k
 lino_react      784          600         230             1.9k
 lino_openui5    242          672         236             1.4k
 lino_book       17k          3k          3k              27k
 total           145k         57k         35k             284k
=============== ============ =========== =============== =============
<BLANKLINE>

Above code snippet is skipped because the values change every day.
