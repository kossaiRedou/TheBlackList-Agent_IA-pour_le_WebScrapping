import asyncio
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI

# Charger .env une fois
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Préparer le navigateur (1 fois)
browser = Browser(
    config=BrowserConfig(
        chrome_instance_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        headless=False,
    )
)

# Génère dynamiquement le prompt
def build_task(category, number, discount):
    return (
        f"J'ai un site de vente de produits dans la catégorie {category}."
        "Ouvre le lien suivant : https://www.cdiscount.com. "
        "Accepte tous les cookies et attends que la page soit complètement chargée."
        "Recherche et clique sur le bouton Promo."
        f"Défile la page pour voir toutes les promotions intéressantes dans la catégorie {category}."
        f"Suggère-moi uniquement {number} produits ayant une réduction d'au moins {discount}%. "
        "Pour chaque produit, précise : le nom, le prix actuel, le prix avant réduction, le pourcentage de réduction, "
        "la présentation (description), l’avantage commercial potentiel, et le lien vers le produit. "
        "Le résultat doit être retourné au format JSON strict, ne retourne rien d'autre que ce format :\n"
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
        "    }\n"
        "  ]\n"
        "}"
    )


# Fonction asynchrone qui lance l'agent
async def run_agent_task(task):
    agent = Agent(
        llm=ChatOpenAI(model="gpt-4.1", openai_api_key=api_key),
        browser=browser,
        task=task
    )

    history = await agent.run()
    result = history.final_result()



    return result

# Fonction à appeler dans ta vue Django
def launch_reddington_agent(category, number, discount):
    task = build_task(category, number, discount)
    return asyncio.run(run_agent_task(task))
