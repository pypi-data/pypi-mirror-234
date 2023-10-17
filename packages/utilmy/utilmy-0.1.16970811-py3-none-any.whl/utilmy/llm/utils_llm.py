"""

https://github.com/Qustelm/Phind-api/blob/main/phindai.py




"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')


def get_completion(info:str=""):
    global driver
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.phind.com/")
    script = """
        return fetch("https://www.phind.com/api/agent", {
            credentials: "include",
            headers: {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "Accept": "*/*",
                "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                "Content-Type": "application/json",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin"
            },\n"""
    
    script += f'referrer: "https://www.phind.com/agent?q={info}&source=searchbox",\n'
    script += 'body: JSON.stringify({userInput: "'+info+'", messages: [], shouldRunGPT4: false}),\n'        
    script += """
            method: "POST",
            mode: "cors"
        })
        .then(response => response.text())
        .then(data => data)
        .catch(error => console.error(error));
    """
    
    result = driver.execute_script(script)
    result = result.replace("\n", "").split("data:")
    stroke = []

    driver.quit()

    if "<!DOCTYPE html>" in result[0]:
        return "ERROR"
        return
    
    for i in range(len(result)):
        try:
            x = json.loads(result[i])["choices"][0]["delta"]["content"]
            if type(x) == str:
                stroke.append(x)
        except:
            pass
    return ''.join(stroke)



if __name__ == "__main__":
    import fire 
    fire.Fire()







