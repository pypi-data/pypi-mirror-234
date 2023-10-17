replacements = {
    'а': ('а', 'a'),
    'б': ('б', '6'),
    'в': ('в', ),
    'г': ('г', ),
    'д': ('д', ),
    'е': ('е', 'e'),
    'ё': ('ё', 'е', 'e'),
    'ж': ('ж', ),
    'з': ('з', '3'),
    'и': ('и', ),
    'й': ('й', ),
    'к': ('к', ),
    'л': ('л', ),
    'м': ('м', ),
    'н': ('н', 'h'),
    'о': ('о', 'o'),
    'п': ('п'),
    'р': ('р', 'p'),
    'с': ('с', 'c'),
    'т': ('т', 't'),
    'у': ('у', 'y'),
    'ф': ('ф', ),
    'х': ('х', 'x'),
    'ц': ('ц', ),
    'ч': ('ч', ),
    'ш': ('ш', ),
    'щ': ('щ', ),
    'ъ': ('ъ', 'ь'),
    'ы': ('ы'),
    'ь': ('ь', 'ъ'),
    'э': ('э'),
    'ю': ('ю'),
    'я': ('я')
}


def make_forms(token, prefix = '', index = 0):
    if index < len(token):
        for replacement in replacements.get(token[index], (token[index], )):
            for token_form in make_forms(token, prefix = f'{prefix}{replacement}', index = index + 1):
                yield token_form
    else:
        yield prefix
