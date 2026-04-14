import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from keep_alive import keep_alive
from PIL import Image, ImageDraw, ImageFont
import io
keep_alive()

import asyncio
from aiogram import Bot, Dispatcher, types

# Baaki bot code...
# ✅ Logging Setup
logging.basicConfig(level=logging.INFO)

# ✅ Load Bot Token and Admin ID from environment variables
import os
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_STR = os.getenv("ADMIN_ID")

# ✅ Validate required environment variables
if not TOKEN:
    raise ValueError("❌ BOT_TOKEN environment variable is not set. Please add it to Secrets.")
if not ADMIN_ID_STR:
    raise ValueError("❌ ADMIN_ID environment variable is not set. Please add it to Secrets.")

try:
    ADMIN_ID = int(ADMIN_ID_STR)
except ValueError:
    raise ValueError(f"❌ ADMIN_ID must be a valid integer, got: {ADMIN_ID_STR}")

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ✅ Persistent Storage
import json

def load_verified_users():
    try:
        with open('verified_users.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_verified_users(users):
    with open('verified_users.json', 'w') as f:
        json.dump(list(users), f)

verified_users = load_verified_users()
current_code = None
user_mines_selection = {}  # Track selected mines count per user
pending_video_users = {}  # Track users waiting for registration video
all_users = set()  # Track all users who have interacted with the bot

# ✅ 60 Daily Marketing Posts
DAILY_POSTS = [
    "Bro, ready signal for you🔥\n\nSTART NOW👉 /start",
    "System upgraded successfully!💰\n\nStart making money with my BOTS for FREE!\n\nClick here👉🏻 /start",
    "YOU HAS LIMITED ACTIVATES🔐\nSTART NOW AND GET 200$ IN HOUR💵🔥\n\nClick 👉 /start",
    "Your 🆔 gives big wins today🔥\n/start NOW",
    "SIGNALS ARE READY🚀✅\nClick: /start 👈",
    "NEW SIGNALS ARE READY ✅\nINVEST AND INCREASE YOUR CAPITAL 📈\nclick here ➡️ /start",
    "GET RICH FAST!🤑\n\nClick👉 /start",
    "👋 This week players have earned more than $12,800 with the help of our bot\n\nStart now 👉 /start",
    "Make from 500$ a day with this bot🤯\n\nJust click here: /start",
    "IT'S TIME TO MAKE MONEY, BRO🔥💸👇\n\nClick ➡️ /start",
    "Need money?💰\nClick👉 /start",
    "MAKE BIG WINS - ALL IN YOUR HANDS 🔥\n\nCLICK 👉 /start",
    "Start earning 500$ a day👍\n\nClick here👉 /start 👈",
    "Bro, ready signal for you☺️\n\nSTART NOW👉 /start",
    "GET YOUR SIGNAL🤑\n\n\nClick👉 /start",
    "🤖 BOT UPDATED 🤖\n\n✅ Small bugs have been fixed\n\n➡️ To get an accurate signal, register and make a deposit.\n\n/start",
    "⭐️All signals- easy⭐️\n\n❗️I want to remind you, in order to get an accurate signal, you need to fulfill the conditions of the bot.\n\n1 - create a new account\n2 - make a deposit of 10$ or more\n\n➡️ /start",
    "✅GET SIGNAL✅\nClick /start",
    "START BOT NOW AND GET MONEY💰🔥\n\n/start",
    "✅NEW SIGNAL FOR 690$✅\n/start",
    "BOT UPDATED ✅\n\nCHANCES OF WINNING INCREASED 🤑\n\nACTIVATE RIGHT NOW\nCLICK 👉 /start",
    "🚀 The signal has already come\n\n🔥 Don't miss your chance to get your money\n\n➡️ /start",
    "BOT UPDATED❗️\n\nWE REMOVE BAGS AND RESTRART AI-SYSTEM 🤖\n\n✅ ACTIVATE YOUR HACK AND START EARN MORE THAN 500$ A DAY👍\n\nBOT➡️ /start",
    "⏱️ Activations are limited every day.\n\nOnce today's spots are gone, you'll wait till tomorrow.\n\nDon't risk missing out 👉 /start",
    "🕒 15 minutes a day. That's all you need.\n\n💯 We use an ultra-fast strategy with laser-accurate signals.\n\nWant to try it now?\n\nActivate bot 👉 /start",
    "🤑 Do you want to earn from 500$ every day?\n\n🔥 You have this opportunity, activate the bot, and join the biggest earning team.\n\n🚀 Stop waiting, places are limited\n\n/start",
    "You haven't activated your bot yet 😶\nHey, we noticed you haven't started using your bot. It's waiting — loaded with live signals, ready to work. Every hour you wait, another user takes your spot in the profit stream.\nDon't just watch.\nJoin the movement /start",
    "🚨 Still watching others make money?\n\nPeople earn between $150 and $350 a day just by following signals.\n\nYou don't need to learn how to analyze yourself — just follow the system and take action.\n\nYou'll see results from day one.\n\n👉 /start",
    "What if I told you… your phone could earn for you? 📱\n\nSounds crazy? That's what most people thought before trying it. The bot predicts safe signals across games like Mines and Aviator. You follow. It calculates. You win. That's it. No stress, no guessing. Just pure data working in your favor.\n\nActivate now 🎯 /start",
    "Don't let this message be another missed chance 💭\n\nYou've seen how it works. You know what it can do. Now the decision is yours — stay where you are or step forward. Every big change begins with one small /start",
    "It's not magic — it's math. The bot turns probability into profit with machine-level precision.\nEvery move calculated. Every win predicted.\nStop fighting the system — start using it.\n\n/start the Algorithm → Get Paid ⚡️",
    "🎉 CONGRATULATIONS.\n\nIf you see this message, it means you have received VIP status in our bot for 24 hours.\n\nTo activate the bot, click ➡️ /start",
    "If you're seeing this message, this is your chance.\n\nHurry up and get access to the free AI bot — you have 20 days left.\n\nDM me the word \"BOT\" and get the instructions — @Jimmy_716\n\n\n👉🏻 /start",
    "Want to get a free AI Mines bot and start earning from $2000 a month?\n\nMessage me \"BOT\" in DM and I'll send you the instructions — @Jimmy_716\n\n\n👉🏻 /start",
    "The bot has been updated. You can get new signals\n\nClick 👉 /start",
    "💎 Bot updated:\n\n• Design\n• Accuracy\n• Speed\n\nTap ➡️ /start",
    "Your last chance.\n\nClick ➡️ /start",
    "To work with the bot:\n\nTelephone 📲\nGood internet 🛜\n\nYou can earn $50-100 every day! /start",
    "System upgraded successfully!💰\n\nStart making money with my BOT for FREE!\n\nClick here👉🏻 /start",
    "YOU HAS LIMITED ACTIVATES🔐\nSTART NOW AND GET 200$ IN HOUR💵🔥\n\nClick 👉 /start",
    "NEW CHANCE TO MAKE 100,000₹ A DAY😌👇\n\n/start",
    "Cashout 2000-3000$ daily today!\n\nPromocode : 74MINES 🎁\n\nClick👉🏻/start",
    "Hey Bro\n\nStill sleeping in your soft bed and not making enough money?💰\n\nGet one of my bots FOR FREE and start making 1000$ DAILY!\n\nClick /start or write /start",
    "+165,311₹ on your balance💳\n\nGET NOW👉 /start",
    "Our Bot's are upgraded!\n\nClaim BOT for FREE NOW and Cashout BIG!\n\nClick 👉🏻 /start",
    "Use my hack bot\nto GET MONEY💰\nClick: /start",
    "✅WIN 1021$✅\n\nCASHOUT ➡️ /start",
    "Get it with signal bot for FREE⬇️\n\nClick👉 /start",
    "✅NEW SIGNAL FOR 1510$✅\n\n🎰 GAME MINES 🎰\n\n➡️ /start",
    "Ready to start earn from 3000$ daily?🤑\n\nIf Yes - Click👉🏻 /start and CASHOUT!",
    "Make from 500$ a day with this bot🤯\n\nJust click here: /start",
    "Today I win 850$🤖✅\nClick👇\n/start",
    "BOT UPDATED ✅\n\nClick 👉 /start Bot activation will take 5 minutes\n\n1. Register\n2. Top up your balance with $5,10,15,20\n3. Start making money on signals",
    "💸 Loss recovery 💸\n\nThat's only possible with my bot\n\n➡️ Click /start to get signal",
    "🤑 EARN ₹10,000 RIGHT NOW! 💸\n\n👉/start\n\nI'll help you get your FIRST PROFIT today!",
    "Do you want win FREE BONUS CODE❔\nGive it to most active players every week🎁\n\n🔥START NOW click-> /start",
    "⚡️Mark YOU WON 500$!⚡️\n\n🎁Claim PRIZE👉🏻/start",
    "🤑 Do you want to earn from 500$ every day?\n\n🔥 You have this opportunity, activate the bot, and join the biggest earning team.\n\n🚀 Stop waiting, places are limited\n\n/start",
    "Bot Upgraded 👨‍💻\n\nRegister an account and get signals /start",
    "Hello Hackers!💣\n\nReady to make couple thousands $ today with my bots?\n\nClick /start and let's start destroying!💸"
]

# ✅ Load/Save Daily Post State
def load_post_state():
    try:
        with open('daily_post_state.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"used_posts": [], "last_sent_date": None}

def save_post_state(state):
    with open('daily_post_state.json', 'w') as f:
        json.dump(state, f)

# ✅ Load/Save User Language Preferences
def load_user_language():
    try:
        with open('user_language.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_language(lang_dict):
    with open('user_language.json', 'w') as f:
        json.dump(lang_dict, f)

# ✅ Load/Save All Users
def load_all_users():
    try:
        with open('all_users.json', 'r') as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()

def save_all_users(users):
    with open('all_users.json', 'w') as f:
        json.dump(list(users), f)

all_users = load_all_users()
user_language = load_user_language()  # Load user language preferences

# ✅ Background Task for Code Rotation
async def send_activation_code():
    global current_code
    while True:
        current_code = str(random.randint(10**7, 10**8 - 1))  # 8-digit code
        
        # ✅ Code is ONLY sent to admin - NO file storage, NO user access
        try:
            await bot.send_message(ADMIN_ID, f"🔐 New 8-digit code:\n<code>{current_code}</code>")
        except Exception as e:
            logging.error(f"Failed to send code to admin: {e}")
        await asyncio.sleep(120)  # 2 minutes

# ✅ Background Task for Sending Registration Video
async def send_registration_video_delayed(user_id):
    """Send registration video after 8-12 minutes"""
    global pending_video_users
    
    # Wait 8-12 minutes (480-720 seconds)
    wait_time = random.uniform(480, 720)
    await asyncio.sleep(wait_time)
    
    # Check if user is still pending (not verified yet)
    if user_id in pending_video_users:
        try:
            video = FSInputFile("registration_video.mp4")
            video_text = (
                "⬇️ First, register an account ⬇️\n"
                "⬇️ Make at least a 5-10$ Deposit 💸 (500₹ | 5€ | 200₺) ⬇️"
            )
            
            # Create button for registration
            register_button = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Register here 🕹️", url="https://1wssrq.life/?open=register&p=lx6n&sub1=8052181437&p=0kik")]
                ]
            )
            
            await bot.send_video(
                user_id,
                video=video,
                caption=video_text,
                reply_markup=register_button
            )
            logging.info(f"Registration video sent to user {user_id}")
        except Exception as e:
            logging.error(f"Failed to send registration video to user {user_id}: {e}")
        finally:
            # Remove user from pending list
            if user_id in pending_video_users:
                del pending_video_users[user_id]

# ✅ Background Task for Daily Posts
async def send_daily_posts():
    """Send one random post from 60 posts to all users every day"""
    from datetime import datetime, timedelta
    
    while True:
        try:
            # Load current state
            post_state = load_post_state()
            current_date = datetime.now().strftime("%Y-%m-%d")
            
            # Check if we already sent a post today
            if post_state["last_sent_date"] == current_date:
                # Already sent today, wait until tomorrow
                now = datetime.now()
                tomorrow = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                wait_seconds = (tomorrow - now).total_seconds()
                logging.info(f"Daily post already sent today. Waiting {wait_seconds/3600:.1f} hours until tomorrow.")
                await asyncio.sleep(wait_seconds + 60)  # Add 60 seconds buffer
                continue
            
            # Get available posts
            used_posts = post_state.get("used_posts", [])
            
            # If all posts have been used, reset the cycle
            if len(used_posts) >= len(DAILY_POSTS):
                used_posts = []
                logging.info("All 60 posts have been sent. Restarting cycle from beginning.")
            
            # Get unused post indices
            available_indices = [i for i in range(len(DAILY_POSTS)) if i not in used_posts]
            
            # Select random post from available ones
            selected_index = random.choice(available_indices)
            selected_post = DAILY_POSTS[selected_index]
            
            # Mark this post as used
            used_posts.append(selected_index)
            post_state["used_posts"] = used_posts
            post_state["last_sent_date"] = current_date
            save_post_state(post_state)
            
            # Load all users
            global all_users
            all_users = load_all_users()
            
            if not all_users:
                logging.info("No users to send daily post to yet.")
            else:
                # Send the post to all users
                success_count = 0
                fail_count = 0
                
                for user_id in all_users:
                    try:
                        await bot.send_message(user_id, selected_post)
                        success_count += 1
                        # Small delay between messages to avoid flooding
                        await asyncio.sleep(0.05)
                    except Exception as e:
                        fail_count += 1
                        logging.error(f"Failed to send daily post to user {user_id}: {e}")
                
                logging.info(f"Daily post #{selected_index + 1} sent to {success_count} users (failed: {fail_count}). Posts used: {len(used_posts)}/60")
                
                # Notify admin
                try:
                    await bot.send_message(
                        ADMIN_ID,
                        f"📊 Daily Post Report:\n\n"
                        f"✅ Post #{selected_index + 1} sent\n"
                        f"👥 Sent to: {success_count} users\n"
                        f"❌ Failed: {fail_count} users\n"
                        f"📈 Progress: {len(used_posts)}/60 posts used"
                    )
                except:
                    pass
            
            # Wait for random time (12-20 hours) before next post
            wait_hours = random.uniform(12, 20)
            wait_seconds = wait_hours * 3600
            logging.info(f"Next daily post will be sent in {wait_hours:.1f} hours")
            await asyncio.sleep(wait_seconds)
            
        except Exception as e:
            logging.error(f"Error in daily post scheduler: {e}")
            # Wait 1 hour before retrying on error
            await asyncio.sleep(3600)

# ✅ Language Selection Menu
def get_language_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇷🇺 Pусский", callback_data="lang_ru"),
             InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
        ]
    )

# ✅ Welcome Menu
def get_welcome_menu(lang='en'):
    if lang == 'ru':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="ИНСТРУКЦИИ 📋", callback_data="show_instructions"),
                 InlineKeyboardButton(text="❓ FAQ", callback_data="show_faq")],
                [InlineKeyboardButton(text="КАНАЛ 📢", url="https://t.me/+_62og6oPxs9jNjg0")],
                [InlineKeyboardButton(text="🌐 ИЗМЕНИТЬ ЯЗЫК", callback_data="change_language")],
                [InlineKeyboardButton(text="🤑ПОЛУЧИТЬ СИГНАЛ🤑", callback_data="show_start")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="INSTRUCTIONS 📋", callback_data="show_instructions"),
                 InlineKeyboardButton(text="❓ FAQ", callback_data="show_faq")],
                [InlineKeyboardButton(text="CHANNEL 📢", url="https://t.me/+_62og6oPxs9jNjg0")],
                [InlineKeyboardButton(text="🌐 CHANGE LANGUAGE", callback_data="change_language")],
                [InlineKeyboardButton(text="🤑GET SIGNAL🤑", callback_data="show_start")]
            ]
        )

# ✅ Instructions Menu
def get_instructions_menu(lang='en'):
    if lang == 'ru':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Регистрация 🕹️", url="https://1wssrq.life/?open=register&p=lx6n&sub1=8052181437&p=0kik")],
                [InlineKeyboardButton(text="📩 ПОЛУЧИТЬ КЛЮЧ 📩", url="https://t.me/Jimmy_716?text=Привет,%20Можете%20выслать%20мне%20ключ%20активации")],
                [InlineKeyboardButton(text="Главная 📱", callback_data="back_to_main")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Register 🕹️", url="https://1wgfor.com/?open=register&p=lx6n&sub1=8052181437&p=0kik")],
                [InlineKeyboardButton(text="📩 GET THE KEY 📩", url="https://t.me/Jimmy_716?text=Hi,%20Can%20you%20please%20send%20me%20activation%20key")],
                [InlineKeyboardButton(text="Main 📱", callback_data="back_to_main")]
            ]
        )

# ✅ FAQ Menu
def get_faq_menu(lang='en'):
    if lang == 'ru':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад в ГЛАВНОЕ МЕНЮ", callback_data="back_to_main")],
                [InlineKeyboardButton(text="🆘 ПОДДЕРЖКА", url="https://t.me/Jimmy_716")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Back to MAIN MENU", callback_data="back_to_main")],
                [InlineKeyboardButton(text="🆘 SUPPORT", url="https://t.me/Jimmy_716")]
            ]
        )

# ✅ Game Menu
def get_game_menu(lang='en'):
    if lang == 'ru':
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Mines ⭐", callback_data="game_mines"),
                 InlineKeyboardButton(text="Mines 2 💎", callback_data="game_mines2")],
                [InlineKeyboardButton(text="Aviator ✈️", callback_data="game_aviator"),
                 InlineKeyboardButton(text="Lucky Jet 🚀", callback_data="game_luckyjet")],
                [InlineKeyboardButton(text="Crash 🛩️", callback_data="game_crash"),
                 InlineKeyboardButton(text="Penalty ⚽", callback_data="game_penalty")],
                [InlineKeyboardButton(text="Brawl Pirates 🏴‍☠️ (Недоступно)", callback_data="game_unavailable")]
            ]
        )
    else:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Mines ⭐", callback_data="game_mines"),
                 InlineKeyboardButton(text="Mines 2 💎", callback_data="game_mines2")],
                [InlineKeyboardButton(text="Aviator ✈️", callback_data="game_aviator"),
                 InlineKeyboardButton(text="Lucky Jet 🚀", callback_data="game_luckyjet")],
                [InlineKeyboardButton(text="Crash 🛩️", callback_data="game_crash"),
                 InlineKeyboardButton(text="Penalty ⚽", callback_data="game_penalty")],
                [InlineKeyboardButton(text="Brawl Pirates 🏴‍☠️ (Unavailable Now)", callback_data="game_unavailable")]
            ]
        )

def get_mines_selection_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1", callback_data="mines_count_1")],
            [InlineKeyboardButton(text="3", callback_data="mines_count_3")],
            [InlineKeyboardButton(text="5", callback_data="mines_count_5")],
            [InlineKeyboardButton(text="7", callback_data="mines_count_7")]
        ]
    )

def get_mines2_selection_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="2", callback_data="mines2_count_2")],
            [InlineKeyboardButton(text="3", callback_data="mines2_count_3")],
            [InlineKeyboardButton(text="5", callback_data="mines2_count_5")],
            [InlineKeyboardButton(text="7", callback_data="mines2_count_7")]
        ]
    )

def get_game_buttons(game):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Get Signal", callback_data=f"get_signal_{game}")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
        ]
    )

def get_mines_signal_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Get Signal", callback_data="get_mines_signal")],
            [InlineKeyboardButton(text="Select Mines 💣", callback_data="select_mines")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
        ]
    )

def get_mines2_signal_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Get Signal", callback_data="get_mines2_signal")],
            [InlineKeyboardButton(text="Select Mines 💣", callback_data="select_mines2")],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back")]
        ]
    )

# ✅ Code Verification Handler
@dp.message(lambda m: m.text and m.text.isdigit() and len(m.text) == 8)
async def verify_code(message: types.Message):
    global current_code, verified_users
    # Reload verified users to check latest status
    verified_users = load_verified_users()
    
    # Get user language
    user_id_str = str(message.from_user.id)
    lang = user_language.get(user_id_str, 'en')
    
    if message.from_user.id in verified_users:
        # User is already verified, show game menu directly
        photo = FSInputFile("casino_menu.png")
        caption = "✅ You're already verified! Select a game to get signals." if lang == 'en' else "✅ Вы уже верифицированы! Выберите игру для получения сигналов."
        await message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=get_game_menu(lang)
        )
        return
    
    if message.text == current_code:
        verified_users.add(message.from_user.id)
        save_verified_users(verified_users)
        photo = FSInputFile("casino_menu.png")
        caption = "✅ Code verified! Select a game to get signals." if lang == 'en' else "✅ Код верифицирован! Выберите игру для получения сигналов."
        await message.reply_photo(
            photo=photo,
            caption=caption,
            reply_markup=get_game_menu(lang)
        )
    else:
        error_msg = "❌ Invalid or expired code. Please contact @Jimmy_716" if lang == 'en' else "❌ Неверный или истекший код. Пожалуйста, свяжитесь с @Jimmy_716"
        await message.reply(error_msg)

# ✅ Check Verification Command
@dp.message(lambda message: message.text == "/check")
async def check_verification(message: types.Message):
    user_id = message.from_user.id
    if user_id == ADMIN_ID:
        verified_count = len(verified_users)
        verified_list = "\n".join([f"• User ID: {uid}" for uid in verified_users])
        await message.reply(f"📊 Verified Users ({verified_count}):\n\n{verified_list}")
    else:
        status = "✅ Verified" if user_id in verified_users else "❌ Not Verified"
        await message.reply(f"Your status: {status}\nYour ID: {user_id}")

# ✅ Language Selection Handlers
@dp.callback_query(lambda c: c.data in ["lang_en", "lang_ru"])
async def select_language(callback_query: types.CallbackQuery):
    global user_language
    await callback_query.answer()
    
    user_id_str = str(callback_query.from_user.id)
    lang = 'ru' if callback_query.data == "lang_ru" else 'en'
    user_language[user_id_str] = lang
    save_user_language(user_language)
    
    welcome_text = "<b>💎 MAIN MENU 💎</b>" if lang == 'en' else "<b>💎 ГЛАВНОЕ МЕНЮ 💎</b>"
    
    try:
        await bot.send_photo(
            callback_query.from_user.id,
            photo="https://i.postimg.cc/J0T8sGPv/photo-5845672359736577114-y.jpg",
            caption=welcome_text,
            reply_markup=get_welcome_menu(lang)
        )
    except Exception as e:
        logging.error(f"Error sending welcome image: {e}")
        await bot.send_message(
            callback_query.from_user.id,
            welcome_text,
            reply_markup=get_welcome_menu(lang)
        )

# ✅ Change Language Handler
@dp.callback_query(lambda c: c.data == "change_language")
async def change_language(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    language_text = "<b>Welcome to the bot👋🏼</b>\n\nChoose a language / Выберите язык:"
    
    try:
        photo = FSInputFile("language_selection.png")
        await bot.send_photo(
            callback_query.from_user.id,
            photo=photo,
            caption=language_text,
            reply_markup=get_language_menu()
        )
    except Exception as e:
        logging.error(f"Error sending language selection image: {e}")
        await bot.send_message(
            callback_query.from_user.id,
            language_text,
            reply_markup=get_language_menu()
        )

# ✅ Start Command
@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    # Track all users who interact with the bot
    global all_users, user_language
    user_id = message.from_user.id
    if user_id not in all_users:
        all_users.add(user_id)
        save_all_users(all_users)
        logging.info(f"New user tracked: {user_id}. Total users: {len(all_users)}")
    
    # Check if user has selected language
    user_id_str = str(user_id)
    if user_id_str not in user_language:
        # Show language selection
        language_text = "<b>Welcome to the bot👋🏼</b>\n\nChoose a language / Выберите язык:"
        
        try:
            photo = FSInputFile("language_selection.png")
            await message.answer_photo(
                photo=photo,
                caption=language_text,
                reply_markup=get_language_menu()
            )
        except Exception as e:
            logging.error(f"Error sending language selection image: {e}")
            await message.answer(
                language_text,
                reply_markup=get_language_menu()
            )
    else:
        # Language already selected, show main menu
        lang = user_language[user_id_str]
        welcome_text = "<b>💎 MAIN MENU 💎</b>" if lang == 'en' else "<b>💎 ГЛАВНОЕ МЕНЮ 💎</b>"
        
        try:
            await message.answer_photo(
                photo="https://i.postimg.cc/J0T8sGPv/photo-5845672359736577114-y.jpg",
                caption=welcome_text,
                reply_markup=get_welcome_menu(lang)
            )
        except Exception as e:
            logging.error(f"Error sending welcome image: {e}")
            await message.answer(
                welcome_text,
                reply_markup=get_welcome_menu(lang)
            )

# ✅ Instructions Button Handler
@dp.callback_query(lambda c: c.data == "show_instructions")
async def show_instructions(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    user_id_str = str(callback_query.from_user.id)
    lang = user_language.get(user_id_str, 'en')
    
    if lang == 'ru':
        instructions_text = (
            "<b>Правила просты:</b>\n\n"
            "1. Зарегистрируйтесь здесь 👉 <a href='https://1wssrq.life/?open=register&p=lx6n&sub1=8052181437&p=0kik'>1WIN</a>\n"
            "2. Введите промокод: <code>74MINES</code>  (ПОЛУЧИТЕ БОНУС 500% 🎁)\n"
            "3. Сделайте депозит минимум $5–$10 💸 ( 500₹|5€| 200₺ )\n"
            "4. Напишите @Jimmy_716 чтобы получить доступ ✏"
        )
    else:
        instructions_text = (
            "<b>Rules are simple:</b>\n\n"
            "1. Register here 👉 <a href='https://1wssrq.life/?open=register&p=lx6n&sub1=8052181437&p=0kik'>1WIN</a>\n"
            "2. Enter promocode: <code>74MINES</code>  (GET 500% BONUS 🎁)\n"
            "3. Make at least a $5–$10 deposit 💸 ( 500₹|5€| 200₺ )\n"
            "4. Write @Jimmy_716 to get access ✏"
        )
    
    try:
        photo = FSInputFile("instructions_registration.jpg")
        await bot.send_photo(
            callback_query.from_user.id,
            photo=photo,
            caption=instructions_text,
            reply_markup=get_instructions_menu(lang)
        )
    except Exception as e:
        logging.error(f"Error sending instructions image: {e}")
        await bot.send_message(
            callback_query.from_user.id,
            instructions_text,
            reply_markup=get_instructions_menu(lang)
        )

# ✅ FAQ Button Handler
@dp.callback_query(lambda c: c.data == "show_faq")
async def show_faq(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    user_id_str = str(callback_query.from_user.id)
    lang = user_language.get(user_id_str, 'en')
    
    if lang == 'ru':
        faq_text = (
            "📢 Искусственный интеллект бота построен на мощной нейросети кластера OpenAI!\n"
            "📊 Бот обучен на анализе более 🎮 30,000 игровых сессий.\n\n"
            "💹 Пользователи в настоящее время стабильно зарабатывают от 15% до 25% своего 💵 капитала каждый день!\n\n"
            "⚙️ Бот продолжает проходить тестирование и оптимизацию. Чтобы достичь максимальных результатов, следуйте этим шагам:\n\n"
            "🔹 Шаг 1: <i>Создайте аккаунт на </i><a href='https://1wssrq.life/?open=register&p=lx6n&sub1=8052181437&p=0kik'>1WIN</a>\n\n"
            "<blockquote>💡 Если ссылка не открывается, активируйте VPN с сервером в Бразилии/Канаде. Попробуйте приложения: BebraVPN, Outline VPN, Planet VPN и другие.\n"
            "❗️ Без регистрации и промо-кода доступ к сигналам будет заблокирован!</blockquote>\n\n"
            "🔹 Шаг 2: <i>Пополните баланс вашего аккаунта.</i>\n"
            "🔹 Шаг 3: <i>Отправьте мне скриншот вашего аккаунта 1WIN и получите ключ активации.</i>\n"
            "🔹 Шаг 4: <i>Откройте раздел игр на платформе 1WIN и выберите игру.</i>\n"
            "🔹 Шаг 5: <i>Установите количество ловушек на три — это обязательное условие!</i>\n"
            "🔹 Шаг 6: <i>Получайте сигналы от бота и делайте ставки, строго следуя подсказкам.</i>\n"
            "🔹 Шаг 7: <i>В случае проигрыша удвойте (x²) вашу ставку, чтобы покрыть потерю следующим сигналом.</i>"
        )
    else:
        faq_text = (
            "📢 The bot's artificial intelligence is built on a powerful OpenAI cluster neural network!\n"
            "📊 The bot is trained on the analysis of more than 🎮 30,000 game sessions.\n\n"
            "💹 Users are currently consistently earning between 15% and 25% of their 💵 capital every day!\n\n"
            "⚙️ The bot continues to undergo testing and optimization. To achieve maximum results, follow these steps:\n\n"
            "🔹 Step 1: <i>Create an account on </i><a href='https://1wssrq.life/?open=register&p=lx6n&sub1=8052181437&p=0kik'>1WIN</a>\n\n"
            "<blockquote>💡 If the link doesn't open, activate a VPN with a server in Brazil/Canada. Try apps like: BebraVPN, Outline VPN, Planet VPN, and others.\n"
            "❗️ Without registration and a promo code, access to signals will be blocked!</blockquote>\n\n"
            "🔹 Step 2: <i>Refill your account balance.</i>\n"
            "🔹 Step 3: <i>Send me a screenshot of your 1WIN account and get the activation key.</i>\n"
            "🔹 Step 4: <i>Open the games section on the 1WIN platform and select a game.</i>\n"
            "🔹 Step 5: <i>Set the number of traps to three — this is a mandatory condition!</i>\n"
            "🔹 Step 6: <i>Receive signals from the bot and place bets strictly following the prompts.</i>\n"
            "🔹 Step 7: <i>In case of loss, double (x²) your bet to cover the loss with the next signal.</i>"
        )
    
    await bot.send_message(
        callback_query.from_user.id,
        faq_text,
        reply_markup=get_faq_menu(lang)
    )

# ✅ Back to Main Button Handler
@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback_query: types.CallbackQuery):
    await callback_query.answer()
    
    user_id_str = str(callback_query.from_user.id)
    lang = user_language.get(user_id_str, 'en')
    welcome_text = "<b>💎 MAIN MENU 💎</b>" if lang == 'en' else "<b>💎 ГЛАВНОЕ МЕНЮ 💎</b>"
    
    try:
        await bot.send_photo(
            callback_query.from_user.id,
            photo="https://i.postimg.cc/J0T8sGPv/photo-5845672359736577114-y.jpg",
            caption=welcome_text,
            reply_markup=get_welcome_menu(lang)
        )
    except Exception as e:
        logging.error(f"Error sending welcome image: {e}")
        await bot.send_message(
            callback_query.from_user.id,
            welcome_text,
            reply_markup=get_welcome_menu(lang)
        )

# ✅ START Button Handler
@dp.callback_query(lambda c: c.data == "show_start")
async def show_start(callback_query: types.CallbackQuery):
    global verified_users
    await callback_query.answer()
    
    # Reload verified users to check latest status
    verified_users = load_verified_users()
    
    # Get user language
    user_id_str = str(callback_query.from_user.id)
    lang = user_language.get(user_id_str, 'en')
    
    # Message 1
    msg1 = "Game found on the server 🔔" if lang == 'en' else "Игра найдена на сервере 🔔"
    await bot.send_message(callback_query.from_user.id, msg1)
    
    # Wait 1-2 seconds
    await asyncio.sleep(random.uniform(1, 2))
    
    # Message 2
    msg2 = "✅ Algorithm confirmed" if lang == 'en' else "✅ Алгоритм подтвержден"
    await bot.send_message(callback_query.from_user.id, msg2)
    
    # Wait 1-2 seconds
    await asyncio.sleep(random.uniform(1, 2))
    
    # Message 3 with current timestamp
    from datetime import datetime
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    await bot.send_message(
        callback_query.from_user.id,
        f"<b>𝗦𝗘𝗥𝗩𝗘𝗥 𝗦𝗘𝗘𝗗 🤖</b> {current_time} (GMT+3)"
    )
    
    # Wait 2-5 seconds before showing signals menu
    await asyncio.sleep(random.uniform(2, 5))
    
    # Show signals menu if user is verified, otherwise ask for activation code
    if callback_query.from_user.id in verified_users:
        photo = FSInputFile("casino_menu.png")
        caption = "✅ Welcome back! You're verified. Select a game to get signals!" if lang == 'en' else "✅ С возвращением! Вы верифицированы. Выберите игру для получения сигналов!"
        await bot.send_photo(
            callback_query.from_user.id,
            photo=photo,
            caption=caption,
            reply_markup=get_game_menu(lang)
        )
    else:
        msg_code = "🔐 Enter the 8-digit activation code to continue:" if lang == 'en' else "🔐 Введите 8-значный код активации для продолжения:"
        await bot.send_message(callback_query.from_user.id, msg_code)
        
        # Schedule registration video to be sent after 8-12 minutes
        user_id = callback_query.from_user.id
        if user_id not in pending_video_users:
            pending_video_users[user_id] = True
            asyncio.create_task(send_registration_video_delayed(user_id))

# ✅ Signal Generators
def generate_mines_signal(mines_count=None):
    # Use provided mines count or default random selection
    if mines_count is None:
        mines_count = random.choice([1, 3])
    
    # Set safe count based on mines count - for 3 mines, use 6 safe positions
    if mines_count == 1:
        safe_count = 12
    elif mines_count == 3:
        safe_count = 5   # Exactly 5 safe positions for 3 mines
    elif mines_count == 5:
        safe_count = 5
    elif mines_count == 7:
        safe_count = 3
    else:
        safe_count = 6   # Default to 6
    
    # Generate safe positions for the visual grid
    safe_positions = random.sample([(i, j) for i in range(5) for j in range(5)], safe_count)
    
    # Create visual signal image
    try:
        # Create a new image with dark background like the reference
        width, height = 800, 800
        image = Image.new('RGB', (width, height), color=(45, 52, 69))  # Dark blue-gray background
        draw = ImageDraw.Draw(image)
        
        # Grid settings
        grid_size = 5
        padding = 80
        cell_size = (width - 2 * padding) // grid_size
        cell_margin = 10
        
        # Draw the 5x5 grid
        for row in range(grid_size):
            for col in range(grid_size):
                # Calculate cell position
                x = padding + col * cell_size + cell_margin
                y = padding + row * cell_size + cell_margin
                cell_width = cell_size - 2 * cell_margin
                cell_height = cell_size - 2 * cell_margin
                
                if (row, col) in safe_positions:
                    # Draw star for safe positions
                    star_center_x = x + cell_width // 2
                    star_center_y = y + cell_height // 2
                    star_size = min(cell_width, cell_height) * 0.7
                    
                    # Create a star shape using polygon
                    star_points = []
                    import math
                    for i in range(10):  # 5 outer points + 5 inner points
                        angle = math.pi * i / 5
                        if i % 2 == 0:  # Outer points
                            radius = star_size / 2
                        else:  # Inner points
                            radius = star_size / 4
                        
                        point_x = star_center_x + radius * math.cos(angle - math.pi/2)
                        point_y = star_center_y + radius * math.sin(angle - math.pi/2)
                        star_points.append((point_x, point_y))
                    
                    # Draw star with gradient-like effect
                    draw.polygon(star_points, fill=(255, 165, 0), outline=(255, 140, 0))  # Orange star
                    
                    # Add inner highlight
                    inner_star_points = []
                    for i in range(10):
                        angle = math.pi * i / 5
                        if i % 2 == 0:
                            radius = star_size / 3
                        else:
                            radius = star_size / 6
                        
                        point_x = star_center_x + radius * math.cos(angle - math.pi/2)
                        point_y = star_center_y + radius * math.sin(angle - math.pi/2)
                        inner_star_points.append((point_x, point_y))
                    
                    draw.polygon(inner_star_points, fill=(255, 215, 120))  # Lighter center
                    
                else:
                    # Draw blue tile for non-safe positions
                    # Create rounded rectangle effect
                    corner_radius = 15
                    
                    # Main tile body
                    draw.rounded_rectangle(
                        [x, y, x + cell_width, y + cell_height],
                        radius=corner_radius,
                        fill=(64, 180, 200),  # Blue tile color
                        outline=(45, 140, 160),
                        width=3
                    )
                    
                    # Add highlight for 3D effect
                    draw.rounded_rectangle(
                        [x + 5, y + 5, x + cell_width - 10, y + cell_height - 15],
                        radius=corner_radius - 5,
                        fill=(80, 200, 220),  # Lighter blue for highlight
                        outline=None
                    )
        
        # Save the image
        output_path = f"mines_signal_{mines_count}.png"
        image.save(output_path)
        
        # Return both the image path and text info - no grid text preview
        signal_text = f"💣 Mines: {mines_count}\n🎯 Safe positions marked with ⭐"
        return signal_text, output_path
        
    except Exception as e:
        logging.error(f"Error generating mines image: {e}")
        # Fallback to text-based signal
        signal_text = f"💣 Mines: {mines_count}\n🎯 Safe positions marked with ⭐"
        return signal_text, None

def generate_mines2_signal(mines_count=None):
    # Use provided mines count or default
    if mines_count is None:
        mines_count = 2
    
    # Set safe count based on mines count as requested for Mines 2
    if mines_count == 2:
        safe_count = 9
    elif mines_count == 3:
        safe_count = 6
    elif mines_count == 5:
        safe_count = 3
    elif mines_count == 7:
        safe_count = 2
    else:
        safe_count = 4  # fallback
    
    safe_positions = random.sample(range(25), safe_count)
    
    # Create visual signal image
    try:
        # Create a new image with dark background
        width, height = 800, 800
        image = Image.new('RGB', (width, height), color=(45, 52, 69))  # Dark blue-gray background
        draw = ImageDraw.Draw(image)
        
        # Grid settings
        grid_size = 5
        padding = 80
        cell_size = (width - 2 * padding) // grid_size
        cell_margin = 10
        
        # Draw the 5x5 grid
        for row in range(grid_size):
            for col in range(grid_size):
                position = row * grid_size + col
                
                # Calculate cell position
                x = padding + col * cell_size + cell_margin
                y = padding + row * cell_size + cell_margin
                cell_width = cell_size - 2 * cell_margin
                cell_height = cell_size - 2 * cell_margin
                
                if position in safe_positions:
                    # Draw blue background tile for safe positions
                    corner_radius = 15
                    draw.rounded_rectangle(
                        [x, y, x + cell_width, y + cell_height],
                        radius=corner_radius,
                        fill=(30, 100, 200),  # Deep blue background
                        outline=(20, 80, 180),
                        width=3
                    )
                    
                    # Draw blue star diamond for safe positions
                    star_center_x = x + cell_width // 2
                    star_center_y = y + cell_height // 2
                    star_size = min(cell_width, cell_height) * 0.6
                    
                    # Create a 5-pointed star shape
                    star_points = []
                    import math
                    for i in range(10):  # 5 outer points + 5 inner points
                        angle = math.pi * i / 5
                        if i % 2 == 0:  # Outer points
                            radius = star_size / 2
                        else:  # Inner points
                            radius = star_size / 4
                        
                        point_x = star_center_x + radius * math.cos(angle - math.pi/2)
                        point_y = star_center_y + radius * math.sin(angle - math.pi/2)
                        star_points.append((point_x, point_y))
                    
                    # Draw blue star diamond
                    draw.polygon(star_points, fill=(120, 180, 255), outline=(80, 140, 220))  # Light blue star
                    
                    # Add inner highlight for 3D effect
                    inner_star_points = []
                    for i in range(10):
                        angle = math.pi * i / 5
                        if i % 2 == 0:
                            radius = star_size / 3
                        else:
                            radius = star_size / 6
                        
                        point_x = star_center_x + radius * math.cos(angle - math.pi/2)
                        point_y = star_center_y + radius * math.sin(angle - math.pi/2)
                        inner_star_points.append((point_x, point_y))
                    
                    draw.polygon(inner_star_points, fill=(180, 220, 255))  # Very light blue center
                    
                else:
                    # Draw gray tile with "1W" text for non-safe positions
                    corner_radius = 15
                    
                    # Main tile body - dark gray
                    draw.rounded_rectangle(
                        [x, y, x + cell_width, y + cell_height],
                        radius=corner_radius,
                        fill=(80, 90, 100),  # Dark gray tile color
                        outline=(60, 70, 80),
                        width=3
                    )
                    
                    # Add "1W" text in the center
                    try:
                        # Try to use a font, fallback to default if not available
                        font_size = int(cell_width * 0.3)
                        font = ImageFont.load_default()
                    except:
                        font = ImageFont.load_default()
                    
                    text = "1W"
                    # Get text bounding box for centering
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    
                    text_x = x + (cell_width - text_width) // 2
                    text_y = y + (cell_height - text_height) // 2
                    
                    draw.text((text_x, text_y), text, fill=(120, 130, 140), font=font)
        
        # Save the image
        output_path = f"mines2_signal_{mines_count}.png"
        image.save(output_path)
        
        # Return both the image path and text info
        signal_text = f"💣 Mines: {mines_count}\n🎯 Safe positions marked with 💎"
        return signal_text, output_path
        
    except Exception as e:
        logging.error(f"Error generating mines2 image: {e}")
        # Fallback to text-based signal
        grid = ["🟦"] * 25
        for pos in safe_positions:
            grid[pos] = "💎"
        signal_grid = f"💣 Mines: {mines_count}\n\n"
        for i in range(0, 25, 5):
            row = " ".join(grid[i:i+5])
            signal_grid += row + "\n"
        return signal_grid, None

def generate_aviator_signal():
    x1 = round(random.uniform(1.10, 1.15), 2)
    x2 = round(random.uniform(1.20, 1.33), 2)
    x3 = round(random.uniform(1.40, 2.0), 2)
    return f"YOUR NEXT BET! ✈️\n\n{x1}x ✅\n{x2}x ✅\n\n💲 CASH OUT!"

def generate_luckyjet_signal():
    x1 = round(random.uniform(1.10, 1.19), 2)
    x2 = round(random.uniform(1.20, 1.35), 2)
    x3 = round(random.uniform(1.45, 2.0), 2)
    return f"YOUR NEXT BET! 🚀\n\n{x1}x ✅\n{x2}x ✅\n\n💰 CASH OUT!"

def generate_crash_signal():
    x1 = round(random.uniform(1.12, 1.5), 2) if random.random() < 0.3 else round(random.uniform(1.5, 2.1), 2)
    x2 = round(random.uniform(1.12, 1.5), 2) if random.random() < 0.3 else round(random.uniform(1.5, 2.1), 2)
    return f"YOUR NEXT BET! 🚀\n\n{x1}x ✅\n{x2}x ✅\n\n💵 CASH OUT!"

def generate_penalty_signal():
    grid = ["🔲"] * 15
    football_positions = random.sample(range(15), 2)
    for pos in football_positions:
        grid[pos] = "⚽"
    signal_grid = "Kick 🥅\n\n"
    for i in range(0, 15, 5):
        signal_grid += " ".join(grid[i:i+5]) + "\n"
    signal_grid += "\nMultiplier: 1.83x 💲"
    return signal_grid

def generate_brawlpirates_signal():
    positions = ["💀", "💎", "💎"]
    random.shuffle(positions)
    return "Multiplier 1.44x 💲\n\n    " + "  ".join(positions)

# ✅ Game Selection Handler
@dp.callback_query(lambda c: c.data.startswith("game_"))
async def select_game(callback_query: types.CallbackQuery):
    await callback_query.answer()
    game_name = callback_query.data.split("_")[1]
    
    if game_name == "unavailable":
        await callback_query.answer("⚠️ This game is temporarily unavailable", show_alert=True)
        return
    
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    
    if game_name == "mines":
        # Show mines selection menu for Mines ⭐
        await bot.send_message(
            callback_query.from_user.id,
            "Select number of mines: 💣",
            reply_markup=get_mines_selection_menu()
        )
    elif game_name == "mines2":
        # Show mines2 selection menu for Mines 2 💎
        await bot.send_message(
            callback_query.from_user.id,
            "Select number of mines: 💣",
            reply_markup=get_mines2_selection_menu()
        )
    else:
        await bot.send_message(
            callback_query.from_user.id,
            "Click 'Get Signal' to receive predictions.",
            reply_markup=get_game_buttons(game_name)
        )

# ✅ Mines Count Selection Handler
@dp.callback_query(lambda c: c.data.startswith("mines_count_"))
async def select_mines_count(callback_query: types.CallbackQuery):
    await callback_query.answer()
    mines_count = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id
    
    # Store the selected mines count for this user
    user_mines_selection[user_id] = mines_count
    
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        callback_query.from_user.id,
        "Click 'Get Signal' to receive predictions.",
        reply_markup=get_mines_signal_buttons()
    )

# ✅ Mines 2 Count Selection Handler
@dp.callback_query(lambda c: c.data.startswith("mines2_count_"))
async def select_mines2_count(callback_query: types.CallbackQuery):
    await callback_query.answer()
    mines_count = int(callback_query.data.split("_")[2])
    user_id = callback_query.from_user.id
    
    # Store the selected mines count for this user with mines2 prefix
    user_mines_selection[f"mines2_{user_id}"] = mines_count
    
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        callback_query.from_user.id,
        "Click 'Get Signal' to receive predictions.",
        reply_markup=get_mines2_signal_buttons()
    )

# ✅ Select Mines Handler (back to mines selection)
@dp.callback_query(lambda c: c.data == "select_mines")
async def back_to_mines_selection(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        callback_query.from_user.id,
        "Select number of mines: 💣",
        reply_markup=get_mines_selection_menu()
    )

# ✅ Select Mines 2 Handler (back to mines2 selection)
@dp.callback_query(lambda c: c.data == "select_mines2")
async def back_to_mines2_selection(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        callback_query.from_user.id,
        "Select number of mines: 💣",
        reply_markup=get_mines2_selection_menu()
    )

# ✅ Get Mines Signal Handler
@dp.callback_query(lambda c: c.data == "get_mines_signal")
async def send_mines_signal(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    
    # Get the selected mines count for this user
    mines_count = user_mines_selection.get(user_id, 1)  # Default to 1 if not found
    
    checking_msg = await bot.send_message(callback_query.from_user.id, "Checking...⏳")
    await asyncio.sleep(random.randint(2, 3))
    await bot.delete_message(callback_query.from_user.id, checking_msg.message_id)

    result = generate_mines_signal(mines_count)
    if isinstance(result, tuple):
        signal, mines_image_path = result
        if mines_image_path:
            # Send the generated mines image
            photo = FSInputFile(mines_image_path)
            await bot.send_photo(
                callback_query.from_user.id, 
                photo=photo, 
                caption=signal, 
                reply_markup=get_mines_signal_buttons()
            )
            return
    else:
        signal = result
    
    await bot.send_message(callback_query.from_user.id, signal, reply_markup=get_mines_signal_buttons())

# ✅ Get Mines 2 Signal Handler
@dp.callback_query(lambda c: c.data == "get_mines2_signal")
async def send_mines2_signal(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    
    # Get the selected mines count for this user from mines2 selection
    mines_count = user_mines_selection.get(f"mines2_{user_id}", 2)  # Default to 2 if not found
    
    checking_msg = await bot.send_message(callback_query.from_user.id, "Checking...⏳")
    await asyncio.sleep(random.randint(2, 3))
    await bot.delete_message(callback_query.from_user.id, checking_msg.message_id)

    result = generate_mines2_signal(mines_count)
    if isinstance(result, tuple):
        signal, mines2_image_path = result
        if mines2_image_path:
            # Send the generated mines2 image
            photo = FSInputFile(mines2_image_path)
            await bot.send_photo(
                callback_query.from_user.id, 
                photo=photo, 
                caption=signal, 
                reply_markup=get_mines2_signal_buttons()
            )
            return
    else:
        signal = result
    
    await bot.send_message(callback_query.from_user.id, signal, reply_markup=get_mines2_signal_buttons())

# ✅ Get Signal Handler
@dp.callback_query(lambda c: c.data.startswith("get_signal_"))
async def send_signal(callback_query: types.CallbackQuery):
    await callback_query.answer()
    checking_msg = await bot.send_message(callback_query.from_user.id, "Checking...⏳")
    await asyncio.sleep(random.randint(2, 3))
    await bot.delete_message(callback_query.from_user.id, checking_msg.message_id)

    game_type = callback_query.data.split("_")[2]
    signal = ""
    image_url = None

    if game_type == "mines2":
        result = generate_mines2_signal()
        if isinstance(result, tuple):
            signal, mines2_image_path = result
            if mines2_image_path:
                # Send the generated mines2 image
                photo = FSInputFile(mines2_image_path)
                await bot.send_photo(
                    callback_query.from_user.id, 
                    photo=photo, 
                    caption=signal, 
                    reply_markup=get_game_buttons(game_type)
                )
                return
        else:
            signal = result
    elif game_type == "aviator":
        signal = generate_aviator_signal()
        image_url = "https://i.postimg.cc/4ygKyN6f/IMG-20250308-003502.jpg"
    elif game_type == "luckyjet":
        signal = generate_luckyjet_signal()
        image_url = "https://i.postimg.cc/vHN15rgb/photo-5933696842585983741-y.jpg"
    elif game_type == "crash":
        signal = generate_crash_signal()
        image_url = "https://i.postimg.cc/NFQmFmJm/photo-5949366588383807408-y.jpg"
    elif game_type == "penalty":
        signal = generate_penalty_signal()
        image_url = "https://i.postimg.cc/g2Vm7J5X/photo-5949366588383807421-y.jpg"
    elif game_type == "brawlpirates":
        await bot.send_message(callback_query.from_user.id, "⚠️ This game is temporarily unavailable.", reply_markup=get_game_menu())
        return

    if image_url:
        await bot.send_photo(callback_query.from_user.id, photo=image_url, caption=signal, reply_markup=get_game_buttons(game_type))
    else:
        await bot.send_message(callback_query.from_user.id, signal, reply_markup=get_game_buttons(game_type))

# ✅ Back Button
@dp.callback_query(lambda c: c.data == "back")
async def go_back(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    photo = FSInputFile("casino_menu.png")
    await bot.send_photo(
        callback_query.from_user.id,
        photo=photo,
        caption="🎮 Select a game to get signals!",
        reply_markup=get_game_menu()
    )

# ✅ Run Bot
async def main():
    try:
        print("🤖 Bot is Starting...")
        # Set commands menu
        await bot.set_my_commands([
            types.BotCommand(command="start", description="Start the bot")
        ])
        print("✅ Commands menu set")
        
        # Start activation code task
        asyncio.create_task(send_activation_code())
        print("✅ Activation code task started")
        
        # Start daily posts scheduler
        asyncio.create_task(send_daily_posts())
        print("✅ Daily posts scheduler started")
        
        # Start polling
        print("🔄 Starting bot polling...")
        await dp.start_polling(bot, allowed_updates=["message", "callback_query"])
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
