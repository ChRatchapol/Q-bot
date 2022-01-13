# Discord Queue Management Bot V 1.0
# ## TODO LIST
# -todo 1. แก้ __next__ ของ Queue 
# -todo 2. แก้ตอนส่งค่าให้ add และ remove ให้เอาค่าแค่จากภายใน " เท่านั้น
#  todo 3. แก้แกรมม่าในคอมเม้นต์ และคำอธิบาย

# | IMPORT SECTION
import discord
import os
import time

from dotenv import load_dotenv
from ggsheet.main import sheet_init, sheet_template_gen, sheet_write
from typing import List
from utils import chk_cmd, param_lst2param_dct, parse_cmd, QueueBotQ, write, load


# | GLOBAL EXECUTION
load_dotenv()
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")
COMMAND_LIST = eval(os.getenv("COMMAND_LIST"))
ADMIN_ROLE = os.getenv("ADMIN_ROLE")
QUEUE_FILE_NAME = os.getenv("QUEUE_FILE_NAME")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

CLIENT = discord.Client()

Q = QueueBotQ(size=17)
START = time.perf_counter()

# | FUNCTIONS


def fill_template(template: List[List[str]], filename: str) -> List[List[str]]:
    """
    fill GGSheet template list with data in QueueBotQ file (For Inno. queue only)

    Parameters
    ----------
    template : List[List[str]]
        GGSheet template list
    filename : str
        filename or filepath that store data of the queue

    Returns
    -------
    List[List[str]]
        template that already filled
    """

    res = template.copy()
    with open(filename, "rt", encoding="utf-8") as f:
        lines = f.readlines()
        data = [line.strip() for line in lines]
        data = [tuple(line.split(",")) for line in data]

        if len(data) < 17:
            data += [("", "")] * (17 - len(data))

        for row in range(len(res)):
            if row == 0:
                continue
            else:
                res[row][0] = data[row - 1][0]
                res[row][1] = data[row - 1][1]

    return res


async def chk_channel(servers: List[discord.Guild]) -> None:
    """
    check if all channels in all servers Q Bot is in have all category and channels

    Parameters
    ----------
    servers : List[discord.Guild]
        servers that will be checked
    """

    global ADMIN_ROLE

    for server in servers:
        print(f"checking {server.name}")

        roles_name_lst = [role.name for role in server.roles]
        if ADMIN_ROLE not in roles_name_lst:
            await server.create_role(
                name="TA",
                colour=discord.Color.magenta(),
                hoist=True,
                mentionable=True,
            )

        Q_Bot_cat = None
        for cat in server.categories:
            if "Q Bot" == cat.name:
                Q_Bot_cat = cat
                break
        if Q_Bot_cat is None:
            await create_text_ch(server, 0)
        else:
            have_q_ch = False
            have_r_q_ch = False
            for text_ch in Q_Bot_cat.text_channels:
                if "___queue___" == text_ch.name:
                    have_q_ch = True
                if "___run_queue___" == text_ch.name:
                    have_r_q_ch = True

                    for r in server.roles:
                        if r.name == ADMIN_ROLE:
                            role = r
                        if r.name == "@everyone":
                            e = r

                    await text_ch.set_permissions(
                        e, read_messages=True, send_messages=False
                    )
                    await text_ch.set_permissions(
                        role, read_messages=True, send_messages=True
                    )
                    await text_ch.set_permissions(
                        server.get_member(CLIENT.user.id),
                        read_messages=True,
                        send_messages=True,
                    )

            if not have_q_ch:
                await create_text_ch(server, 1)
            if not have_r_q_ch:
                await create_text_ch(server, 2)

    print("checking done!")


async def create_text_ch(server: discord.Guild, mode: int) -> None:
    """
    create category and/or channels Q Bot needed in the server

    Parameters
    ----------
    server : discord.Guild
        Server that will create category and/or channels in to.
    mode : int
        mode for specify that will create category and all channels (0), create just ___queue___ (1) or create just ___run_queue___ (2)
    """

    global ADMIN_ROLE
    global CLIENT

    if mode == 0:
        cat = await server.create_category(
            name="Q Bot", reason="needed for Q Bot to work", position=0
        )
    else:
        cat = [c for c in server.categories if c.name == "Q Bot"][0]

    if mode == 0 or mode == 1:
        await server.create_text_channel(
            name="___queue___", category=cat, reason="needed for Q Bot to work"
        )

    if mode == 0 or mode == 2:
        tmp = await server.create_text_channel(
            name="___run_queue___", category=cat, reason="needed for Q Bot to work"
        )

        for r in server.roles:
            if r.name == ADMIN_ROLE:
                role = r
            if r.name == "@everyone":
                e = r

        await tmp.set_permissions(e, read_messages=True, send_messages=False)
        await tmp.set_permissions(role, read_messages=True, send_messages=True)
        await tmp.set_permissions(
            server.get_member(CLIENT.user.id), read_messages=True, send_messages=True
        )


@CLIENT.event
async def on_ready() -> None:
    """
    things to do when Q Bot is ready
    """
    global CLIENT
    global START

    user = CLIENT.user
    servers = CLIENT.guilds
    servers_text = ", ".join([server.name for server in servers])
    print(f"I've logged in as {user} and in this/these server(s): {servers_text}")
    await chk_channel(servers)
    START = time.perf_counter()


@CLIENT.event
async def on_message(msg: discord.Message) -> None:
    """
    things to do when Q Bot detect message sending

    Parameters
    ----------
    msg : discord.Message
        Message object that Q Bot detected
    """

    global CLIENT
    global START
    global Q
    global QUEUE_FILE_NAME

    channel = msg.channel
    channel_name = channel.name
    channel_cat = channel.category.name
    content = msg.content
    server = msg.guild
    categories = server.categories
    group_cat = [c for c in categories if c.name == "Group"][0]
    group_text_ch = group_cat.text_channels

    if time.perf_counter() - START >= 60:
        await chk_channel(CLIENT.guilds)
        START = time.perf_counter()

    if msg.author == CLIENT.user:
        return

    if chk_cmd(content):
        command_dct = parse_cmd(content)
        print(command_dct)
        if command_dct["command"] == "$list":
            new_msg = Q.show()
            await msg.channel.send(
                "```" + new_msg + "```"
                if new_msg != ""
                else "The queue is currently empty!"
            )
            return

        elif command_dct["command"] == "$help":
            bar = "─" * 30
            double_bar = "═" * 30
            embed = discord.Embed(
                title="**__Help__**",
                description=f"_Q Bot command list_\n{double_bar}",
                colour=discord.Colour.random(),
            )
            embed.add_field(
                name="**`$add`**",
                value=f"""
                {bar}

                **description:** เพิ่มกลุ่มลงไปในคิว

                **usage:** `$add [group name] [topic]`

                **parameter detail:**
                **• group name:** ชื่อกลุ่ม ต้องอยู่ในเครื่องหมายคำพูด (") **และต้องชื่อเหมือนกับ text channel ใน discord**
                **• topic:** หัวข้อที่จะนำเสนอ ต้องอยู่ในเครื่องหมายคำพูด (")

                **หมายเหตุ:** หากต้องการใช้เครื่องหมายคำพูดในหัวช้อให้ใส่ \ นำหน้าตัวที่ต้องการ

                **example:** `$add "Robot Family" "\\"Am I cute?\\""`

                {double_bar}
                """,
                inline=False,
            )
            embed.add_field(
                name="**`$remove`**",
                value=f"""
                {bar}
                
                **description:** ลบกลุ่มลงไปในคิว

                **usage:** `$remove [group name]`

                **parameter detail:**
                **• group name:** ชื่อกลุ่ม ต้องอยู่ในเครื่องหมายคำพูด (") **และต้องชื่อเหมือนกับ text channel ใน discord**

                **example:** `$remove "work fast like a sloth"`

                {double_bar}
                """,
                inline=False,
            )
            embed.add_field(
                name="**`$list`**",
                value=f"""
                {bar}
                
                **description:** แสดงคิว

                **usage:** `$list`

                **example:** `$list`

                {double_bar}
                """,
                inline=False,
            )
            embed.add_field(
                name="**`$next`**",
                value=f"""
                {bar}
                
                **description:** แสดงกลุ่มต่อไปในคิว และนำออกจากคิว

                **usage:** `$next`

                **example:** `$next`

                {double_bar}
                """,
                inline=False,
            )
            embed.add_field(
                name="**`$help`**",
                value=f"""
                {bar}

                **description:** แสดงข้อความช่วยเหลือ

                **usage:** `$help`

                **example:** `$help`

                {double_bar}
                """,
                inline=False,
            )
            await msg.channel.send(embed=embed)
            return

        elif channel_name == "___queue___" and channel_cat == "Q Bot":
            if command_dct["command"] == "$add":
                if len(command_dct["parameters"]) != 2:
                    await msg.channel.send(
                        f"The $add command accepts 2 parameters as strings, but got {len(command_dct['parameters'])} parameter(s)"
                    )
                else:
                    for item in Q:
                        if item["group"] == command_dct["parameters"][0]:
                            await msg.channel.send(
                                f"{item['group']} is already in the queue. Remove it first!"
                            )
                            return

                    noti_channel = discord.utils.get(
                        group_text_ch,
                        name=command_dct["parameters"][0],
                    )
                    if noti_channel is None:
                        await msg.channel.send(
                            f"text channel {command_dct['parameters'][0]} not found!"
                        )
                    else:
                        try:
                            Q.push(param_lst2param_dct(command_dct["parameters"]))
                        except QueueBotQ.Full:
                            await msg.channel.send("The queue is currently full!")
                        else:
                            await noti_channel.send(
                                f"Group: **{command_dct['parameters'][0]}** Topic: **{command_dct['parameters'][1]}** is added to the queue by <@{msg.author.id}>."
                            )

            elif command_dct["command"] == "$remove":
                if len(command_dct["parameters"]) != 1:
                    await msg.channel.send(
                        f"the $remove command accepts a single parameter as an integer, but got {len(command_dct['parameters'])} parameter(s)"
                    )
                else:
                    try:
                        noti_channel = discord.utils.get(
                            group_text_ch,
                            name=command_dct["parameters"][0],
                        )
                        if noti_channel is None:
                            await msg.channel.send(
                                f"text channel {command_dct['parameters'][0]} not found!"
                            )
                        else:
                            done = False
                            for item in Q:
                                if item["group"] == command_dct["parameters"][0]:
                                    Q.remove_from_value(item)
                                    await noti_channel.send(
                                        f"Group: **{command_dct['parameters'][0]}** is removed from the queue by <@{msg.author.id}>."
                                    )
                                    done = True
                                    break
                            if not done:
                                await msg.channel.send(
                                    f"{command_dct['parameters'][0]} is not in the queue!"
                                )
                    except ValueError:
                        await msg.channel.send(
                            f"{command_dct['parameters'][0]} is not in the queue!"
                        )

            elif command_dct["command"] == "$next":
                await msg.channel.send(
                    "`$next` can only use in Q Bot > \_\_\_run_queue\_\_\_."
                )

        elif channel_name == "___run_queue___" and channel_cat == "Q Bot":
            if command_dct["command"] == "$next":
                try:
                    nxt = Q.pop()
                    noti_channel = discord.utils.get(
                        group_text_ch,
                        name=nxt["group"],
                    )
                    await noti_channel.send(f"You're next! Congratulations!")
                    await msg.channel.send(
                        "\n".join([f"**{k}:** {v}" for k, v in nxt.items()])
                    )
                except QueueBotQ.Empty:
                    await msg.channel.send("The queue is currently empty!")

    write(Q, QUEUE_FILE_NAME)
    Q = load(QUEUE_FILE_NAME)
    data = fill_template(sheet_template_gen(), QUEUE_FILE_NAME)
    print("writing to sheet")
    print(sheet_write("Queue!A1", data))


# | MAIN
if __name__ == "__main__":
    sheet_init(SPREADSHEET_ID)
    Q = load(QUEUE_FILE_NAME)

    data = fill_template(sheet_template_gen(), QUEUE_FILE_NAME)
    print("writing to sheet")
    print(sheet_write("Queue!A1", data))

    CLIENT.run(os.getenv("DISCORD_BOT_TOKEN"))
