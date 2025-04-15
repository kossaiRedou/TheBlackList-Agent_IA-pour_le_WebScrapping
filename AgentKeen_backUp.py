from browser_use import Agent, Browser, BrowserConfig
from browser_use import Controller
from langchain_openai import ChatOpenAI
import asyncio
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
from typing import List
from datetime import datetime



#================================================================
# Charge les variables d'environnement du fichier .env
#=====================================================
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")





#=================================================
# Config navigateur
#=============================================
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        #startup_url="https://www.orange.fr/portail",
        headless=False,
    )
)





#========================================================
# Définit une tâche : un promte que j'ai optimiser avec ChatGpt
#=====================================
task = (
    "J'ai un site de vente de produits électroménagers. "
    "Ouvre le lien suivant : https://www.cdiscount.com. "
    "Accepte tous les cookies et attends que la page soit complètement chargée. "
    "Recherche et clique sur le bouton ou lien 'Promo'. "
    "Défile la page pour voir toutes les promotions intéressantes en rapport avec mon business. "
    "Suggère-moi uniquement deux produits électroménagers intéressants que je pourrais acheter et revendre sur mon site, en précisant leur nom, prix, prix avant reduction, reduction appliquer, présentation (description) du produit, avantage commercial potentiel, lien vers le produit."
    "Le résultat doit être retourné au format JSON, ne retourne rien d'autre que le JSON."
    "{\n"
    "  \"products\": [\n"
    "    {\n"
    "      \"name\": \"\",\n"
    "      \"price\": \"\",\n"
    "      \"normal_price\": \"\",\n"
    "      \"discount\": \"\",\n"
    "      \"link\": \"\",\n"
    "      \"description\": \"\",\n"
    "      \"advantage\": \"\"\n"
    "    },\n"
    "    ...\n"
    "  ]\n"
    "}"
)




#===================================================
# Crée l'agent et lui deleguer la tache
#==============================================
agent = Agent(
    llm=ChatOpenAI(model="gpt-4.1", openai_api_key=api_key),
    browser=browser,
    task=task
)




#=================================================
# Préparer l'exécution de l'agent et enregistrer comme une fonction
#===================================
async def run_agent_task():
    history = await agent.run()

    result = history.final_result()
    
    # Ajoute la date/heure actuelle (format lisible)
    date_instant = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construit la structure finale avec timestamp à la racine
    result_dater = {
        "products": result.get("products", []),
        "timestamp": date_instant
    }

    # Écriture dans un fichier JSON unique
    with open("resultata.json", "w", encoding="utf-8") as f:
        json.dump(result_dater, f, indent=2, ensure_ascii=False)


    #retourner le resultat completer avec une date
    return result_dater




#==================================================
# convertir l'agent en fonction python (async)
#=============================================
def launch_agent():
    return asyncio.run(run_agent_task())


