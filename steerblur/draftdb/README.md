# teq

## teq.ttext module

### ttext in a nutshell

*ttext* stands for tabular-text, and is originally based on '.tsv' files 
(tab-separated text files, similar to .csv, but not using colon, rather, 
tab -- character 0x08 ASCII).

Here follows a quick example:
- 4 tabular files related with stocks: [git, here](https://github.com/serrasqueiro/codeclone/tree/master/steerblur/anacondy_com/common_dict/wstocks/)

```import teq.ttext as ttext
dname = "wstocks/"
ttb = ttext.TsvBase()
assert ttb.read_files(ttb.scan_tsv(dname)) == 0
fname_list, heads, content, msgs = ttb.get_table("isin_ref")
assert not msgs
_, fields = heads
nlines, encoding, payload = content
```
You can iterate and show the key ('ISIN') using:
`for isin, memo, long_name in [line.split("\t") for line in payload]: print(i
sin)`
An alternative is:
```
adict = dict()
for isin, memo, long_name in [line.split("\t") for line in payload]:
    assert isin not in adict
    adict[isin] = (memo, long_name)
```
Then you can consult, or print the keys sorted alphabetically:
`sorted(adict)` or `sorted(adict, key=str.casefold)`

At this point there is no fancy handling of dictionaries.
For that matter, please check `table.tabular` or `table.stable` at:
- [git hub - table](https://github.com/serrasqueiro/prizedseason/tree/master/cotagente/packages/table)

