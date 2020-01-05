# stds

mlaby stds are Python modules that convert standards into JSON or python-dictionary like structures.

## stds in a nutshell

### stdcurrency.py

```text
$ python stdcurrency.test.py

...
nick: AFN is: [971, 'Afghani', 1]
...
nick: EUR is: [978, 'Euro', 35]
...
nick: GBP is: [826, 'Pound Sterling', 4]
...
nick: USD is: [840, 'US Dollar', 19]
...
nick: ZWL is: [932, 'Zimbabwe Dollar', 1]

...
Histog.: 978 (EUR) Euro (appears 35*)
	...
	at: IRELAND
	at: PORTUGAL
	at: FRANCE
	...
Histog.:  36 (AUD) Australian Dollar (appears 8*)
	at: KIRIBATI
	...
	at: AUSTRALIA
```
- **stdcurrency.test.py** tests:
  + stdcurrency.py
  + and shows the current structures.
    - in particular:
      it shows the major entities adopting a given currency, ordered by the most referenced ones (not necessarily the most important ones).
- if you use an xml file as parameter:
  + _stdcurrency.test.py a.xml_
  + it will show the structures, e.g. _**dict_ISO4217**_


## Python 3 support

Python scripts/ modules are Python 3 compatible, and were not tested against legacy Python 2.


## Namespace support

ToDo.

## Ok, how do I get it?

### Using pypi

ToDo.!

```sh
$ pip install mlaby
```

