# coding: utf-8

from typing import Dict, Any

_package_data: Dict[str, Any] = dict(
    full_package_name='ryd',
    version_info=(0, 8, 0),
    __version__='0.8.0',
    version_timestamp='2023-10-10 18:09:31',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='Ruamel Yaml Doc preprocessor (pronounced: /rɑɪt/ like the verb "write")',
    keywords='restructuredtext markdown markup preprocessing',
    entry_points='ryd=ryd.__main__:main',
    extra_packages=['ryd._convertor', 'ryd._tag'],
    license='MIT',
    since=2017,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    install_requires=[
        'ruamel.std.pathlib',
        'ruamel.yaml',
    ],
    tox=dict(
        env='3',
    ),
    oitnb=dict(
        multi_line_unwrap=True,
    ),
    print_allowed=True,
    python_requires='>=3',
)  # NOQA


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

_cligen_data = """\
# all tags start with an uppercase char and can often be shortened to three and/or one
# characters. If a tag has multiple uppercase letter, only using the uppercase letters is a
# valid shortening
# Tags used:
# !Commandlineinterface, !Cli,
# !Option, !Opt, !O
# - !Option [all, !Action store_true, !Help build sdist and wheels for all platforms]
# !PreSubparserOption, !PSO
# !Help, !H
# !Argument, !Arg
# - !Arg [files, nargs: '*', !H files to process]
# !Module   # make subparser function calls imported from module
# !Instance # module.Class: assume subparser method calls on instance of Class imported from module
# !Main     # function to call/class to instantiater,, no subparsers
# !Action # either one of the actions in subdir _action (by stem of the file) or e.g. "store_action"
# !Config YAML/INI/PON  read defaults from config file
# !AddDefaults ' (default: %(default)s)'
# !Prolog (sub-)parser prolog/description text (for multiline use | )
# !Epilog (sub-)parser epilog text (for multiline use | )
# !NQS used on arguments, makes sure the scalar is non-quoted e.g for instance/method/function
#      call arguments, when cligen knows about what argument a keyword takes, this is not needed
!Cli 0:
- formatter_class: !NQS argparse.RawTextHelpFormatter
- !Epilog |
    Sections, subsections, etc. in .ryd files
      # with over-line, for parts
      * with over-line, for chapters
      =, for sections
      +, for subsections
      ^, for subsubsections
      ", for paragraphs
- !Opt [verbose, v, !Help increase verbosity level, !Action count, const: 1, nargs: 0, default: 0]
- !Opt [force, !Help 'force action, even on normally skipped files', !Action count, const: 1, nargs: 0, default: 0]
- !Instance ryd.ryd.RYD
- !Config YAML
- convert:
  - !DefaultSubparser
  - !Opt [pdf, !Action store_true, default: null, !Help postprocess to pdf]
  - !Opt [no-pdf, !Action store_false, dest: pdf]
  - !Opt [html, !Action store_true, default: null, !Help postprocess to HTML]
  - !Opt [no-html, !Action store_false, dest: html]
  - !Opt [embed, !Action store_true, !Help embed images in HTML]
  - !Opt [stdout, !Action store_true, !Help write to stdout instead of file]
  - !Opt [keep, !Action store_true, !Help preserve partial .rst/.md on execution error]
  - !Opt [generate-mkdocs-config, !Help generate the config file for mkdocs from metadata]
  - !Arg [file, nargs: +, !Help files to process]
  - !Help generate output as per first YAML document
- clean:
  - !Arg [file, nargs: +, !Help files to process]
  - !Help clean output files for .ryd files
- roundtrip:
  # - !Opt [formatter, f, nargs: +, !Help 'formatter specification (tag cmd [option, ...])']
  - !Arg [file, nargs: +, !Help files to process]
  - !Help roundtrip .ryd file, updating sections
- from-rst:
  - !Help convert .rst to .ryd with some section anylysis
  - !Option [output, o, !H 'write to file (default argument with .ryd suffix)']
  - !Arg [file, nargs: +, !Help files to process]
- rst-md:
  - !Help convert .ryd file from reST content to markdown  content
  - !Arg [file, nargs: +, !Help files to process]
- serve:
  - !Help use mkdocs serve -f .mkdocs.yaml to serve .md files
"""  # NOQA
