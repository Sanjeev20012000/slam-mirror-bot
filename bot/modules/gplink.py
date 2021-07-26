import subprocess
from functools import wraps
from bot import LOGGER, dispatcher
from bot import OWNER_ID, OWN
from telegram import ParseMode, Update
from bot.helper.telegram_helper.filters import CustomFilters
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.dispatcher import run_async

@run_async
def gplink(update: Update, context: CallbackContext):
    message = update.effective_message
    cmd = message.text.split(' ', 1)
    if len(cmd) == 1:
        message.reply_text('No gplink given by user.')
        return
    cmd = f'bash gn {cmd[1]}'
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    reply = ''
    stderr = stderr.decode()
    stdout = stdout.decode()
    if stdout:
        reply += f"*Stdout*\n`{stdout}`\n"
        LOGGER.info(f"Shell - {cmd} - {stdout}")
    if stderr:
        reply += f"*Stderr*\n`{stderr}`\n"
        LOGGER.error(f"Shell - {cmd} - {stderr}")
    if len(reply) > 3000:
        with open('shell_output.txt', 'w') as file:
            file.write(reply)
        with open('shell_output.txt', 'rb') as doc:
            context.bot.send_document(
                document=doc,
                filename=doc.name,
                reply_to_message_id=message.message_id,
                chat_id=message.chat_id)
    else:
        message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

GPLINK_HANDLER = CommandHandler(BotCommands.Gplinkcommand, gplink, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
dispatcher.add_handler(GPLINK_HANDLER)
