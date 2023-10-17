import datetime
import random
from typing import Union

from discord import Embed
from eveuniverse.models import EveRegion, EveSolarSystem, EveStation, EveType

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Q, QuerySet, Sum

from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger
from esi.models import Token

from marketmanager.app_settings import (
    MARKETMANAGER_WEBHOOK_COLOUR_INFO, MARKETMANAGER_WEBHOOK_COLOUR_WARNING,
    get_site_url,
)
from marketmanager.models import (
    Order, PriceConfig, PrivateConfig, Structure, SupplyConfig, TypeStatistics,
)

from . import __version__
from .providers import get_characters_character_id_roles_from_token

logger = get_extension_logger(__name__)


def get_corp_token(corporation_id: int, scopes: list, req_roles: list) -> Token:
    """
    Helper method to get a token for a specific character from a specific corp with specific scopes
    :param corp_id: Corp to filter on.
    :param scopes: array of ESI scope strings to search for.
    :param req_roles: roles required on the character.
    :return: :class:esi.models.Token or False
    """
    if 'esi-characters.read_corporation_roles.v1' not in scopes:
        scopes.append("esi-characters.read_corporation_roles.v1")

    char_ids = EveCharacter.objects.filter(
        corporation_id=corporation_id).values('character_id')
    tokens = Token.objects \
        .filter(character_id__in=char_ids) \
        .require_scopes(scopes)

    for token in tokens:
        roles = get_characters_character_id_roles_from_token(token)
        has_roles = False
        for role in roles.get('roles', []):
            if role in req_roles:
                has_roles = True

        if has_roles:
            return token
        else:
            pass  # TODO Maybe remove token?

    return False


def get_random_market_token() -> Union[Token, bool]:
    """Very specific edge case, we need _any_ token in order to view data on public structures.

    Args:
        scopes: array of ESI scope strings to search for.

    Returns:
        Matching token
    """
    required_scopes = ['esi-markets.structure_markets.v1']
    try:
        random_token = random.choice(
            Token.objects.all().require_scopes(
                required_scopes
            )
        )
        return random_token
    except Exception as e:
        logger.error(e)
        return False


def is_existing_order(order, current_orders):
    try:
        existing_order = current_orders.get(order_id=order["order_id"])
        return existing_order
    except ObjectDoesNotExist:
        return False


def get_matching_privateconfig_token(structure_id: int) -> Union[Token, bool]:
    structure = Structure.objects.get(structure_id=structure_id)

    configured_tokens = PrivateConfig.objects.filter(valid_structures=structure)
    if configured_tokens.count() == 0:
        try:
            structure = Structure.objects.get(structure_id=structure_id)
            corporation = EveCorporationInfo.objects.get(
                corporation_id=structure.owner_id)
        except ObjectDoesNotExist:
            return False
        configured_tokens = PrivateConfig.objects.filter(valid_corporations=corporation)
    try:
        return random.choice(configured_tokens).token
    except IndexError:
        return False


def create_embed_base(config: Union[SupplyConfig, PriceConfig]):
    embed = Embed()
    embed.timestamp = datetime.datetime.now()
    embed.set_footer(
        icon_url="",
        text=f"AA Market Manager v{__version__}"
    )

    if config.buy_order is True:
        buy_order_string = "BUY"
    else:
        buy_order_string = "SELL"
    embed.add_field(
        name="Order",
        value=buy_order_string,
        inline=True
    )

    if config.structure.count() > 0 or config.solar_system.count() > 0 or config.region.count() > 0:
        locations_string = ""
        for structure in config.structure.all():
            locations_string = locations_string + f"{structure.name} \n"
        for solar_system in config.solar_system.all():
            locations_string = locations_string + f"{solar_system.name} \n"
        for region in config.region.all():
            locations_string = locations_string + f"{region.name} \n"
        if locations_string == "":
            locations_string = "New Eden"
        embed.add_field(
            name="Locations",
            value=locations_string,
            inline=False
        )

    if config.structure_type.count() > 0:
        structure_type_string = ""
        for type in config.structure_type.all():
            structure_type_string = structure_type_string + f"{type.name} \n"

        embed.add_field(
            name="Structure_Types",
            value=structure_type_string,
            inline=False
        )

    return embed


def create_embed_supply(
        config: SupplyConfig,
        matched_volume: int,
        description: str,
        calculated_price: int = 0,
        colour: int = MARKETMANAGER_WEBHOOK_COLOUR_INFO):

    embed = create_embed_base(config)
    embed.title = f"{config.eve_type.name}"
    embed.url = f"{get_site_url()}/marketmanager/marketbrowser?type_id={config.eve_type.id}"
    embed.set_thumbnail(url=config.eve_type.icon_url())
    embed.description = description
    embed.colour = colour
    embed.insert_field_at(
        index=2,
        name="Volume",
        value=f"{matched_volume:,} / {config.volume:,}",
        inline=True
    )
    if config.jita_compare_percent != 0:
        embed.insert_field_at(
            index=3,
            name=f"Jita {config.jita_compare_percent:,}%",
            value=f"{calculated_price:,} ISK",
            inline=True
        )
    elif config.price != 0:
        embed.insert_field_at(
            index=3,
            name="Price",
            value=f"{config.price:,} ISK",
            inline=True
        )

    if config.managed_supply_config is not None:
        if config.managed_supply_config.managed_app == 'fittings':
            managed_app = "AA-Fittings"
        else:
            managed_app = config.managed_supply_config.managed_app

        embed.add_field(
            name=managed_app,
            value=f"{config.managed_supply_config.managed_app_reason} x{config.managed_supply_config.managed_quantity}",
            inline=True
        )

    return embed


def create_embed_price(
        config: PriceConfig,
        description: str,
        calculated_price: int = 0,
        colour: int = MARKETMANAGER_WEBHOOK_COLOUR_INFO):

    embed = create_embed_base(config)
    if config.scalp is True:
        embed.title = 'Price Check: Scalping'
    else:
        embed.title = 'Price Check: Bargains'
    embed.url = f"{get_site_url()}/marketmanager/marketbrowser"
    # embed.set_thumbnail(url=config.eve_type.icon_url())
    embed.description = description
    embed.colour = MARKETMANAGER_WEBHOOK_COLOUR_WARNING

    if config.jita_compare_percent != 0:
        embed.insert_field_at(
            index=2,
            name=f"Jita {config.jita_compare_percent:,}%",
            value="\u200b",
            inline=True
        )
    elif config.price != 0:
        embed.insert_field_at(
            index=2,
            name="Price",
            value=f"{config.price:,} ISK",
            inline=True
        )

    return embed


def fifth_percentile(eve_type: EveType, eve_region: EveRegion = EveRegion(None), buy_order: bool = False):
    if eve_region.id is None:
        orders = Order.objects.filter(
            eve_type=eve_type, is_buy_order=buy_order).order_by('price')
    else:
        orders = Order.objects.filter(
            eve_type=eve_type, eve_region=eve_region, is_buy_order=buy_order).order_by('price')

    if buy_order is True:
        orders.reverse

    total_volume = orders.aggregate(volume=Sum(F('volume_remain')))['volume']
    if total_volume is None or 0:
        return 0

    cumulative_volume = 0

    for order in orders:
        cumulative_volume = cumulative_volume + order.volume_remain
        if cumulative_volume > (total_volume * 0.05):
            return order.price

    return 0


def median(eve_type: EveType, eve_region: EveRegion = EveRegion(None), buy_order: bool = False):
    # Hey median is just 50th percentile lol
    # Can we combine these?
    if eve_region.id is None:
        orders = Order.objects.filter(
            eve_type=eve_type, is_buy_order=buy_order).order_by('price')
    else:
        orders = Order.objects.filter(
            eve_type=eve_type, eve_region=eve_region, is_buy_order=buy_order).order_by('price')

    if buy_order is True:
        orders.reverse

    total_volume = orders.aggregate(volume=Sum(F('volume_remain')))['volume']
    if total_volume is None or 0:
        return 0
    cumulative_volume = 0

    for order in orders:
        cumulative_volume = cumulative_volume + order.volume_remain
        if cumulative_volume > (total_volume * 0.50):
            return order.price

    return 0


def weighted_average(eve_type: EveType, eve_region: EveRegion = EveRegion(None), buy_order: bool = False):
    if eve_region.id is None:
        orders = Order.objects.filter(eve_type=eve_type, is_buy_order=buy_order)
    else:
        orders = Order.objects.filter(
            eve_type=eve_type, eve_region=eve_region, is_buy_order=buy_order)

    total_volume = orders.aggregate(aggregate_volume=Sum(
        F('volume_remain')))['aggregate_volume']
    cumulative_price = orders.aggregate(aggregate_price=Sum(
        F('volume_remain') * F("price")))['aggregate_price']

    try:
        return cumulative_price / total_volume
    except (ZeroDivisionError, TypeError):
        return 0


def filter_orders_by_location(
        orders: QuerySet,
        config: Union[SupplyConfig, PriceConfig]
) -> QuerySet:
    if config.structure.count() > 0 or config.solar_system.count() > 0 or config.region.count() > 0:
        matching_orders_location = orders.filter(
            Q(location_id__in=config.structure.all()) | Q(eve_solar_system__in=config.solar_system.all()) | Q(eve_region__in=config.region.all()))
    else:
        matching_orders_location = orders

    if config.structure_type.count() > 0:
        valid_structures = Structure.objects.filter(
            eve_type__in=config.structure_type.all())
        matching_orders_location_type = matching_orders_location.filter(
            location_id__in=valid_structures.all())
        return matching_orders_location_type

    return matching_orders_location


def calculate_comparator_price(config: SupplyConfig):
    if config.price != 0:
        return config.price

    if config.jita_compare_percent != 0:
        try:
            type_statistics = TypeStatistics.objects.get(
                eve_type=config.eve_type,
                eve_region=EveRegion.objects.get(id=10000002))
            if config.buy_order is True:
                return type_statistics.buy_weighted_average * (config.jita_compare_percent / 100)
            if config.buy_order is False:
                return type_statistics.sell_weighted_average * (config.jita_compare_percent / 100)
        except ObjectDoesNotExist:
            return 0
    else:
        return 0


def location_resolver_to_solar_system(location_id: int) -> EveSolarSystem:
    """
    Return the Solar System for a location_id, if known

    :param location_id: _description_
    :type location_id: int
    :return: _description_
    :rtype: EveSolarSystem
    """
    if location_id >= 60000000 and location_id <= 64000000:
        try:
            station, fetched = EveStation.objects.get_or_create_esi(id=location_id)
            return station.eve_solar_system
        except Exception as e:
            logger.debug(e)
            return EveSolarSystem(None)
    else:
        try:
            return Structure.objects.get(structure_id=location_id).solar_system
        except Exception as e:
            logger.debug(e)
            return EveSolarSystem(None)
