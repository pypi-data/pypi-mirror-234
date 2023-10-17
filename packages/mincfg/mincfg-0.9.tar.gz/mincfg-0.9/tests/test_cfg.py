
import os

from mincfg import MergedConfiguration
from mincfg import DictSource, OSEnvironSource, SubsetSource, YamlFileSource, INIFileSource, DotEnvFileSource


D1 = DictSource({
        'a': '11', 
        'B': '12',
        'C': { 
            'Ca': '131', 
            'CB': '132'
        }
    })

D2 = DictSource({
        'A': '21',
        'c': {
            'ca': '231',
            'cc': '233'
        },
        'd': '24',
    })



def test_merged_case_insensitive():

    config = MergedConfiguration([D1, D2])

    assert config.get('a') == '21'
    assert config.get('b') == '12'
    assert config.get('d') == '24'

    for k in ('a', 'b', 'd'):
        assert config.get(k.lower()) == config.get(k.upper())


def test_as_dict():

    config = MergedConfiguration([D1])

    c = config.as_dict()
    assert c['c']['ca'] == '131'
    assert c['c']['cb'] == '132'

    c = config.as_dict(['c'])
    assert c['ca'] == '131'
    assert c['cb'] == '132'


def test_as_ns():

    config = MergedConfiguration([D1])

    c = config.as_ns()
    assert c.a == '11'
    assert c.b == '12'
    assert c.c.ca == '131'
    assert c.c.cb == '132'

    c = config.as_ns(['c'])
    assert c.ca == '131'
    assert c.cb == '132'


def test_as_configparser():

    config = MergedConfiguration([D1])

    c = config.as_configparser()
    assert c['c']['ca'] == '131'
    assert c['c']['cb'] == '132'
    assert 'c' in c.sections()


def test_osenviron_source():

    cur_keys = set(os.environ.keys())
    os.environ.update({
        'MINCFGTST_A': 'a',
        'MINCFGTST_B': 'b',
        'MINCFGTST_C_A': 'ca',
        'MINCFGTST_C_B': 'cb',
    })

    shell = os.environ.get('SHELL', 'no-shell-defined')
    user = os.environ.get('USER', 'unknown user')

    config = MergedConfiguration([OSEnvironSource('MINCFGTST')])
    assert config.get('a') == 'a'
    assert config.get('b') == 'b'
    assert config.get('a', namespace=['c']) == 'ca'
    assert config.get('b', namespace=['c']) == 'cb'


def test_subset_source():

    a = {'a': '1',
         'b': '1',
         'c': '1'
        }
    b = {'a': '2',
         'b': '2',
         'c': '2'
        }
    a_src = DictSource(a)
    b_src = DictSource(b)
    config = MergedConfiguration([a_src, b_src, SubsetSource(a_src, set('a'))])

    assert config.get('a') == '1'
    assert config.get('b') == '2'
    assert config.get('c') == '2'


def test_yaml_file_source(tmp_path):

    nonexistantsrc = YamlFileSource(None)

    # make up a tempfile name
    cfgfile = tmp_path / "config.yaml"

    # write test config to the temp file
    cfgfile.write_text("a: 1\nb: 2\nc:\n  ca: 3\n  cb: 4\n\n")

    cfgfilesrc = YamlFileSource(str(cfgfile))

    # point the config at it
    config = MergedConfiguration([nonexistantsrc, cfgfilesrc])

    assert config.get('a') == '1'
    assert config.get('b') == '2'
    assert config.get('ca', namespace=['c']) == '3'
    assert config.get('cb', namespace=['c']) == '4'


def test_ini_file_source(tmp_path):

    nonexistantsrc = INIFileSource(None)

    # make up a tempfile name
    cfgfile = tmp_path / "config.ini"

    # write test config to the temp file
    cfgfile.write_text("a = 1\nb=2\n[c]\nca = 3\ncb = 4\n\n")

    cfgfilesrc = INIFileSource(str(cfgfile))

    # point the config at it
    config = MergedConfiguration([nonexistantsrc, cfgfilesrc])

    assert config.get('a') == '1'
    assert config.get('b') == '2'
    assert config.get('ca', namespace=['c']) == '3'
    assert config.get('cb', namespace=['c']) == '4'


def test_dotenv_file_source(tmp_path):

    nonexistantsrc = DotEnvFileSource(None)

    # make up a tempfile name
    cfgfile = tmp_path / "config.env"

    # write test config to the temp file
    cfgfile.write_text("a=1\nb=2\nc_a=3\nc_b=4\n\n")

    cfgfilesrc = DotEnvFileSource(str(cfgfile))

    # point the config at it
    config = MergedConfiguration([nonexistantsrc, cfgfilesrc])

    assert config.get('a') == '1'
    assert config.get('b') == '2'
    assert config.get('a', namespace=['c']) == '3'
    assert config.get('b', namespace=['c']) == '4'



