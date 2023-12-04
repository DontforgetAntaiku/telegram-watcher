from pyrogram import Client
from uuid import getnode
from os import environ
from random import choice
from string import printable
app = Client("my_account", api_id=1077763, api_hash='eaa5d10fa099d63e0d135fe83d2e2b9e')
print(1)
async def main():
	async with app:
		mac = ':'.join(format(getnode(), '012x')[i:i + 2] for i in range(0, 12, 2))
		secret_word = ''.join([choice(printable[:62]) for i in range(8)])
		mac = mac + secret_word
		binary = ""
		for char in mac:
			ascii_code = ord(char)
			binary_code = bin(ascii_code)[2:].zfill(8)
			binary += binary_code
		binary = input("Enter an individual password from the author:\n")
		text = ""
		for i in range(0, len(binary), 8):
			binary_code = binary[i:i + 8]
			ascii_code = int(binary_code, 2)
			char = chr(ascii_code)
			text += char
		if text == mac:
			with open(f"{environ.get('windir')}\\enable", 'wt'):
				print("Success")
		else:
			print("Wrong password")
app.run(main())