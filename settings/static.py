URL = 'https://www.volby.cz/pls/prez2023/vysledky'
KRAJE_URL = 'https://www.volby.cz/pls/prez2023/vysledky_krajmesta'
EXTRA_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language': 'en-US,en;q=0.5',
	'Upgrade-Insecure-Requests': '1',
}
CANDIDATE_MAP = {
	1: 'fischer',
	2: 'basta',
	4: 'pavel',
	5: 'zima',
	6: 'nerudova',
	7: 'babis',
	8: 'divis',
	9: 'hilser',
}
