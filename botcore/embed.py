from datetime import datetime

import discord
from config import config
from discord.ext import commands

from botcore.utils import (cleanxml, format_time_seconds)


async def BasicEmbed(
        ctx: commands.Context = None,
        title: str = None,
        description: str = None,
        timestamp: datetime = None,
        color: int = config.EMBED_COLOR,
        **kwargs
    ):
    """
        kwargs:
            delete_after
            delete_after_footer
            skip_send
            footer_text
            footer_url
            view
            author
            author_url
            author_icon_url
            image
            thumbnail
    """
    delete_after = kwargs.get("delete_after", None)
    delete_after_footer = kwargs.get("delete_after_footer", None)
    skip_send = kwargs.get("skip_send", None)
    footer_text = kwargs.get("footer_text", None)
    footer_url = kwargs.get("footer_url", None)
    view = kwargs.get("view", None)
    author = kwargs.get("author", None)
    author_url = kwargs.get("author_url", None)
    author_icon_url = kwargs.get("author_icon_url", None)
    image = kwargs.get("image", None)
    thumbnail = kwargs.get("thumbnail", None)

    embed = discord.Embed(
        title=cleanxml(title),
        description=description,
        timestamp=timestamp,
        color=color
    )
    if author or author_url:
        embed.set_author(name=author, url=author_url, icon_url=author_icon_url)

    # footer_text will override this
    if delete_after_footer:
        footer_text = config.UI_EMBED_TIMEOUT_DESC.format(format_time_seconds((delete_after)))

    if footer_text or footer_url:
        embed.set_footer(text=footer_text, icon_url=footer_url)

    if image:
        embed.set_image(url=image)

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    if skip_send: return embed
    if view:
        view.message=await ctx.send(embed=embed,delete_after=delete_after,view=view)
        return view.message
    return await ctx.send(embed=embed,delete_after=delete_after,view=view)