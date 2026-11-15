import glob
import io
from google.cloud import bigquery

PROJET = "steam-514714"
TABLE = f"{PROJET}.steam.raw_top"

# 1. Coller tous les fichiers JSONL en un seul
contenu = ""

for chemin in sorted(glob.glob("data/*.jsonl")):
    with open(chemin, encoding="utf-8") as fichier:
        contenu += fichier.read()

# 2. Décrire les colonnes de la table
schema = [
    bigquery.SchemaField("date_collecte", "DATE"),
    bigquery.SchemaField("rang", "INTEGER"),
    bigquery.SchemaField("rang_semaine_derniere", "INTEGER"),
    bigquery.SchemaField("appid", "INTEGER"),
    bigquery.SchemaField("nom", "STRING"),
    bigquery.SchemaField("gratuit", "BOOLEAN"),
    bigquery.SchemaField("prix_eur", "FLOAT"),
    bigquery.SchemaField("reduction_pct", "INTEGER"),
    bigquery.SchemaField("genres", "STRING"),
    bigquery.SchemaField("pic_joueurs", "INTEGER"),
]

config = bigquery.LoadJobConfig(
    source_format="NEWLINE_DELIMITED_JSON",
    schema=schema,
    write_disposition="WRITE_TRUNCATE",
)

# 3. Envoyer dans BigQuery (la table est remplacée à chaque fois)
client = bigquery.Client(project=PROJET)
fichier = io.BytesIO(contenu.encode("utf-8"))

tache = client.load_table_from_file(fichier, TABLE, job_config=config)
tache.result()

print("Lignes chargées :", tache.output_rows)
