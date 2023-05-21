import requests
from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import openai

app = Flask(__name__)
# Beispielwerte für die Ergebnisse und ausgewählten Optionen
titles = []
links = []
selected_options = []

# Benutzerdefinierte Funktion zum Kombinieren von zwei Listen
def combine_lists(a, b):
    return zip(a, b)

@app.route('/', methods=['GET', 'POST'])
def search():
    global selected_options

    if request.method == 'POST':
        search_term = request.form["search_term"]
        selected_options = request.form.getlist('selected_options')
        print(request.form)

        driver_path = "./chromedriver"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)

        driver.get("https://www.google.com")
        try:
            accept_cookies_button = driver.find_element(By.ID, "L2AGLb")
            accept_cookies_button.click()
        except:
            pass

        time.sleep(2)

        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        search_results = soup.select('div.g')

        titles = []
        links = []
        for result in search_results[:3]:
            title_element = result.find('h3')
            if title_element:
                title = title_element.text.strip()
                link = result.find('a')['href']
                titles.append(title)
                links.append(link)

        time.sleep(2)

        driver.quit()

        return render_template('index.html', search_term=search_term, titles=titles, links=links, combine_lists=combine_lists, selected_options=selected_options)

    return render_template('index.html')

@app.route('/send_prompt', methods=['POST'])
def send_prompt():
    search_term = request.form["search_term"]
    selected_options = request.form.getlist('selected_options')

    # Define OpenAI API key 
    openai.api_key = "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"

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    prompt = "Bitte lesen Sie die ausgewählten Links sorgfältig durch und generieren Sie einen Titel sowie einen Text von 200 Wörtern basierend auf den Informationen in den Links." + search_term + str(selected_options)

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text

    return render_template('index.html', search_term=search_term, titles=titles, links=links, combine_lists=combine_lists, selected_options=selected_options, response=response)







