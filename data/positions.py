positions = {}


positions['af'] = positions['am'] = positions['cy'] = positions['en'] = positions['es-419'] = positions['es-BO'] = positions['es-CR'] = positions['es-CU'] = positions['es-DO'] = positions['es-GQ'] = positions['es-GT'] = positions['es-HN'] = positions['es-MX'] = positions['es-NI'] = positions['es-PA'] = positions['es-PE'] = positions['es-PR'] = positions['es-SV'] = positions['es-US'] = positions[
    'fil'] = positions['ga'] = positions['gl'] = positions['gu'] = positions['hi'] = positions['id'] = positions['ja'] = positions['km'] = positions['kn'] = positions['ko'] = positions['ml'] = positions['mr'] = positions['ms'] = positions['pt'] = positions['si'] = positions['sw'] = positions['te'] = positions['th'] = positions['zh'] = positions['zu'] = lambda symbol, amount, minus: minus + symbol + amount


positions['ar'] = positions['az'] = positions['de-AT'] = positions['de-LI'] = positions['en-AT'] = positions['en-IN'] = positions['en-US-POSIX'] = positions['es-AR'] = positions['es-CO'] = positions['es-UY'] = positions['hy'] = positions['mk'] = positions[
    'mn'] = positions['ms-BN'] = positions['my'] = positions['nb'] = positions['ne'] = positions['pa'] = positions['root'] = positions['ta'] = positions['to'] = positions['ur'] = positions['vi'] = lambda symbol, amount, minus: minus + symbol + ' ' + amount


positions['be'] = positions['bg'] = positions['bs'] = positions['ca'] = positions['cs'] = positions['da'] = positions['de'] = positions['el'] = positions['en-150'] = positions['en-BE'] = positions['en-DE'] = positions['en-DK'] = positions['en-FI'] = positions['en-SE'] = positions['en-SI'] = positions['es'] = positions['et'] = positions['eu'] = positions['fi'] = positions['fo'] = positions['fr'] = positions['he'] = positions['hr'] = positions['hu'] = positions['is'] = positions['it'] = positions['ka'] = positions[
    'kk'] = positions['ky'] = positions['lt'] = positions['lv'] = positions['nl-BE'] = positions['pl'] = positions['pt-AO'] = positions['pt-CV'] = positions['pt-GW'] = positions['pt-MO'] = positions['pt-MZ'] = positions['pt-PT'] = positions['pt-ST'] = positions['pt-TL'] = positions['ro'] = positions['ru'] = positions['sk'] = positions['sl'] = positions['sq'] = positions['sr'] = positions['sv'] = positions['tr'] = positions['uk'] = positions['uz'] = lambda symbol, amount, minus: minus + amount + ' ' + symbol


positions['bn'] = lambda symbol, amount, minus: minus + amount + symbol


positions['de-CH'] = positions['en-CH'] = positions['fr-CH'] = positions['it-CH'] = lambda symbol, amount, minus: symbol + \
    minus + amount if minus else symbol + ' ' + amount


positions['en-NL'] = positions['es-PY'] = positions['nl'] = lambda symbol, amount, minus: symbol + \
    ' ' + minus + amount if minus else symbol + ' ' + amount


positions['es-CL'] = positions['es-EC'] = positions['es-VE'] = positions[
    'lo'] = lambda symbol, amount, minus: symbol + minus + amount if minus else symbol + amount


positions['fa'] = lambda symbol, amount, minus: '‎' + minus + symbol + amount
