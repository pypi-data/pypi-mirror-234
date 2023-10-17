import logging
from datetime import datetime

from discord import AutocompleteContext, Option
from discord.commands import SlashCommandGroup
from discord.embeds import Embed
from discord.ext import commands
from eveuniverse.models import EveRegion, EveSolarSystem
from rapidfuzz import fuzz, process

from django.conf import settings

from allianceauth.services.modules.discord.models import DiscordUser

from drifters import __version__
from drifters.app_settings import JOVE_OBSERVATORIES
from drifters.models import Clear, Wormhole

logger = logging.getLogger(__name__)


class Drifters(commands.Cog):
    """
    Drifter Wormhole Mapping and Management
    From AA-Drifters
    """

    def __init__(self, bot):
        self.bot = bot

    drifter_commands = SlashCommandGroup(
        "drifters", "Drifter Wormholes", guild_ids=[int(settings.DISCORD_GUILD_ID)])

    async def search_solar_systems(self, ctx: AutocompleteContext):
        """
        Returns a subset of solar systems, known to have jove observatories, that begin with the characters entered so far

        :param ctx: _description_
        :type ctx: AutocompleteContext
        :return: Fuzzy Searched list of solar systems as a list of strings.
        :rtype: list
        """
        return [i[0] for i in process.extract(ctx.value, JOVE_OBSERVATORIES, scorer=fuzz.WRatio, limit=10)]

    async def search_regions(self, ctx: AutocompleteContext):
        """
        Returns a list of EveSolarSystems that begin with the characters entered so far

        :param ctx: _description_
        :type ctx: AutocompleteContext
        :return: _description_
        :rtype: list
        """
        return list(EveRegion.objects.filter(name__icontains=ctx.value).values_list('name', flat=True)[:10])

    @drifter_commands.command(name="about", description="About the Discord Bot", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def about(self, ctx):
        """
        All about the bot
        """
        embed = Embed(title="AA Drifters")
        embed.description = "https://gitlab.com/tactical-supremacy/aa-drifters\nShvo please come back"
        embed.url = "https://gitlab.com/tactical-supremacy/aa-drifters"
        embed.set_thumbnail(url="https://images.evetech.net/types/34495/render?size=128")
        embed.set_footer(
            text="Developed for INIT and publicly available to encourage destruction by Ariel Rin")
        embed.add_field(
            name="Version", value=f"{__version__}", inline=False
        )

        return await ctx.respond(embed=embed)

    @drifter_commands.command(name="clear", description="Report a system as Clear of drifter holes", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def clear(
        self, ctx,
        system=Option(str, "Solar System", autocomplete=search_solar_systems),
    ):
        """
        Adds a Clear record and optionally tidies up any holes in the system
        """
        archived_holes = 0
        try:
            clear_report, created = Clear.objects.get_or_create(
                system=EveSolarSystem.objects.get(name=system))
            if created is True:
                clear_report.created_at = datetime.now()
                clear_report.created_by = DiscordUser.objects.get(uid=ctx.user.id).user
            else:
                clear_report.updated_at = datetime.now()
                clear_report.updated_by = DiscordUser.objects.get(uid=ctx.user.id).user
            clear_report.save()
        except EveSolarSystem.DoesNotExist as e:
            logger.error(e)
            return await ctx.respond(f"System {system} not found")
        except DiscordUser.DoesNotExist as e:
            logger.error(e)
            return await ctx.respond("User not Found")
        except Exception as e:
            logger.error(e)

        try:
            archived_holes = Wormhole.objects.filter(
                system=EveSolarSystem.objects.get(name=system),
                archived=False
            ).update(
                archived=True,
                archived_at=datetime.now(),
                archived_by=DiscordUser.objects.get(uid=ctx.user.id).user)
        except EveSolarSystem.DoesNotExist as e:
            logger.error(e)
            return await ctx.respond(f"System {system} not found")
        except DiscordUser.DoesNotExist as e:
            logger.error(e)
            return await ctx.respond("User not Found")
        except Exception as e:
            logger.error(e)

        if created is True:
            return await ctx.respond(f"{system} Marked as Clear for the first time, {archived_holes} Wormholes archived")
        elif created is False:
            return await ctx.respond(f"{system} Updated as Clear, {archived_holes} Wormholes archived")
        else:
            return await ctx.respond(f"{system} Unable to confirm=, please try again. {archived_holes} Wormholes archived")

    @drifter_commands.command(name="add", description="Add a Drifter wormhole in a K-Space system", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def add_wormhole(
        self, ctx,
        system=Option(str, "Solar System", autocomplete=search_solar_systems),
        complex=Option(str, "Drifter Complex", choices=Wormhole.Complexes.values),
        mass=Option(str, "Mass Status", choices=Wormhole.Mass.values),
        lifetime=Option(str, "Life Remaining", choices=Wormhole.Lifetime.values),
        bookmarked_k=Option(bool, "K Space Bookmarked?", default='True', choices=["True", "False"]),
        bookmarked_w=Option(bool, "W Space Bookmarked?", default='True', choices=["True", "False"])
    ):
        """
        Adds a drifter hole record
        """
        await ctx.trigger_typing()

        try:
            Clear.objects.get(EveSolarSystem.objects.get(name=system)).delete()
        except Exception as e:
            logger.error(e)
        try:
            Wormhole.objects.create(
                system=EveSolarSystem.objects.get(name=system),
                complex=complex,
                mass=mass,
                lifetime=lifetime,
                created_at=datetime.now(),
                created_by=DiscordUser.objects.get(uid=ctx.user.id).user,
                bookmarked_k=bookmarked_k,
                bookmarked_w=bookmarked_w,
            )
        except EveSolarSystem.DoesNotExist:
            return await ctx.respond(f"System:{system} not found")
        except DiscordUser.DoesNotExist:
            return await ctx.respond("User not Found")
        except Exception as e:
            logger.error(e)

        return await ctx.respond(f"Saved {complex} hole in {system}, {mass}, {lifetime} <t:{datetime.now():.0}:R>")

    @drifter_commands.command(name="complex_list", description="List wormholes leading to a complex", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def list_complex_wormholes(
        self, ctx,
        complex=Option(str, "Drifter Complex", choices=Wormhole.Complexes.values)
    ):
        """
        list_complex_wormholes _summary_

        :param ctx: _description_
        :type ctx: _type_
        :param complex: _description_, defaults to Option(str, "Drifter Complex", choices=Wormhole.Complexes.values)
        :type complex: _type_, optional
        :return: _description_
        :rtype: _type_
        """
        embed = Embed(title=f"AA-Drifters: {complex}")

        for wormhole in Wormhole.objects.filter(complex=complex, archived=False):
            embed.add_field(
                name=wormhole.system.name, value=f"Mass {wormhole.mass} Lifetime {wormhole.lifetime}\n Updated:<t:{wormhole.updated_at.timestamp():.0f}:R>", inline=False
            )

        return await ctx.respond(embed=embed)

    @drifter_commands.command(name="system_list", description="List wormholes in a system", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def list_system_wormholes(
        self, ctx,
        system=Option(str, "Solar System", autocomplete=search_solar_systems),
    ):
        """
        list_system_wormholes _summary_

        :param ctx: _description_
        :type ctx: _type_
        :param system: _description_, defaults to Option(str, "Solar System", autocomplete=search_solar_systems)
        :type system: _type_, optional
        :return: _description_
        :rtype: _type_
        """
        evesolarsystem = EveSolarSystem.objects.get(name=system)

        embed = Embed(title=f"AA-Drifters: {system}")

        for wormhole in Wormhole.objects.filter(system=evesolarsystem, archived=False):
            embed.add_field(
                name=wormhole.complex, value=f"{wormhole.mass}, {wormhole.formatted_lifetime}\n Updated:<t:{wormhole.updated_at.timestamp():.0f}:R>", inline=False
            )

        return await ctx.respond(embed=embed)

    @drifter_commands.command(name="system_jumps_list", description="List wormholes of wormoles x jumps from system", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def list_system_jumps_wormholes(
        self, ctx,
        region=Option(str, "Region", autocomplete=search_regions),
        jumps=Option(int, required=False)
    ):

        return await ctx.respond("Not Yet Implemented")

    @drifter_commands.command(name="region_list", description="List wormholes in a system", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def list_region_wormholes(
        self, ctx,
        region=Option(str, "Region", autocomplete=search_regions),
    ):
        """
        list_region_wormholes _summary_

        :param ctx: _description_
        :type ctx: _type_
        :param system: _description_, defaults to Option(str, "Region", autocomplete=search_regions)
        :type system: _type_, optional
        :return: _description_
        :rtype: _type_
        """
        everegion = EveRegion.objects.get(name=region)

        embed = Embed(title=f"AA-Drifters: {region}")

        for wormhole in Wormhole.objects.filter(region=everegion, archived=False):
            embed.add_field(
                name=wormhole.complex, value=f"{wormhole.mass}, {wormhole.formatted_lifetime}, Updated:<t:{wormhole.updated_at.timestamp():.0f}:R>", inline=False
            )

        return await ctx.respond(embed=embed)

    @drifter_commands.command(name="region_status", description="Known Jove Observatories in a region and their Status", guild_ids=[int(settings.DISCORD_GUILD_ID)])
    async def status_region(
        self, ctx,
        region=Option(str, "Region", autocomplete=search_regions),
    ):
        """
        list_region_wormholes _summary_

        :param ctx: _description_
        :type ctx: _type_
        :param system: _description_, defaults to Option(str, "Region", autocomplete=search_regions)
        :type system: _type_, optional
        :return: _description_
        :rtype: _type_
        """
        everegion = EveRegion.objects.get(name=region)
        embed = Embed(title=f"AA-Drifters: Status {region}")
        content = ""

        for system in EveSolarSystem.objects.filter(eve_constellation__eve_region=everegion, name__in=JOVE_OBSERVATORIES):
            if Wormhole.objects.filter(system=system, archived=False):
                for wormhole in Wormhole.objects.filter(system=system, archived=False):
                    content += f"{system.name} - {wormhole.complex}, {wormhole.mass}, {wormhole.formatted_lifetime}, Updated:<t:{wormhole.updated_at.timestamp():.0f}:R>) \n"
            elif Clear.objects.filter(system=system):
                for clear in Clear.objects.filter(system=system):
                    content += f"{system.name} - Clear (<t:{clear.updated_at.timestamp():.0f}:R>)\n"
            else:
                content += f"{system.name} - UNKNOWN\n"
        embed.description = content

        return await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Drifters(bot))
