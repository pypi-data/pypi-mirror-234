from fastapi import APIRouter, Request, Depends, status
from starlette.responses import HTMLResponse

from .service import template_service, templates_name, RequestContext
from ..auth.user_forms import AuthUserDataForm

page_router = APIRouter(
	tags=["Pages"],
	dependencies=[],
	responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@page_router.get("/", response_class=HTMLResponse)
async def auth_page(request: Request):
	return template_service.generate_template(templates_name.get('auth_panel'),
	                                          RequestContext(request=request))


@page_router.post('/user-page', response_class=HTMLResponse)
async def user_page(
		request: Request,
		data_form: AuthUserDataForm = Depends(AuthUserDataForm.as_form),
):
	return template_service.generate_user_page_template(templates_name.get('user_panel'),
	                                                    dict(request=request, data=data_form))
