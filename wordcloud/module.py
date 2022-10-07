from typing import List, Optional

import discord
from discord import app_commands
from discord.ext import commands

from numpy import array, ndarray, reshape
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

import pie.database.config
from pie import check, exceptions, i18n, logger, utils

bot_log = logger.Bot.logger()
guild_log = logger.Guild.logger()

class WordCloudGenerator(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        # set parameters for default wordcloud
    
    # get the text of the last 100 messages in the channel
    async def _get_text(self, ctx: commands.Context) -> str:
        text = ""
        async for message in ctx.channel.history(limit=100):
            text += message.content + " "
        return text

    # # generate the wordcloud
    async def _generate_wordcloud(self, ctx: commands.Context, 
        text,
        width,
        height,
        prefer_horizontal,
        contour_width,
        contour_color,
        scale,
        min_font_size,
        font_step,
        max_words,
        background_color,
        max_font_size,
        mode,
        relative_scaling,
        regexp,
        collocations,
        colormap,
        normalize_plurals,
        repeat,
        include_numbers,
        min_word_length,
        collocation_threshold,
        ) -> BytesIO:

        if relative_scaling == -1:
            relative_scaling = "auto"

        # get the text of the last 100 messages in the channel
        # await bot_log.debug all the parameters
        await bot_log.debug(ctx.guild, ctx.channel, f"text: {text[:100]}")
        await bot_log.debug(ctx.guild, ctx.channel, f"width: {width}")
        await bot_log.debug(ctx.guild, ctx.channel, f"height: {height}")
        await bot_log.debug(ctx.guild, ctx.channel, f"prefer_horizontal: {prefer_horizontal}")
        await bot_log.debug(ctx.guild, ctx.channel, f"contour_width: {contour_width}")
        await bot_log.debug(ctx.guild, ctx.channel, f"contour_color: {contour_color}")
        await bot_log.debug(ctx.guild, ctx.channel, f"scale: {scale}")
        await bot_log.debug(ctx.guild, ctx.channel, f"min_font_size: {min_font_size}")
        await bot_log.debug(ctx.guild, ctx.channel, f"font_step: {font_step}")
        await bot_log.debug(ctx.guild, ctx.channel, f"max_words: {max_words}")
        await bot_log.debug(ctx.guild, ctx.channel, f"background_color: {background_color}")
        await bot_log.debug(ctx.guild, ctx.channel, f"max_font_size: {max_font_size}")
        await bot_log.debug(ctx.guild, ctx.channel, f"mode: {mode}")
        await bot_log.debug(ctx.guild, ctx.channel, f"relative_scaling: {relative_scaling}")
        await bot_log.debug(ctx.guild, ctx.channel, f"regexp: {regexp}")
        await bot_log.debug(ctx.guild, ctx.channel, f"collocations: {collocations}")
        await bot_log.debug(ctx.guild, ctx.channel, f"colormap: {colormap}")
        await bot_log.debug(ctx.guild, ctx.channel, f"normalize_plurals: {normalize_plurals}")
        await bot_log.debug(ctx.guild, ctx.channel, f"repeat: {repeat}")
        await bot_log.debug(ctx.guild, ctx.channel, f"include_numbers: {include_numbers}")
        await bot_log.debug(ctx.guild, ctx.channel, f"min_word_length: {min_word_length}")
        await bot_log.debug(ctx.guild, ctx.channel, f"collocation_threshold: {collocation_threshold}")

    
        # generate the wordcloud
        wordcloud_arr = WordCloud(
            width=width,
            height=height,
            prefer_horizontal=prefer_horizontal,
            contour_width=contour_width,
            contour_color=contour_color,
            scale=scale,
            min_font_size=min_font_size,
            font_step=font_step,
            max_words=max_words,
            background_color=background_color,
            max_font_size=max_font_size,
            mode=mode,
            relative_scaling=relative_scaling,
            regexp=regexp,
            collocations=collocations,
            colormap=colormap,
            normalize_plurals=normalize_plurals,
            repeat=repeat,
            include_numbers=include_numbers,
            min_word_length=min_word_length,
            collocation_threshold=collocation_threshold,
        ).generate(text).to_array()
        # save the image in a buffer

        wordcloud_img = Image.fromarray(wordcloud_arr)

        wordcloud_buf = BytesIO()
        wordcloud_img.save(wordcloud_buf, format='PNG')
        wordcloud_buf.seek(0)

        return wordcloud_buf

    


    help = '''
    **Aliases:** `wc`
    **Usage:** `wordcloud`
    **Description:** Generate a wordcloud from the last 100 messages in the channel.
    '''
    # group command
    @commands.guild_only()
    @check.acl2(check.ACLevel.MEMBER)
    @commands.group(name="wordcloud", aliases=["wc"], help=help, invoke_without_command=False)
    async def wordcloud_(self, ctx) -> None:
        await utils.discord.send_help(ctx)

    # # subscribe to channel    
    # @wordcloud_.command(name="subscribe", help="Subscribe wordcloud generator to this channel.")
    # async def subscribe(self, ctx: commands.Context) -> None:
    #     await guild_log.info(ctx.author, ctx.channel, "wordcloud subscribed")
    #     await ctx.send("wordcloud subscribes to this channel")

    # # unsubscribe from channel
    # @wordcloud_.command(name="unsubscribe", help="Unsubscribe wordcloud generator from this channel.")
    # async def unsubscribe(self, ctx: commands.Context) -> None:
    #     await guild_log.info(ctx.author, ctx.channel, "wordcloud unsubscribed")
    #     await ctx.send("wordcloud unsubscribes from this channel")

    # generate wordcloud
    @wordcloud_.command(name="generate", aliases=["g", "gen"], help="Manually generate a wordcloud from the last 100 messages in the channel.")
    async def generate(self, ctx: commands.Context,
        width: int = 400,
        height: int = 200,
        prefer_horizontal: float = 0.90,
        contour_width: float = 0,
        contour_color: str = "black",
        scale: float = 1,
        min_font_size: int = 4,
        font_step: int = 1,
        max_words: int = 200,
        background_color: str = "#00000000",
        max_font_size: int = None,
        mode: str = "RGBA",
        relative_scaling: float = -1,
        regexp: str = None,
        collocations: bool = True,
        colormap: str = "viridis",
        normalize_plurals: bool = True,
        repeat: bool = False,
        include_numbers: bool = False,
        min_word_length: int = 0,
        collocation_threshold: int = 30,
        ) -> None:
        
        text = await self._get_text(ctx)
        
        await guild_log.info(ctx.author, ctx.channel, "wordcloud generate")
        wordcloud_buf = await self._generate_wordcloud(ctx, text, width, height, prefer_horizontal, contour_width, contour_color, scale, min_font_size, font_step, max_words, background_color, max_font_size, mode, relative_scaling, regexp, collocations, colormap, normalize_plurals, repeat, include_numbers, min_word_length, collocation_threshold)
        
        await ctx.send(file=discord.File(wordcloud_buf, "wordcloud.png"))

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WordCloudGenerator(bot))