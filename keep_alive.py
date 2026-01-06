from flask import Flask
from threading import Thread

app = Flask("")

html = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Robô do Bolsonaro - by xongs</title></head><body><h1>Bot is running!</h1><button onclick="redirectToGithub()">COOL STUFF</button><script>function redirectToGithub(){const url = "https://github.com/joaozacchello08";window.open(url, "_blank")}</script></body></html>'

@app.route("/")
def home():
	return html

def run():
	app.run(host="0.0.0.0", port=8080)

def keep_alive():
	t = Thread(target=run)
	t.start()
