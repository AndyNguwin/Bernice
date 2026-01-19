# main.py
import sys
from pathlib import Path
src_path = Path(__file__).parent.parent  # Goes from src/bot/ to src/
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


from datetime import datetime
import os, random, logging
from pathlib import Path
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from dotenv import load_dotenv
from collections import Counter, defaultdict
from app.models.card import Card
from app.models.idol import Idol
from infra.db.postgres_repository import PostgresRepository

# ===================== Setup =====================
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit("No DISCORD_TOKEN in .env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s"
)
file_handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
file_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(file_handler)

intents = discord.Intents.default()
intents.message_content = True  # keep on for prefix commands
bot = commands.Bot(command_prefix=["c","C"] , intents=intents)

# ===================== Config / Data =====================
STATE_REPO = PostgresRepository()

async def draw_one() -> Idol:
    return await STATE_REPO.get_random_idol()

def make_embed(user, idol: Idol, card: Card, artist: str, card_set: str):
    e = discord.Embed(
        title=f"{idol.idol_name} — {artist} [{card_set}]",
        description=f"Rolled by {user.mention}"
    )
    # print(idol.image_url)
    e.set_footer(text=f"Code {card.card_id} • Print {card.print_number}")
    # image_path = Path(idol.image_url)  # assuming idol.image_url now contains "img/hanni.png"
    # if image_path.exists():
    #     file = discord.File(image_path, filename=image_path.name)
    #     e.set_image(url=f"attachment://{image_path.name}")
    #     return e, file  # Return both embed and file
    # else:
    #     return e, None  # No image file found

    e.set_image(url=idol.image_url)
    return e

# ===================== Bot Events =====================
@bot.event
async def on_ready():
    await STATE_REPO._make_connection_pool()
    print(f"✅ Logged in as {bot.user} (id: {bot.user.id})")
    await bot.change_presence(activity=discord.Game(name="cdrop/cd • cinv/ci"))


# ===================== Commands =====================
# Drop (single) with alias "cd"
@commands.cooldown(1, 3, BucketType.user)
@bot.command(name="drop", aliases=["d","D"], help="Roll the gacha")
async def drop(ctx: commands.Context):
    user = f"{ctx.author.name} (id={ctx.author.id})"
    print(f"[COMMAND] {ctx.command} by {user}")
    idol = await draw_one()
    code = await STATE_REPO.next_code()
    print_number = await STATE_REPO.allocate_print(idol.idol_id)

    card = Card(
        card_id = code,
        idol_id = idol.idol_id,
        print_number = print_number,
        owner_id = ctx.author.id,
        acquired_date = datetime.now()
    )

    await STATE_REPO.add_card_to_inventory(card)
    artist = await STATE_REPO.get_artist_by_id(idol.artist_id)
    card_set = await STATE_REPO.get_card_set_by_id(idol.card_set_id)
    
    await ctx.reply(embed=make_embed(ctx.author, idol, card, artist, card_set), mention_author=True)
    # embed, file = make_embed(ctx.author, idol, card, artist, card_set)
    # if file:
    #     await ctx.reply(embed=embed, file=file, mention_author=True)
    # else:
    #     await ctx.reply(embed=embed, mention_author=True)


# @drop.error
# async def drop_error(ctx, error, pulls=None):
#     if isinstance(error, commands.CommandOnCooldown):
#         await ctx.reply(f"⏳ Cooldown: try again in {error.retry_after:.1f}s.", mention_author=True)
#     else:
#         raise error

#     # summary embed + show last card image
#     counts = Counter(c["rarity"] for (c, _, _, _) in pulls)
#     lines = [f"**{r}**: {counts.get(r, 0)}" for r in ("SSR","SR","R","N")]
#     last_card, last_code, last_ed, last_ser = pulls[-1]
#     e = discord.Embed(
#         title=f"{ctx.author.name}'s 10x Pull",
#         description="\n".join(lines),
#         color=0x5865F2
#     )
#     sample = ", ".join([f"{c['name']}[{c['rarity']}]#{code}" for (c, code, _, _) in pulls[:10]])
#     if sample: e.add_field(name="10 Card Drop", value=sample, inline=False)
#     e.set_image(url=last_card["image"])
#     e.set_footer(text="Use cinv / ci to view your full inventory.")
#     await ctx.reply(embed=e, mention_author=True)

# ===================== Run =====================
bot.run(TOKEN, log_handler=file_handler, log_level=logging.INFO)
