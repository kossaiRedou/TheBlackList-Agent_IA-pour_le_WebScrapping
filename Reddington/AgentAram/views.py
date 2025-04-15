from django.shortcuts import render
from AgentAram.forms import PromoForm
from AgentAram.AgentKeen import launch_reddington_agent
from .models import ScrapedProduct 
from django.core.mail import send_mail
import json
from datetime import datetime

# fonction d'envoi de mail
def envoyer_resultat_par_mail(result):
    subject = "Résultats du scraping (Agent Reddington)"
    message = f"Bonjour,\n\nVoici les résultats du scraping :\n\n{result}\n\nBonne journée."
    from_email = None  # utilise DEFAULT_FROM_EMAIL de settings
    recipient_list = ['aliou@gabithex.fr']

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )





def index(request):
    if request.method == 'POST':
        form = PromoForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['product_category']
            number = form.cleaned_data['number_of_articles']
            discount = form.cleaned_data['discount_threshold']

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            result = launch_reddington_agent(category, number, discount)

            # Envoi par e-mail
            envoyer_resultat_par_mail(result)
            
            # convertit en dictionnaire
            if isinstance(result, str):
                result = json.loads(result)
                
            
            # Stocke le résultat dans la session (pour l'afficher dans la vue resultats)
            request.session['last_result'] = result
                
                
            # Enregistrement des produits en BDD
            for item in result["products"]:
                ScrapedProduct.objects.create(
                    name=item["name"],
                    price=item["price"],
                    normal_price=item["normal_price"],
                    discount=item["discount"],
                    link=item["link"],
                    description=item["description"],
                    advantage=item["advantage"],
                    category=category  # depuis le formulaire
                )

            return render(request, 'AgentAram/resultats.html', {'result': result, 'timestamp':timestamp})

    else:
        form = PromoForm()
    return render(request, 'AgentAram//index.html', {'form': form})




def resultats(request):
    """
    Vue qui affiche le résultat de la dernière analyse.
    Le résultat est récupéré depuis la session.
    """
    # On récupère le résultat stocké dans la session par la vue index
    result = request.session.get('last_result', None)
    if not result:
        result = {"timestamp": "", "products": []}
    return render(request, 'AgentAram/resultats.html', {'result': result})


def historique(request):
    """
    Vue qui affiche l'historique complet des produits enregistrés en base,
    triés du plus récent au plus ancien.
    """
    produits = ScrapedProduct.objects.all().order_by('-timestamp')
    return render(request, 'AgentAram/historique.html', {'produits': produits})