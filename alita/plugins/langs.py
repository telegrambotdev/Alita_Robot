from alita.__main__ import Alita
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from alita.utils.localization import GetLang, langdict
from alita.db import lang_db as db
from alita import PREFIX_HANDLER
from alita.utils.admin_check import admin_check


__PLUGIN__ = "Language"

__help__ = """
Not able to change language of the bot?
Easily change by using this module!

Just type /lang and use inline keyboard to choose a language \
for yourself or your group.
"""


def gen_langs_kb():
    langs = list(langdict)
    kb = []
    while langs:
        lang = langdict[langs[0]]
        a = [
            InlineKeyboardButton(
                f"{lang['language_flag']} {lang['language_name']}",
                callback_data=f"set_lang.{langs[0]}",
            )
        ]
        langs.pop(0)
        if langs:
            lang = langdict[langs[0]]
            a.append(
                InlineKeyboardButton(
                    f"{lang['language_flag']} {lang['language_name']}",
                    callback_data=f"set_lang.{langs[0]}",
                )
            )
            langs.pop(0)
        kb.append(a)
    return kb


@Alita.on_callback_query(filters.regex("^chlang$"))
async def chlang_callback(c: Alita, m: CallbackQuery):
    _ = GetLang(m).strs
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            *gen_langs_kb(),
            [
                InlineKeyboardButton(
                    "« " + _("general.back_btn"), callback_data="start_back"
                )
            ],
        ]
    )
    await m.message.edit_text(_("lang.changelang"), reply_markup=keyboard)
    await m.answer()
    return


@Alita.on_callback_query(filters.regex("^close$"))
async def close_btn_callback(c: Alita, m: CallbackQuery):
    await m.message.delete()
    await m.answer()
    return


@Alita.on_callback_query(filters.regex("^set_lang."))
async def set_lang_callback(c: Alita, m: CallbackQuery):
    _ = GetLang(m).strs
    if m.message.chat.type == "private":
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        "« " + _("general.back_btn"), callback_data="start_back"
                    )
                ]
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton("❌ " + _("close_btn"), callback_data="close")]
            ]
        )
    db.set_lang(m.message.chat.id, m.message.chat.type, m.data.split(".")[1])
    await m.message.edit_text(
        "🌐 " + _("langs.changed").format(lang_code=m.data.split(".")[1]),
        reply_markup=keyboard,
    )
    await m.answer()
    return


@Alita.on_message(filters.command(["lang", "setlang"], PREFIX_HANDLER))
async def set_lang(c: Alita, m: Message):

    res = await admin_check(c, m)
    if not res:
        return

    _ = GetLang(m).strs
    keyboard = InlineKeyboardMarkup(inline_keyboard=[*gen_langs_kb()])
    if len(m.text.split()) >= 2:
        await m.reply_text(_("langs.correct_usage"))
        return
    await m.reply_text(_("lang.changelang"), reply_markup=keyboard)
    return
