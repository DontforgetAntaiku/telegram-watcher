import logging
import os
import sys
from threading import Thread
from time import sleep

from PIL import Image
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pystray import Icon, Menu as menu, MenuItem as item

#logging.basicConfig(filename="logs.txt", level=logging.ERROR, format='%(asctime)s %(message)s')
app = Client("my_account", api_id=api_id, api_hash='api_hash')
if 'chats' not in os.listdir("."):
	os.mkdir('chats')



class icon(Icon):
	pass

def delete_all_history(icon):
	for i in os.listdir("./chats"):
		for j in [files for files in os.listdir(f'./chats/{i}') if 'dis' not in files]:
			while True:
				try:
					os.remove(f'./chats/{i}/{j}')
					break
				except Exception:
					pass
	tray.notify('All data deleted successfully')
	sleep(2)
	tray.remove_notification()


def delete_history(icon):
	for i in os.listdir("./chats"):
		for j in [files for files in os.listdir(f'./chats/{i}') if '.txt' not in files and 'dis' not in files]:
			while True:
				try:
					os.remove(f'./chats/{i}/{j}')
					break
				except Exception as e:
					pass
	tray.notify('All media deleted successfully')
	sleep(2)
	tray.remove_notification()


def exit_btn(icon):
	commands = ['app.stop()', 'tray.stop()', 'os._exit(1)']
	tray.notify(message='App stopped', title='Message saver')
	sleep(2)
	tray.remove_notification()
	for command in commands:
		try:
			exec(command)
		except Exception as e:
			print(e)

# def restart():
# 	commands = ['app.stop()', 'tray.stop()', f"os.execl({sys.executable}, {sys.executable}, *sys.argv)"]
# 	print('Started')
# 	sleep(5)
# 	print('Yes')
# 	exit_btn(None, type='restart')
# 	python = sys.executable
# 	print(python, sys.argv)
# 	os.execl(python, python, *sys.argv)

@app.on_message(~filters.channel & filters.text & ~filters.bot & filters.incoming)
async def text(_, message):
	if message.chat.first_name is None:
		message.chat.first_name = message.chat.title
		async for i in '\\ / : * ? " < > |'.split():
			message.chat.first_name = message.chat.first_name.replace(i, '')
		message.chat.first_name = message.chat.first_name.strip()
	try:
		os.mkdir(f".\\chats\\{message.chat.first_name}")
	except FileExistsError:
		pass
	if message.chat.type == ChatType.PRIVATE and message.outgoing == True or message.chat.type == ChatType.BOT:
		return
	message.text = '→'.join(message.text.splitlines())
	if 'dis' in os.listdir(f".\\chats\\{message.chat.first_name}\\"):
		return
	with open(f'.\\chats\\{message.chat.first_name}\\messages.txt', 'at', encoding='utf-8') as f:
		if message.chat.type == ChatType.GROUP or message.chat.type == ChatType.SUPERGROUP:
			f.write(f'[{message.id}] {message.date} {message.from_user.first_name} text: "{message.text}";\n')
		elif message.chat.type == ChatType.PRIVATE:
			f.write(f'[{message.id}] {message.date} text: "{message.text}";\n')
	if 'README.txt' not in os.listdir(f".\\chats\\{message.chat.first_name}\\") or 'disable.bat' not in os.listdir(
			f".\\chats\\{message.chat.first_name}\\"):
		with open(f'.\\chats\\{message.chat.first_name}\\README.txt', 'wt', encoding='utf-8') as f:
			f.write('Create file "dis" for disable this chat')
		with open(f".\\chats\\{message.chat.first_name}\\disable.bat", 'wt', encoding='utf-8') as f:
			f.write('null >> dis & exit')


@app.on_message(~filters.channel & ~filters.text & ~filters.bot & filters.incoming)
async def download(_, message):
	if message.chat.first_name is None:
		message.chat.first_name = message.chat.title
		async for i in '\\ / : * ? " < > |'.split():
			message.chat.first_name = message.chat.first_name.replace(i, '')
		message.chat.first_name = message.chat.first_name.strip()
	try:
		os.mkdir(f".\\chats\\{message.chat.first_name}")
	except FileExistsError:
		pass
	if message.outgoing == True or 'dis' in os.listdir(f".\\chats\\{message.chat.first_name}\\"):
		return
	try:
		a = message.download(
			file_name=f'.\\chats\\{message.chat.first_name}\\')
		filename = message.date.strftime(f"%d-%m (%H %M %S).") + a.split('.')[-1]
	except ValueError:
		return
	i = 1
	while True:
		try:
			os.rename(a, f'{os.getcwd()}.\\chats\\{message.chat.first_name}\\{filename}')
			break
		except PermissionError:
			sleep(2)
		except FileExistsError:
			filename = message.date.strftime(f"%d-%m (%H %M %S) ({str(i)}).") + a.split('.')[-1]
			i = i + 1


@app.on_edited_message(~filters.channel & filters.text & ~filters.bot & ~filters.me)
async def edited_text(_, message):
	if message.chat.first_name is None:
		message.chat.first_name = message.chat.title
		async for i in '\\ / : * ? " < > |'.split():
			message.chat.first_name = message.chat.first_name.replace(i, '')
		message.chat.first_name = message.chat.first_name.strip()
	if message.outgoing == True or 'dis' in os.listdir(f".\\chats\\{message.chat.first_name}\\"):
		return
	message.text = '→'.join(message.text.splitlines())
	with open(f'.\\chats\\{message.chat.first_name}\\messages.txt', 'rt', encoding='utf-8', ) as f:
		file_text = [i async for i in f.read().split('\n') if i != '']
	async for i in range(len(file_text)):
		if file_text[i].find(f'[{message.id}]') == 0:
			file_text[i] = file_text[i] + f' {message.edit_date} edited to text: "{message.text}";'
			if 'edited.txt' not in os.listdir(f'.\\chats\\{message.chat.first_name}'):
				open(f'.\\chats\\{message.chat.first_name}\\edited.txt', 'wt', encoding='utf-8', )
			with open(f'.\\chats\\{message.chat.first_name}\\edited.txt', 'at', encoding='utf-8', ) as f:
				f.write(f'{file_text[i]}\n')
	with open(f'.\\chats\\{message.chat.first_name}\\messages.txt', 'wt', encoding='utf-8') as f:
		async for i in file_text:
			f.write(f'{i}\n')


@app.on_deleted_messages(~filters.channel & ~filters.me)  # filters.private & ~filters.me & ~filters.bot
async def deleted_text(_, message):
	chat_name = ''
	async for i in [name async for name in os.listdir(".\\chats\\")]:
		if 'messages.txt' not in os.listdir(f".\\chats\\{i}"):
			continue
		with open(f'.\\chats\\{i}\\messages.txt', 'rt', encoding='utf-8') as f:
			file_text = [i async for i in f.read().split('\n') if i != '']
		async for a in range(len(file_text)):
			async for b in range(len(message)):
				if file_text[a].find(f'[{message[b].id}]') == 0:
					file_text[a] = file_text[a] + ' deleted;'
					with open(f'.\\chats\\{i}\\messages.txt', 'wt', encoding='utf-8') as f:
						async for j in file_text:
							f.write(f'{j}\n')
					if 'deleted.txt' not in os.listdir(f'.\\chats\\{i}\\'):
						open(f'.\\chats\\{i}\\deleted.txt', 'wt', encoding='utf-8')
					with open(f'.\\chats\\{i}\\deleted.txt', 'at', encoding='utf-8') as f:
						f.write(f'{file_text[a]}\n')
					chat_name = i
	async for i in app.get_dialogs():
		if i.chat.first_name == chat_name:
			await i.chat.mark_unread()
			break

if __name__ == "__main__":
	if 'enable' not in os.listdir(os.environ.get('windir')):
		os._exit(1)
	try:
		os.remove('First use.exe')
	except:
		pass
	global tray
	tray = icon('Message saver', Image.open(
		os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), 'icon.png')),
							   menu=menu(item('Open folder', lambda: os.startfile(os.getcwd()), default=True),
										 item('What to delete?', menu(
											 item('All data', delete_all_history),
											 item('All media(.mp4, .mp3 and more)', delete_history))),
										 item('Exit', exit_btn),
										 ), title='Message saver')
	Thread(target=lambda: tray.run()).start()
	# Thread(target=restart).start()
	app.run()
