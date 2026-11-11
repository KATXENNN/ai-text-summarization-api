
import sys
from pathlib import Path
from statistics import mean

from rouge_score import rouge_scorer

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.summarizer import summarize_text


# Evaluation dataset: 5 English and 5 French examples
test_cases = [
    # ENGLISH
    {
        "language": "en",
        "topic": "Healthcare",
        "text": (
            "Artificial intelligence is transforming healthcare. Doctors use "
            "intelligent systems to analyze medical images, detect diseases, "
            "and improve diagnosis. These technologies process large amounts "
            "of data quickly. However, they also raise concerns about patient "
            "privacy, data security, and medical responsibility."
        ),
        "reference": (
            "Artificial intelligence helps doctors analyze medical images, "
            "detect diseases, and improve diagnosis. It also raises concerns "
            "about patient privacy, security, and medical responsibility."
        )
    },
    {
        "language": "en",
        "topic": "Education",
        "text": (
            "Technology is changing modern education. Online platforms allow "
            "students to access courses from anywhere. Artificial intelligence "
            "can personalize learning by identifying student weaknesses and "
            "recommending suitable exercises. Teachers can use digital tools "
            "to monitor progress. However, unequal internet access remains "
            "a major challenge for many students."
        ),
        "reference": (
            "Digital platforms and artificial intelligence make education "
            "more accessible and personalized. Teachers can monitor student "
            "progress, but unequal internet access remains a challenge."
        )
    },
    {
        "language": "en",
        "topic": "Technology",
        "text": (
            "Cloud computing allows companies to store data and use software "
            "through the internet instead of maintaining all their own "
            "hardware. It reduces infrastructure costs, supports remote work, "
            "and makes it easier to increase computing capacity. However, "
            "organizations must consider cybersecurity, data privacy, and "
            "dependence on external service providers."
        ),
        "reference": (
            "Cloud computing reduces infrastructure costs and supports "
            "flexible access to digital services. Companies must also "
            "consider cybersecurity, privacy, and provider dependence."
        )
    },
    {
        "language": "en",
        "topic": "Environment",
        "text": (
            "Climate change is increasing global temperatures and causing "
            "more frequent extreme weather events. Governments and businesses "
            "are investing in renewable energy such as solar and wind power. "
            "Energy efficiency, public transportation, and forest protection "
            "can also reduce greenhouse gas emissions. International "
            "cooperation is essential to address this global challenge."
        ),
        "reference": (
            "Climate change increases temperatures and extreme weather. "
            "Renewable energy, efficient transport, and forest protection "
            "can reduce emissions, while international cooperation is essential."
        )
    },
    {
        "language": "en",
        "topic": "Business",
        "text": (
            "E-commerce has changed how businesses sell products and "
            "communicate with customers. Online stores operate continuously "
            "and can reach customers in different countries. Digital payments "
            "and delivery services make purchases more convenient. However, "
            "businesses face competition, cybersecurity risks, and the "
            "challenge of maintaining customer trust."
        ),
        "reference": (
            "E-commerce helps businesses reach customers globally and offers "
            "convenient online purchases. Companies must manage competition, "
            "cybersecurity, and customer trust."
        )
    },

    # FRENCH
    {
        "language": "fr",
        "topic": "Santé",
        "text": (
            "L'intelligence artificielle transforme le secteur de la santé. "
            "Les médecins utilisent des systèmes intelligents pour analyser "
            "les images médicales, détecter des maladies et améliorer les "
            "diagnostics. Ces technologies traitent rapidement de grandes "
            "quantités de données. Cependant, elles soulèvent des questions "
            "sur la confidentialité des patients, la sécurité des données "
            "et la responsabilité médicale."
        ),
        "reference": (
            "L'intelligence artificielle aide les médecins à analyser les "
            "images médicales et à détecter les maladies. Elle soulève aussi "
            "des questions de confidentialité, de sécurité et de responsabilité."
        )
    },
    {
        "language": "fr",
        "topic": "Éducation",
        "text": (
            "Les technologies numériques transforment l'éducation moderne. "
            "Les plateformes en ligne permettent aux étudiants de suivre "
            "des cours à distance. L'intelligence artificielle peut adapter "
            "les exercices aux besoins de chaque apprenant et identifier "
            "ses difficultés. Les enseignants peuvent suivre les progrès "
            "des étudiants grâce aux outils numériques. Toutefois, les "
            "inégalités d'accès à Internet restent un problème important."
        ),
        "reference": (
            "Les plateformes numériques et l'intelligence artificielle "
            "facilitent l'apprentissage personnalisé et à distance. "
            "Cependant, les inégalités d'accès à Internet persistent."
        )
    },
    {
        "language": "fr",
        "topic": "Technologie",
        "text": (
            "Le cloud computing permet aux entreprises de stocker leurs "
            "données et d'utiliser des logiciels sur Internet sans gérer "
            "toute leur infrastructure informatique. Cette solution réduit "
            "les coûts, facilite le travail à distance et permet d'adapter "
            "rapidement les ressources informatiques. Cependant, les "
            "entreprises doivent protéger leurs données et prendre en compte "
            "les risques liés à la cybersécurité et aux fournisseurs externes."
        ),
        "reference": (
            "Le cloud computing réduit les coûts informatiques et facilite "
            "le travail à distance. Les entreprises doivent protéger leurs "
            "données et gérer les risques de cybersécurité."
        )
    },
    {
        "language": "fr",
        "topic": "Environnement",
        "text": (
            "Le changement climatique entraîne une hausse des températures "
            "mondiales et augmente la fréquence des phénomènes météorologiques "
            "extrêmes. Les gouvernements investissent dans les énergies "
            "renouvelables comme le solaire et l'éolien. Les transports "
            "publics, l'efficacité énergétique et la protection des forêts "
            "peuvent également réduire les émissions de gaz à effet de serre. "
            "La coopération internationale reste essentielle."
        ),
        "reference": (
            "Le changement climatique augmente les températures et les "
            "événements extrêmes. Les énergies renouvelables, les transports "
            "publics et la protection des forêts contribuent à réduire les émissions."
        )
    },
    {
        "language": "fr",
        "topic": "Commerce",
        "text": (
            "Le commerce électronique transforme la manière dont les "
            "entreprises vendent leurs produits et communiquent avec leurs "
            "clients. Les boutiques en ligne peuvent fonctionner en permanence "
            "et atteindre des consommateurs dans plusieurs pays. Les paiements "
            "numériques et les services de livraison facilitent les achats. "
            "Cependant, les entreprises doivent faire face à la concurrence, "
            "aux risques de cybersécurité et à la nécessité de maintenir "
            "la confiance des clients."
        ),
        "reference": (
            "Le commerce électronique permet aux entreprises d'atteindre "
            "des clients dans plusieurs pays et facilite les achats. "
            "Les entreprises doivent gérer la concurrence, la sécurité "
            "et la confiance des clients."
        )
    }
]


# Initialize ROUGE scorer
scorer = rouge_scorer.RougeScorer(
    ["rouge1", "rouge2", "rougeL"],
    use_stemmer=False
)

# Store F1 scores for each language
results = {
    "en": {"rouge1": [], "rouge2": [], "rougeL": []},
    "fr": {"rouge1": [], "rouge2": [], "rougeL": []}
}


# Run evaluation
for index, case in enumerate(test_cases, start=1):

    language = case["language"]

    print("\n" + "=" * 60)
    print(f"TEST {index}: {case['topic']} ({language.upper()})")
    print("=" * 60)

    generated_summary = summarize_text(
        text=case["text"],
        max_length=100,
        min_length=30,
        language=language
    )

    print("\nGenerated summary:")
    print(generated_summary)

    print("\nReference summary:")
    print(case["reference"])

    scores = scorer.score(
        case["reference"],
        generated_summary
    )

    print("\nROUGE scores:")

    for metric, score in scores.items():

        f1 = score.fmeasure
        results[language][metric].append(f1)

        print(
            f"{metric.upper()}: "
            f"Precision={score.precision:.4f}, "
            f"Recall={score.recall:.4f}, "
            f"F1={f1:.4f}"
        )


# Calculate average F1 scores
print("\n\n" + "=" * 60)
print("FINAL AVERAGE ROUGE F1 SCORES")
print("=" * 60)

for language in ["en", "fr"]:

    print(f"\n{language.upper()} RESULTS:")

    for metric, values in results[language].items():

        average_score = mean(values)

        print(
            f"{metric.upper()} Average F1: "
            f"{average_score:.4f}"
        )
