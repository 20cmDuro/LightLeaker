import cloudscraper, random, configparser, time, json
from bs4 import BeautifulSoup

c = cloudscraper.create_scraper()
config = configparser.ConfigParser()
config.read("config.ini")
Interval = config["GEN"]["Interval"]
UseDiscordWebhook = config["OPTIONS"]["UseDiscordWebhook"]
DiscordWebhook = config["OPTIONS"]["DiscordWebhook"]
SaveOpt = config["OPTIONS"]["Save"]

while True:
	code = "".join(random.choice("qwertyuiopasdfghjklzxcvbnm1234567890") for i in range(6))

	request = c.get("https://prnt.sc/{}".format(code))
	soup = BeautifulSoup(request.text, "lxml")
	anotherone = soup.find_all("img", {"class":"no-click screenshot-image"})
	try:
		yikes = anotherone[0]["src"]
	except:
		yikes = "//st.prntscr.com/"
	if "//st.prntscr.com/" in yikes:
		print(f"[prnt.sc/{code}] Inválido!")
		inv = "inv"
	else:
		inv = "ninv"
		if SaveOpt == "true":
			with open(f"./scraped_imgs/{code}.png", "wb") as img:
				resp = c.get(yikes, stream=True)
				for b in resp.iter_content(1024):
					img.write(b)
				print(f"[prnt.sc/{code}] Válido!\n[prnt.sc/{code}] Salvo com sucesso!")
		elif SaveOpt == "false":
			print(f"[prnt.sc/{code}] Válido!\n[prnt.sc/{code}] Não foi salvo!")
		else:
			print("Erro na configuração de 'Save'.")
	if UseDiscordWebhook == "true":
		if inv == "ninv":
			c.post(DiscordWebhook, data=json.dumps({"username":"LightLeaker", "avatar_url": "https://i.imgur.com/jIxcJsX.png", "content": "`Com o uso de LightLeaker.`\n[ https://prnt.sc/{} ]".format(code)}), headers={"Content-Type": "application/json"})
			print(f"[prnt.sc/{code}] Enviado com o uso de uma webhook!")
	elif UseDiscordWebhook == "false":
		if inv == "ninv":
			print(f"[prnt.sc/{code}] Não foi utilizada uma webhook!")
	else:
		print("Erro na configuração de 'UseDiscordWebhook'.")
	print("Esperando {} segundo(s)...".format(Interval))
	time.sleep(int(Interval))