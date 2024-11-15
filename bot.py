import os
import time
import sys
import asyncio
import requests
import random
from telethon import TelegramClient, functions
from telethon.errors import YouBlockedUserError, SessionPasswordNeededError

b = "\033[1;34m"
c = "\033[1;36m"
d = "\033[0m"
h = "\033[1;32m"
k = "\033[1;33m"
m = "\033[1;31m"
p = "\033[1;37m"
u = "\033[1;35m"

class Display:
    @staticmethod
    def Error(msg):
        print(m + "---[" + p + "😭" + m + "] " + p + msg)
        
    @staticmethod
    def Sukses(msg):
        print(h + "---[" + p + "🥰" + h + "] " + p + msg)
        
    @staticmethod
    def Line():
        print(b + "─" * 60)
        
    @staticmethod
    def Clear():
        os.system('cls' if os.name == 'nt' else 'clear')

class Functions:
    @staticmethod
    def Explode(str, src):
        return src.split(str)

def countdown_animation(seconds):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = f"{h}{mins:02}:{secs:02}{d} remaining"
        print(timer, end="\r")
        time.sleep(1)
        seconds -= 1
    print(" " * 30, end="\r")

Display.Clear()

api_id = '20050469'
api_hash = '23f3cef31d35cb546e5a932f6e83f7ad'

session_folder = "sessions"
if not os.path.exists(session_folder):
    os.makedirs(session_folder)

existing_sessions = [f.replace(".session", "") for f in os.listdir(session_folder) if f.endswith(".session")]

while True:
    print(p + ("Pilih:" + d))
    print("\033[1;32m[1]. Tambahkan akun baru\033[0m")
    print("\033[1;32m[2]. Jalankan akun yang sudah ada\033[0m")

    choice = input(p + ("Masukkan pilihan: " + d))

    if choice == "1":
        num_sessions = int(input(p +"Berapa yang ingin dibuat? " + d))
        sessions = []

        async def create_new_session(session_name, phone_number):
            client = TelegramClient(os.path.join(session_folder, session_name), api_id, api_hash)
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                code = input(p + f"Masukkan kode OTP '{session_name}': " + d)
                try:
                    await client.sign_in(phone_number, code)
                except SessionPasswordNeededError:
                    password = input(p + f"Akun ini memiliki 2FA. Masukkan password: " + d)
                    await client.sign_in(password=password)
                Display.Sukses(f"\033[1;32m'{session_name}' Berhasil dibuat!\033[0m")
            await client.disconnect()

        for i in range(1, num_sessions + 1):
            session_name = f"session_{i}"
            phone_number = input(p + f"Masukkan nomor telepon (dengan +62) '{session_name}': " + d)
            sessions.append(session_name)
            asyncio.run(create_new_session(session_name, phone_number))
        break

    elif choice == "2":
        sessions = existing_sessions
        break

    else:
        Display.Error("Pilihan tidak valid. Silakan coba lagi.")
        
Display.Clear()
Display.Line()

async def delay_execution(coro, *args, **kwargs):
    await asyncio.sleep(3)
    return await coro(*args, **kwargs)

async def GetEntity(client, bot_entity):
    try:
        channel_entity = await delay_execution(client.get_entity, bot_entity)
        await delay_execution(client.send_message, entity=channel_entity, message="/start")
    except YouBlockedUserError:
        channel_entity = await delay_execution(client.get_entity, bot_entity)
        idc = channel_entity.id
        await delay_execution(client, functions.contacts.UnblockRequest(id=idc))
        await delay_execution(client.send_message, entity=channel_entity, message="/start")
    return channel_entity

async def Visit(client, channel_entity):
    repeat_count = 0
    last_message = None

    while True:
        try:
            await delay_execution(client.send_message, entity=channel_entity, message="💻 Visit Sites")
            await asyncio.sleep(7)
            r = await delay_execution(client.get_messages, channel_entity, limit=2)
            await asyncio.sleep(5)

            if r[0].message == last_message:
                repeat_count += 1
                if repeat_count >= 2:
                    Display.Error("NEXT...")
                    Display.Line()
                    try:
                        await r[0].click(text="➡️ Skip")
                    except Exception as e:
                        Display.Error(f"Gagal mengklik tombol '➡️ Skip': {e}")
                    Display.Line()
                    break
            else:
                repeat_count = 0
                last_message = r[0].message

            try:
                url = r[0].reply_markup.rows[0].buttons[1].url
            except:
                Display.Error("Site habis")
                Display.Line()
                break

            try:
                curl = requests.Session()
                r = curl.get(url=url).text
                tmr = Functions.Explode(";", Functions.Explode("let x = ", r)[1])[0]
                token = Functions.Explode('">', Functions.Explode('<input name="session" value="', r)[1])[0]
                countdown_animation(int(tmr))
                data = {"session": token}
                r = curl.post(url, data=data)

                await asyncio.sleep(5)
                r = await delay_execution(client.get_messages, channel_entity, limit=2)
                Display.Sukses(r[0].message)
            except requests.exceptions.TooManyRedirects:
                await asyncio.sleep(3)
                r = await delay_execution(client.get_messages, channel_entity, limit=2)
                Display.Error(r[0].message)
        except KeyboardInterrupt:
            exit("[ t.me/hiddensx ]")

async def send_start_message(client, channel_entity):
    await asyncio.sleep(1)
    try:
        await client.send_message(entity=channel_entity, message="/start")
    except Exception as e:
        Display.Error(f"Next: {e}")

async def JoinBots(client, channel_entity):
    same_message_count = 0
    last_message = None

    while True:
        try:
            await client.send_message(entity=channel_entity, message="🤖 Join Bots")
            await asyncio.sleep(7)
            r = await client.get_messages(channel_entity, limit=2)
            
            if "❌ An error occurred ⚠️ You completed the same task from multiple accounts" in r[1].message:
                Display.Error("NOT COMPLETE")
                Display.Line()
                break
            
            if last_message is not None and r[0].message == last_message:
                same_message_count += 1
            else:
                same_message_count = 0
            
            last_message = r[0].message

            if same_message_count >= 2:
                Display.Error("NEXT...")
                Display.Line()
                break

            try:
                url = r[0].reply_markup.rows[0].buttons[0].url
            except:
                Display.Error("Join bot habis")
                Display.Line()
                break

            chnel = "@" + Functions.Explode("?", Functions.Explode("/", url)[3])[0]
            try:
                msgchnl = await client.get_entity(chnel)
                await asyncio.sleep(3)
                r = await client.get_messages(channel_entity, limit=2)
                await r[0].click(text="✅ Started")
                await asyncio.sleep(2)

                await client.send_message(entity=msgchnl, message="/start")
                await asyncio.sleep(7)

                res = await client.get_messages(msgchnl, limit=2)
                if "/start" in res[0].message:
                    await client.send_message(entity=channel_entity, message="🔙 Back")
                    await asyncio.sleep(7)
                    await client.send_message(entity=channel_entity, message="🤖 Join Bots")
                    await asyncio.sleep(7)
                    r = await client.get_messages(channel_entity, limit=2)
                    await r[0].click(text="➡️ Skip")
                else:
                    await res[0].forward_to(channel_entity)
                    await asyncio.sleep(7)

                    r = await client.get_messages(channel_entity, limit=2)
                    Display.Sukses(r[1].message)
            except YouBlockedUserError:
                msgchnl = await client.get_entity(chnel)
                idx = msgchnl.id
                await client(functions.contacts.UnblockRequest(id=idx))
        except KeyboardInterrupt:
            exit("[ t.me/hiddensx ]")
        except Exception as e:
            Display.Error("NOT COMPLETE")
            Display.Line()
            break

    await send_start_message(client, channel_entity)
    await asyncio.sleep(2)

async def JoinChannel(client, channel_entity):
    previous_message = None

    while True:
        await client.send_message(entity=channel_entity, message="📢 Join Channels")
        await asyncio.sleep(7)
        
        r = await client.get_messages(channel_entity, limit=2)
        
        if previous_message is not None and r[0].message == previous_message:
            Display.Error("NEXT...")
            Display.Line()
            break
        
        previous_message = r[0].message

        try:
            url = r[0].reply_markup.rows[0].buttons[0].url
        except:
            Display.Error("Join channel habis")
            Display.Line()
            break

        try:
            chnel = "@" + Functions.Explode("/", url)[3]
            await client(JoinChannelRequest(f"{chnel}"))
            await asyncio.sleep(2)
            await r[0].click(text="✅ Joined")
            await asyncio.sleep(7)
            r = await client.get_messages(channel_entity, limit=2)
            Display.Sukses(r[0].message)
        except:
            r = await client.get_messages(channel_entity, limit=2)
            await r[0].click(text="➡️ Skip")
            
async def ViewPosts(client, channel_entity):
    stop_message = "⛔️ Oh no! There are NO TASKS available at the moment. Please check back later! ⏰\n\nYou can promote your own channels, groups, or bots with /OrderAds."
    error_message = "❌ An error occurred ⚠️ You completed the same task from multiple accounts\n\n❌ Payment has been refused"
    last_message = None
    
    while True:
        try:
            await client.send_message(entity=channel_entity, message="🤩 More")
            await asyncio.sleep(2)
            
            await client.send_message(entity=channel_entity, message="📄 View Posts")
            await asyncio.sleep(2)
            
            response = await client.get_messages(channel_entity, limit=2)
            
            if response:
                if stop_message in response[0].message:
                    Display.Error("View posts habis")
                    Display.Line()
                    break
                elif error_message in response[1].message:
                    Display.Error("NOT COMPLETE")
                    Display.Line()
                    break
            
            if last_message is not None and response[0].message == last_message:
                Display.Error("NEXT...")
                Display.Line()
                break
            
            last_message = response[0].message
            
            await asyncio.sleep(20)
            
            try:
                r = await client.get_messages(channel_entity, limit=2)
                
                if r and r[1].buttons:
                    await r[1].click(0, 1)
                    
                    await asyncio.sleep(2)
                    
                    r = await client.get_messages(channel_entity, limit=2)
                    
                    Display.Sukses(r[0].message)
                else:
                    Display.Error("Tidak ada tombol yang ditemukan.")
            except Exception as e:
                Display.Error(f"Error: {e}")
                
            await asyncio.sleep(5)
            
        except Exception as e:
            Display.Error(f"Error pada fungsi ViewPosts: {e}")
            break          

async def GetBalance(client, channel_entity):
    await client.send_message(entity=channel_entity, message="💰 Balance")
    await asyncio.sleep(7)
    r = await client.get_messages(channel_entity, limit=2)

    if r and len(r) > 0:
        lines = r[0].message.splitlines()
        if len(lines) > 3:
            balan = lines[3].strip()
            Display.Sukses("Balance: " + balan)
        else:
            Display.Error("Tidak cukup informasi pada pesan.")
    else:
        Display.Error("Tidak ada pesan yang diterima.")

    Display.Line()    
    
    await client.send_message(entity=channel_entity, message="/start")
    return channel_entity

async def process_session(session_name):
    client = TelegramClient(os.path.join(session_folder, session_name), api_id, api_hash)
    await client.start()
    me = await client.get_me()

    try:
        akun_name = f"{h}\033[1m=== Akun: {me.username if me.username else me.first_name} ==={d}\033[0m"
        print(akun_name)
    except:
        print(f"{h}\033[1m=== Akun: Tidak Diketahui ==={d}\033[0m")

    Display.Line()

    bot_entity = "@ClickBeeLTCBot"
    try:
        channel_entity = await GetEntity(client, bot_entity)
        
        print(k + "🌐 Visit")
        try:
            await Visit(client, channel_entity)
        except Exception as e:
            Display.Error(f"Error in Visit function: {e}")

        print(k + "🤖 Join Bot")
        try:
            await JoinBots(client, channel_entity)
        except Exception as e:
            Display.Error(f"Error in JoinBots function: {e}")

        print(k + "📢 Join Channel")
        try:
            await JoinChannel(client, channel_entity)
        except Exception as e:
            Display.Error(f"Error in JoinChannel function: {e}")
            
        print(k + "📄 View Posts")
        try:
            await ViewPosts(client, channel_entity)
        except Exception as e:
            Display.Error(f"Error in ViewPosts function: {e}")    

        try:
            await GetBalance(client, channel_entity)
        except Exception as e:
            Display.Error(f"Error in GetBalance function: {e}")

    except Exception as e:
        Display.Error(f"Error di akun {session_name}: {e}")

    finally:
        await client.disconnect()

async def main():
    while True:
        for session in sessions:
            Display.Line()
            print(f"Menjalankan session: {session}")
            await process_session(session)
        
        print("\033[1;32mBerhasil di proses ✅\033[0m")
        countdown_animation(1800)
        Display.Clear()

if __name__ == "__main__":
    asyncio.run(main())