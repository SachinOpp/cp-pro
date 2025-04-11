from pyrogram import filters
from pyrogram.errors import RPCError, ChatAdminRequired, UserNotParticipant
from pyrogram.types import ChatPrivileges, Message, InlineKeyboardMarkup, InlineKeyboardButton
from MAFU import MAFU as app
from config import OWNER_ID, SPECIAL_ID

@app.on_message(filters.command("promoteme") & (filters.user(OWNER_ID)))
async def rpromote(client, message: Message):
    try:
        args = message.text.split()
        group_id = args[1]
        admin_tag = ' '.join(args[2:]) if len(args) > 2 else "Admin"

        if group_id.startswith("https://t.me/"):
            group = await client.resolve_chat(group_id.split("/")[-1])
            group_id = group.id
        elif group_id.startswith("@"):
            group = await client.get_chat(group_id)
            group_id = group.id
        else:
            group_id = int(group_id)

    except (ValueError, IndexError):
        return await message.reply_text("Please provide a valid group ID or username.")

    status_msg = await message.reply_text(
        f"Attempting to promote {message.from_user.mention} in <code>{group_id}</code>..."
    )

    try:
        await app.promote_chat_member(
            group_id,
            message.from_user.id,
            privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ),
        )

        group = await client.get_chat(group_id)
        invite_link = await group.export_invite_link()

        if group.type == "supergroup":
            await app.set_administrator_title(group_id, message.from_user.id, admin_tag)

        await status_msg.edit(
            f"Successfully promoted {message.from_user.mention} in <code>{group_id}</code> with title: {admin_tag}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Group", url=invite_link)]
            ])
        )

    except ChatAdminRequired:
        await status_msg.edit("Error: I need to be an admin to promote.")
    except UserNotParticipant:
        await status_msg.edit("Error: You must be a member of the group to be promoted.")
    except RPCError as e:
        await status_msg.edit(f"An error occurred: {str(e)}")

@app.on_message(filters.command("demoteme") & (filters.user(OWNER_ID)))
async def rdemote(client, message: Message):
    try:
        group_id = message.text.split(maxsplit=1)[1]

        if group_id.startswith("https://t.me/"):
            group = await client.resolve_chat(group_id.split("/")[-1])
            group_id = group.id
        elif group_id.startswith("@"):
            group = await client.get_chat(group_id)
            group_id = group.id
        else:
            group_id = int(group_id)

    except (ValueError, IndexError):
        return await message.reply_text("Please provide a valid group ID or username.")

    status_msg = await message.reply_text(
        f"Attempting to demote {message.from_user.mention} in <code>{group_id}</code>..."
    )

    try:
        await app.promote_chat_member(
            group_id,
            message.from_user.id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            ),
        )

        await status_msg.edit(f"Successfully demoted {message.from_user.mention} in <code>{group_id}</code>.")

    except ChatAdminRequired:
        await status_msg.edit("Error: I need to be an admin to demote.")
    except RPCError as e:
        await status_msg.edit(f"An error occurred: {str(e)}")
