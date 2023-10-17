import logging
from datetime import datetime, timedelta

from discord import Colour, Embed
from eveuniverse.models import EveSolarSystem

from incursions import __version__
from incursions.models import Incursion
from incursions.static_data import incursion_constellations

from .app_settings import get_site_url

logger = logging.getLogger(__name__)


def embed_base() -> Embed:
    embed = Embed(title="AA Incursions")
    embed.url = f"{get_site_url() }/incursions/"
    embed.set_thumbnail(
        url="https://images.evetech.net/types/2192/render?size=128")
    embed.set_footer(
        text=f"AA Incursions v{__version__}: Developed by Ariel Rin")
    embed.timestamp = datetime.now()
    return embed


def embed_established(incursion: Incursion) -> Embed:
    embed = embed_base()
    embed.colour = Colour.green()
    embed.title = f"New {incursion.security_string}: {incursion.constellation.name}"
    embed.description = "PSA: Create and use an Insta-Dock Bookmark when warping to the new dockup. Scout the route ahead including the dockup station."
    embed.add_field(
        name="Region",
        value=f"[{incursion.constellation.eve_region.name}]({incursion.constellation.eve_region.profile_url})",
        inline=True)
    embed.add_field(
        name="Constellation",
        value=f"[{incursion.constellation.name}]({incursion.constellation.profile_url})")
    # newline
    embed.add_field(
        name="Headquarters",
        value=incursion_constellations[incursion.constellation.name]["Headquarter"])
    embed.add_field(
        name="Assault",
        value=incursion_constellations[incursion.constellation.name]["Assaults"],
        inline=True)
    embed.add_field(
        name="Vanguard",
        value=incursion_constellations[incursion.constellation.name]["Vanguards"],
        inline=True)
    # newline
    embed.add_field(name="Stations in HQ",
                    value=f"{ EveSolarSystem.objects.get(name=incursion_constellations[incursion.constellation.name]['Headquarter']).eve_stations.count() }", inline=True)
    embed.add_field(name="HS Island?",
                    value=f"{incursion.is_island}", inline=True)
    embed.add_field(name="Jumps from last HQ", value="69420lmao", inline=True)
    # newline
    embed.add_field(name="Suggested Dockup",
                    value="Not Implemented", inline=True)
    embed.add_field(name="Edencom In Spawn",
                    value="Not Implemented", inline=True)
    embed.add_field(name="Trigs In Spawn",
                    value="Not Implemented", inline=True)
    return embed


def embed_established_addendum(incursion: Incursion) -> Embed:
    embed = embed_base()
    embed.colour = Colour.blue()
    embed.title = f"{incursion.constellation.name}"
    embed.add_field(name="Spawn Time",
                    value=f"<t:{ int(incursion.established_timestamp.timestamp()) }:R>", inline=True)
    embed.add_field(name="Despawn Window Starts",
                    value=f"<t:{ int((incursion.established_timestamp + timedelta(days=4)).timestamp()) }:R>", inline=True)
    embed.add_field(name="Despawn Window Ends",
                    value=f"<t:{ int((incursion.established_timestamp + timedelta(days=8)).timestamp()) }:R>", inline=True)
    # newline
    embed.add_field(name="Max Established Time",
                    value=f"<t:{ int((incursion.established_timestamp + timedelta(days=5)).timestamp()) }:R>")
    embed.add_field(name="HQ to Hek",
                    value=f"{incursion.staging_solar_system.jumps_to(destination=EveSolarSystem.objects.get(id=30002053)) }", inline=True)
    embed.add_field(name="HQ to Dodixie",
                    value=f"{incursion.staging_solar_system.jumps_to(destination=EveSolarSystem.objects.get(id=30002659)) }", inline=True)
    # newline
    embed.add_field(name="HQ to Rens",
                    value=f"{incursion.staging_solar_system.jumps_to(destination=EveSolarSystem.objects.get(id=30002510)) }")
    embed.add_field(name="HQ to Jita",
                    value=f"{incursion.staging_solar_system.jumps_to(destination=EveSolarSystem.objects.get(id=30000142)) }", inline=True)
    embed.add_field(name="HQ to Amarr",
                    value=f"{incursion.staging_solar_system.jumps_to(destination=EveSolarSystem.objects.get(id=30002187)) }", inline=True)
    # newline
    embed.add_field(name="Gank Pipes In Route", value="Not Implemented")
    embed.add_field(name="Edencom In Route",
                    value="Not Implemented", inline=True)
    embed.add_field(name="Edencom In Route",
                    value="Not Implemented", inline=True)
    return embed


def embed_mobilizing(incursion: Incursion) -> Embed:
    embed = embed_base()
    embed.colour = Colour.yellow()
    embed.title = f"Mobilizing {incursion.security_string}: {incursion.constellation.name}"
    embed.add_field(name="Estimated Withdrawing Time",
                    value=f"<t:{ int((incursion.mobilizing_timestamp + timedelta(days=2)).timestamp()) }:R>", inline=False)
    embed.add_field(name="Estimated Despawn Time",
                    value=f"<t:{ int((incursion.mobilizing_timestamp + timedelta(days=3)).timestamp()) }:R>", inline=False)
    embed.add_field(name="Max Spawn Stats",
                    value=f'''
                        {incursion.mobilizing_timestamp - incursion.established_timestamp} Uptime
                        {(incursion.mobilizing_timestamp - incursion.established_timestamp) - timedelta(days=5)} Unused
                        {(incursion.mobilizing_timestamp - incursion.established_timestamp).microseconds / timedelta(days=5).microseconds - 100:.3f}% total possible `established` time used")
                    ''')
    embed.add_field(name="Estimated Respawn Window Opens",
                    value=f"<t:{ int((incursion.mobilizing_timestamp + timedelta(days=3, hours=12)).timestamp()) }:R>", inline=False)
    embed.add_field(name="Estimated Respawn Window Closes",
                    value=f"<t:{ int((incursion.mobilizing_timestamp + timedelta(days=3, hours=36)).timestamp()) }:R>", inline=False)
    return embed

    # Spawn Mobilizing!
    # Estimated Withdrawing Time
    # Friday, 23 June 2023 21:37 (in a day)
    # Estimated Despawn Time
    # Saturday, 24 June 2023 21:37 (in 2 days)
    # Saturday, June 24, 2023 11:37 (Eve Time)
    # Max Spawn Stats
    # 4 days 2 hours 36 minutes established
    # 21 hours 24 minutes unused
    # 82.17% total possible "established" time used
    # Estimated Respawn Window Opens
    # Sunday, 25 June 2023 09:37 (in 3 days)
    # Estimated Respawn Window Closes
    # Monday, 26 June 2023 09:37 (in 4 days)


def embed_withdrawing(incursion: Incursion) -> Embed:
    embed = embed_base()
    embed.colour = Colour.red()
    embed.title = f"Withdrawing {incursion.security_string}: {incursion.constellation.name}"
    embed.add_field(name="Despawn Before",
                    value=f"<t:{ int((incursion.withdrawing_timestamp + timedelta(days=1)).timestamp()) }:R>", inline=False)
    embed.add_field(name="Estimated Respawn Window Opens",
                    value=f"<t:{ int((incursion.withdrawing_timestamp + timedelta(days=1, hours=12)).timestamp()) }:R>", inline=False)
    embed.add_field(name="Estimated Respawn Window Closes",
                    value=f"<t:{ int((incursion.withdrawing_timestamp + timedelta(days=1, hours=36)).timestamp()) }:R>", inline=False)
    return embed

    # Spawn Withdrawing!
    # Despawn Before
    # Saturday, 24 June 2023 21:40 (2 days ago)
    # Saturday, June 24, 2023 11:40 (Eve Time)
    # Estimated Respawn Window Opens
    # Sunday, 25 June 2023 09:40 (a day ago)
    # Estimated Respawn Window Closes
    # Monday, 26 June 2023 09:40 (2 hours ago)


def embed_ended(incursion: Incursion) -> Embed:
    embed = embed_base()
    embed.colour = Colour.red()
    embed.description = "The next spawn will occur in 12-36 hours."
    embed.title = f"Ended {incursion.security_string}: {incursion.constellation.name}"
    embed.add_field(name="Spawn Window Opens",
                    value=f"<t:{ int((incursion.established_timestamp + timedelta(days=1)).timestamp()) }:R>", inline=False)
    embed.add_field(name="Spawn Window Closes",
                    value=f"<t:{ int((incursion.established_timestamp + timedelta(days=1, hours=12)).timestamp()) }:R>", inline=False)
    embed.add_field(name="Max Spawn Stats",
                    value=f'''
                        {incursion.ended_timestamp - incursion.withdrawing_timestamp} Withdrawing
                        {(incursion.ended_timestamp - incursion.withdrawing_timestamp) + timedelta(days=1)} Unused
                        {(incursion.ended_timestamp - incursion.withdrawing_timestamp) / timedelta(days=1):.2f}% total possible `withdrawing` time used")
                    ''')
    return embed

    # Max Spawn Stats
    # 23 hours 50 minutes withdrawing
    # 10 minutes unused
    # 99.31% total possible "withdrawing" time used


def embed_boss_spawned(incursion: Incursion) -> Embed:
    embed = embed_base()
    embed.colour = Colour.yellow()
    embed.description = "Boss Spawned"
    embed.title = f"Ended {incursion.security_string}: {incursion.constellation.name}"
    return embed
