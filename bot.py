import ssl
import requests
from bs4 import BeautifulSoup
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import tkinter as tk

#Set the SSL certificate verification path
ssl._create_default_https_context = ssl._create_unverified_context

#Scrape drug names from nhs
url = 'https://www.nhs.uk/medicines/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
drugNames = []
drugURLS = []
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    if href and '/medicines/' in href:
        drugName = link.text.strip()
        drugNames.append(drugName)
        drugURL = "https://www.nhs.uk{}".format(href)
        drugURLS.append(drugURL)
drugNames = drugNames[22:]
drugURLS = drugURLS[22:]
drugDictionary = dict(zip(drugNames, drugURLS))

#Print drug names
print(drugDictionary)

#Train chatbot on drug names
chatbot = ChatBot('Health Bot')
trainer = ListTrainer(chatbot)
trainer.train(drugNames + drugURLS)

corpusTrainer = ChatterBotCorpusTrainer(chatbot)
corpusTrainer.train("chatterbot.corpus.english.greetings",
                     "chatterbot.corpus.english.conversations",
                     "chatterbot.corpus.english")

#Train chatbot
trainer.train([
	"Hi",
	"Welcome, friend 🤗",
])
trainer.train([
    "Are you a plant?",
    "No, I'm the pot below the plant!",
])

def text():
    query = textbox.get()
    print("You:", query)
    textbox.delete(0, tk.END)

    if 'side effects' in query:
        for word in query.split():
            if word in drugDictionary:
                reply = f"🔗 Here you can learn more about the side effects of {word} : {drugDictionary[word]}side-effects-of-{word}"
                print("Health Bot:", reply)
                textHistory.insert(tk.END, "You: " + query)
                textHistory.insert(tk.END, "Health Bot: " + reply)
                return reply

    for word in query.split():
        if word in drugDictionary:
            reply = f"🔗 The link to the information about {word} is: {drugDictionary[word]}"
            print("Health Bot:", reply)
            textHistory.insert(tk.END, "You: " + query)
            textHistory.insert(tk.END, "Health Bot: " + reply)
            return reply

    else:
        reply = str(chatbot.get_response(query))
        print("Health Bot:", reply)
        textHistory.insert(tk.END, "You: " + query)
        textHistory.insert(tk.END, "Health Bot: " + reply)

def export():
    file = open("chatHistory.txt", "w")
    for i in range(textHistory.size()):
        file.write(textHistory.get(i) + "\n")

userInterface = tk.Tk()
userInterface.title("Health Bot")
userInterface.geometry("3072x1920")

textHistory = tk.Listbox(userInterface, height=25, width=50, font=("Helvetica", 20))
textHistory.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

textboxSendPackage = tk.Frame(userInterface)
textboxSendPackage.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

textbox = tk.Entry(textboxSendPackage, font=("Helvetica", 18), width=145)
textbox.pack(side=tk.LEFT, fill=tk.X)

send = tk.Button(textboxSendPackage, text='Send', font=('Helvetica', 18), command=text)
send.pack(side=tk.RIGHT, padx=10, pady=10)

export = tk.Button(textboxSendPackage, text='Export', font=('Helvetica', 18), command=export)
export.pack(side=tk.RIGHT, padx=10, pady=10)

userInterface.mainloop()