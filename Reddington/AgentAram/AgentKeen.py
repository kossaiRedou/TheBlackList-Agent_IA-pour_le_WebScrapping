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
        headless=True,
    )
)

# Génère dynamiquement le prompt
def build_task(category, number, discount):
    return (
        "J'ai un business de vente d'article de catégorie '{category}'."
        f"Va sur https://www.cdiscount.com, accepte les cookies et attends que la page charge complètement. "
        f"Clique sur 'Promo', puis explore les offres dans la catégorie '{category}'. "
        f"Trouve {number} produits qui serrais interessants pour mon business avec une réduction d'au moins {discount}%. "
        "Pour chaque produit, donne : le nom, le prix actuel, le prix avant réduction, le pourcentage de réduction s'il est affiché sinon ne le calcule pas, "
        "une brève description, avantage commercial potentiel pour un business achat-revente, et le lien du produit. "
        "Retourne uniquement un JSON strict comme ceci :\n"
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
