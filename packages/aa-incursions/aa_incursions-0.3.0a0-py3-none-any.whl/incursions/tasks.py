import datetime

from celery import shared_task
from eveuniverse.models import EveConstellation, EveSolarSystem

from allianceauth.eveonline.models import EveFactionInfo

from incursions.helpers import (
    embed_boss_spawned, embed_ended, embed_established,
    embed_established_addendum, embed_mobilizing, embed_withdrawing,
)
from incursions.models import Incursion, IncursionInfluence, IncursionsConfig
from incursions.providers import get_incursions_incursions


@shared_task
def update_incursions():
    incursions, response = get_incursions_incursions()
    actives = []
    for incursion in incursions:
        actives.append(incursion['constellation_id'])
        try:
            # Get, because i need to do more steps than an update_or_create would let me
            # Also incursions have no unique id.... wtf ccp
            i = Incursion.objects.get(
                constellation=EveConstellation.objects.get_or_create_esi(
                    id=incursion['constellation_id'])[0],
                ended_timestamp__isnull=True)
            if incursion['state'] == "established":
                # This is still just an established incursion, nothing to act on
                pass
            elif incursion['state'] == "mobilizing" and i.state != Incursion.States.MOBILIZING:
                i.mobilizing_timestamp = datetime.datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z')
                i.state = Incursion.States.MOBILIZING
                i.save(update_fields=["mobilizing_timestamp", "state"])
            elif incursion['state'] == "withdrawing " and i.state != Incursion.States.WITHDRAWING:
                i.withdrawing_timestamp = datetime.datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z')
                i.state = Incursion.States.WITHDRAWING
                i.save(update_fields=["withdrawing_timestamp", "state"])
            else:
                # ????
                pass
            IncursionInfluence.objects.create(
                incursion=i,
                influence=incursion['influence'],
                timestamp=datetime.datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z')
            )
        except Incursion.DoesNotExist:
            # Create an Incursion
            i = Incursion.objects.create(
                constellation=EveConstellation.objects.get_or_create_esi(
                    id=incursion['constellation_id'])[0],
                faction=EveFactionInfo.objects.get_or_create(
                    faction_id=incursion['faction_id'])[0],
                has_boss=incursion['has_boss'],
                staging_solar_system=EveSolarSystem.objects.get_or_create_esi(
                    id=incursion['staging_solar_system_id'])[0],
                state=incursion['state'],
                type=incursion['type'],
                established_timestamp=datetime.datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z')
            )
            IncursionInfluence.objects.create(
                incursion=i,
                influence=incursion['influence'],
                timestamp=datetime.datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z')

            )
    for ended in Incursion.objects.filter(ended_timestamp__isnull=True).exclude(constellation_id__in=actives):
        # Cant use update here, need to fire signals
        ended.ended_timestamp = datetime.datetime.strptime(
            str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z')
        ended.state = Incursion.States.ENDED
        ended.save(update_fields=["ended_timestamp", "state"])


@shared_task
def incursion_established(incursion_pk: int):
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        webhook.send_embed(embed=embed_established(incursion))
        webhook.send_embed(embed=embed_established_addendum(incursion))


@shared_task
def incursion_mobilizing(incursion_pk: int):
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        webhook.send_embed(embed=embed_mobilizing(incursion))


@shared_task
def incursion_withdrawing(incursion_pk: int):
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        webhook.send_embed(embed=embed_withdrawing(incursion))


@shared_task
def incursion_ended(incursion_pk: int):
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        webhook.send_embed(embed=embed_ended(incursion))


@shared_task
def incursion_boss_spawned(incursion_pk: int):
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        webhook.send_embed(embed=embed_boss_spawned(incursion))


@shared_task
def recreate_history():
    # Step through eve-ref data and recreate incursion history.
    pass
