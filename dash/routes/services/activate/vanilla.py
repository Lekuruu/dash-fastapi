
from fastapi import HTTPException, Request, APIRouter, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from types import ModuleType

from dash.data.repositories import activations, penguins
from dash.data import Language
from dash import state

import i18n

router = APIRouter()

@router.get("/{language}", response_class=HTMLResponse)
def vanilla_activation_page(
    request: Request,
    language: Language,
    config: ModuleType = Depends(state.config)
) -> str:
    register_template = state.jinja2_template(
        f'activate/{language.value}.html'
    )
    return register_template.render(
        vanilla_play_link=config.VANILLA_PLAY_LINK,
        site_key=config.GSITE_KEY
    )

@router.get("/{language}/{code}", response_class=HTMLResponse)
def vanilla_activation_autofill(
    code: str,
    request: Request,
    language: Language,
    config: ModuleType = Depends(state.config)
) -> str:
    register_template = state.jinja2_template(
        f'activate/{language.value}.html'
    )
    return register_template.render(
        vanilla_play_link=config.VANILLA_PLAY_LINK,
        site_key=config.GSITE_KEY,
        activation_key=code
    )

@router.post("/{language}/")
def vanilla_activation(
    request: Request,
    language: Language,
    database: Session = Depends(state.database_session),
    config: ModuleType = Depends(state.config),
    username: str = Form(..., alias="name"),
    activation_key: str = Form(..., alias="activationcode"),
    recaptcha_response: str | None = Form(None, alias="recaptcha_response"),
) -> RedirectResponse:
    if not validate_recaptcha(recaptcha_response, config):
        raise HTTPException(
            status_code=400,
            detail=i18n.t("activate.captcha_invalid", locale=language.value)
        )

    if not (penguin := penguins.fetch_by_name_case_insensitive(username, database)):
        raise HTTPException(
            status_code=404,
            detail=i18n.t("activate.username_404", locale=language.value)
        )

    if not (activation := activations.fetch_one(activation_key, database)):
        raise HTTPException(
            status_code=404,
            detail=i18n.t("activate.activation_key_404", locale=language.value)
        )

    if penguin.id != activation.penguin_id:
        raise HTTPException(
            status_code=403,
            detail=i18n.t("activate.incorrect_username", locale=language.value)
        )

    was_updated = penguins.update(
        penguin.id,
        {'active': True},
        session=database
    )

    if not was_updated:
        raise HTTPException(
            status_code=500,
            detail=i18n.t("activate.error", locale=language.value)
        )

    activations.delete(activation_key, database)
    return RedirectResponse(config.VANILLA_ACTIVATE_REDIRECT)

def validate_recaptcha(recaptcha_response: str | None, config: ModuleType) -> bool:
    if not config.GSECRET_KEY:
        # Recaptcha is not configured
        return True

    if not recaptcha_response:
        # No recaptcha response provided
        return False

    requests = state.requests()
    response = requests.post(
        config.GCAPTCHA_URL,
        data={
            'secret': config.GSECRET_KEY,
            'response': recaptcha_response
            # TODO: Add remote IP
        }
    )

    if response.ok:
        return False

    data = response.json()
    return data.get('success', False)
