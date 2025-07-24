
from fastapi import HTTPException, Request, APIRouter, Query
from fastapi.responses import JSONResponse
from fast_autocomplete import AutoComplete
from json import load

router = APIRouter()
models_directory = './dash/data/autocomplete'

autocomplete_models = {
    'en': AutoComplete(words=load(open(f'{models_directory}/en.json', 'r'))),
    'es': AutoComplete(words=load(open(f'{models_directory}/es.json', 'r'))),
    'fr': AutoComplete(words=load(open(f'{models_directory}/fr.json', 'r'))),
    'pt': AutoComplete(words=load(open(f'{models_directory}/pt.json', 'r')))
}

@router.post("/")
def complete(
    request: Request,
    language: str = Query("en"),
    limit: int = Query(7, ge=1),
    query: str = Query(..., alias="text"),
) -> JSONResponse:
    model = autocomplete_models.get(language, autocomplete_models['en'])
    stop_characters = ['.', '?', '!']
    space_count = query.count(' ')

    if any(stop in query for stop in stop_characters):
        return JSONResponse(content=[], status_code=200)
    
    if space_count >= limit:
        return JSONResponse(content=[], status_code=200)

    potential_words = []
    tokens = query.lower().rsplit(' ', 3)

    for i in range(min(3, len(tokens)), 0, -1):
        word = ' '.join(tokens[-i:])
        results = model.search(word, max_cost=10, size=10)
        potential_words += [
            token
            for phrases in results
            for token in phrases[-1].split()
            if token.startswith(tokens[-1])
        ]

    result = [
        {
            'text': word.capitalize() if len(tokens) == 1 else query.rsplit(' ', 1)[0] + ' ' + word,
            'is_match': True,
            'can_send': True
        }
        for word in dict.fromkeys(potential_words)
    ]

    return JSONResponse(
        content=result[:12],
        status_code=200
    )
