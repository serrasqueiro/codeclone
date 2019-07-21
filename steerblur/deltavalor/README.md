
* RE-using aspell
The following files are re-used, and greatly simplified:
	iso-8859-1.cset

** ISO-8859-1 (latin-1) character set
aspell iso-8859-1.cset is installed e.g. at /usr/lib64/aspell-0.60/ .
The character set for Latin-1 is iso-8859-1.cset, which contains:
	<char> <uni>   The ASCII hex and unicode hex (2 and four hex numeric)
	<type>         'L' indicates 'Letters'
	<display>      'Y' indicates printable
	<upper> <lower> (equivalent upper and lower)
        <title>        Upper-case
	<plain>        Plain 7bit character; 00: no plain char
        <sl-first> <sl-rest>
The latter (sl-first, sl-rest) dictate the following:
    latin letters,
    vowels:
	sl-first as 2A (star, i.e. '*'), sl-rest 00
    non-vowels:
	sl-first shows the lower-case letter;
	special accented letters, like 'c,' (cedilla) show 'c'.

*** Scripts using cset
Basically showing the relevant western-europe, excluding 'sharp s'
or '&szlig;'; see also fileformat char 0xdf.
[comment]: # https://www.fileformat.info/info/unicode/char/00df/index.htm

	% cat other_pub/iso-8859-1.cset | grep " L " | grep -i -v sharp | grep -i -v thorn | grep -i -v eth | grep -v "# LATIN SMALL LETTER ".$ | grep -v "# LATIN CAPITAL LETTER ".$ | sed 's/ RING ABOVE/ RING/;s/# LATIN \([A-Z]\)\([A-Z]*\)\( LETTER \)\(.*\)/#\1 \4/;s/ WITH /+/' > self.txt

An exploratory command is as follow:
	% cat other_pub/iso-8859-1.cset | awk '{print $1,$3,"upper:"$5,"lower:"$6,"title:"$7,"plain:"$8,$9,$10,$11,$12,$13,$14":"$15"@"$16"%"$17}' | grep -i AE
--- in this case the two first rows show diaeresis (0xa8), which is type='-';
    

The second exploratory command is this:
	% cat other_pub/iso-8859-1.cset | awk '{print $1,$3,"sl-first:"$9,"sl-rest:"$10,$11,$12,$13,$14,$15,$16,$17}' | grep ^'[A-F][A-F0-9]' | grep " L " | sed 's/  / /g' > self_letter.txt
Then you can show single lettered with another accent:
	% cat self_letter.txt | grep 'LETTER [A-Z] '
...or multiple letters with another accent:
	% cat self_letter.txt | grep 'LETTER [A-Z][A-Z]'
The latter shows (and we are talking about ISO-8859-1):
	capital and small...
		AE
		ETH
		THORN
	and 'sharp s' (i.e. '&sslig;').
