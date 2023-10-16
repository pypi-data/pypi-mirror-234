from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

system_info = """Given the email of the user, give one or two standalone questions that summarize the client need.
Generate in the same language as the client's email."""

STANDALONE_QUESTION_PROMPT = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_info),
            HumanMessage(content=f'''Mail : Bonjour,  J'aimerais recevoir mes factures papiers par mail ou poste. Auparavant je recois par voie postale mes factures que je règle immédiatement. Sur mon espace je constate un retard de paiement pour lequel je n'ai aucune facture. Sur mon espace je ne parviens pas à recupérer cette facture . Pouvez-vous me la transmettre par mail darif70@hotmail.com afin que je paies de suite. Dans cette attente. Bien cordialement.<br/><br/>  Ann
            Question : '''),
            AIMessage(content="""Pouvez-vous m'envoyer les factures par la poste dorénavant ?\nJe ne trouve pas ma facture impayée pouvez-vous me l'envoyer par la poste ?"""),
            HumanMessage(content=f'''Mail : J'aimerais passer d'un tarif bi-horaire à un tarif mono-horaire de jour, et garder le même compteur. A quel service, doit je faire la demande?<br/><br/>  An\n
            Question : '''),
            AIMessage(content="""Comment passez à un tarif mono-horraire de jour sans changer de compteur ?"""),
            HumanMessage(content=f'''Mail : Bonjour, je viens de souscrire un contrat de introduisant l'EAN communiqué par mon propriétaire, à savoir 541448965000411895. Le contrat ouvert par Engue me propose une adresse 55 fritz Toussaint A20 qui ne correspond pas à la nôtre,  soit 53 Fritz Toussaint A12... Pourriez-vous m'indiquer s'il s'agit bien du même compteur? Le propriétaire était monsieur Siperius...<br/><br/>  Ans\n
            Question : '''),
            AIMessage(content="""Pouvez-vous vérifier que le compteur à l'adresse 53 Fritz Toussaint A12 a bien l'EAN 541448965000411895?\nPouvez-vous changer l'adresse sur le contrat ?"""),
            HumanMessagePromptTemplate.from_template('''Mail : {input}\n
            Question : ''')  
        ])