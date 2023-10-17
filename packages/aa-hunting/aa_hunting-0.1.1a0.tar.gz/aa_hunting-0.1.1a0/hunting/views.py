from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from allianceauth.eveonline.models import EveCharacter
from allianceauth.services.hooks import get_extension_logger
from esi.decorators import token_required

from .models import LocateChar, LocateCharMsg, Target, TargetAlt

logger = get_extension_logger(__name__)

CHARACTER_SCOPES = ['esi-characters.read_notifications.v1']


@login_required
@permission_required("hunting.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """
    targets = Target.objects.all()

    context = {
        "targets": targets,
    }

    return render(request, "hunting/index.html", context)


@login_required
@permission_required("hunting.basic_access")
def target_details(request: WSGIRequest, target_id: int) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """
    target = Target.objects.get(id=target_id)

    context = {
        "target": target,
    }

    return render(request, "hunting/target_details.html", context)


@login_required
@permission_required("hunting.basic_access")
def alt_details(request: WSGIRequest, alt_id: int) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """
    targetalt = TargetAlt.objects.get(id=alt_id)

    context = {
        "targetalt": targetalt,
    }

    return render(request, "hunting/alt_details.html", context)


@login_required
@permission_required("hunting.basic_access")
def agent_details(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """
    characters = request.user.character_ownerships.all()
    valid_agents = LocateChar.objects.filter(character__is_in=characters)

    context = {
        "target": valid_agents,
    }

    return render(request, "hunting/agent_details.html", context)


@login_required
@token_required(scopes=CHARACTER_SCOPES)
def add_char(request, token) -> HttpResponse:
    try:
        try:
            character = EveCharacter.objects.get(
                character_id=token.character_id)
        except EveCharacter.DoesNotExist:
            character = EveCharacter.objects.create_character(
                character_id=token.character_id
            )
        LocateChar.objects.create(character=character)
        messages.success(request, f"Locate Character {token.character_name} Added")
    except IntegrityError:
        messages.info(request, f"Locate Character {token.character_name} is already added")

    return redirect('hunting:index')


@login_required
@permission_required("hunting.locator_view")
def locate_history(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # is_ajax
        character_id = request.GET.get('character_id', None)
    else:
        character_id = None

    locates = LocateCharMsg.objects.filter(
        character=EveCharacter.objects.get(
            character_id=character_id)).order_by('timestamp').values(
        'timestamp',
        'solar_system__name',
        'constellation__name',
        'region__name',
        'station__name',
    )

    return JsonResponse({"locate_history": list(locates)})
