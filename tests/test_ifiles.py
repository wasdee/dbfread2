from dbfread2.ifiles import ifnmatch, ipat

assert ipat('mixed') == '[Mm][Ii][Xx][Ee][Dd]'
assert ifnmatch('test', 'test')
assert ifnmatch('miXEdCaSe', 'mixedcase')
assert not ifnmatch('CAMELCASE/CamelCase', 'CamelCase/UPPERCASE')

# Pattern with
# assert ipat('[A]') == '[[Aa]]'

