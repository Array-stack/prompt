from flask import Flask, render_template, request
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import sys



app = Flask(__name__)

# Beispielwerte für die Ergebnisse und ausgewählten Optionen
titles = ['Option 1', 'Option 2', 'Option 3']
links = ['#', '#', '#']
selected_options = []

# Benutzerdefinierte Funktion zum Kombinieren von zwei Listen
def combine_lists(a, b):
    return zip(a, b)


@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form["search_term"]
        selected_options = request.form.getlist('selected_options')

    # Beispiel: Drucken Sie den Suchbegriff und die ausgewählten Optionen
        print("Suchbegriff:", search_term)
        print("Ausgewählte Optionen:", selected_options)
        sys.stdout.flush()



        # Pfad zum ChromeDriver
        driver_path = "./chromedriver_win32/chromedriver.exe"
    
        # ChromeDriver-Service erstellen
        service = Service(driver_path)
    
        # Starte den Webdriver
        driver = webdriver.Chrome(service=service)
    
        # Navigiere zur Google-Suche
        driver.get("https://www.google.com")
    
        # Akzeptiere die Cookies, falls das Element vorhanden ist
        try:
            accept_cookies_button = driver.find_element("id", "L2AGLb")
            accept_cookies_button.click()
        except:
            pass
    
        time.sleep(2)
    
        # Suche nach dem Suchfeld und gib den Suchbegriff ein
        search_box = driver.find_element("name", "q")
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
    
        time.sleep(2)
    
        # Extrahiere die Suchergebnisse
        soup = BeautifulSoup(driver.page_source, "html.parser")
        search_results = soup.select('div.g')
    
        # Extrahiere die ersten 5 Suchergebnisse
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
    
        # Schließe den Webdriver
        driver.quit()
    
        return render_template('index.html', search_term=search_term, titles=titles, links=links, combine_lists=combine_lists, selected_options=selected_options)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run()








