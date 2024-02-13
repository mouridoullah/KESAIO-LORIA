import csv
def process_csv_data(input_file, output_file):
    # Ouvrez le fichier CSV d'entrée
    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        unique_records = {}

        for row in reader:
            row["seismeLabel"] = row["seismeLabel"].replace(" ", "_")
            row["lieuLabel"] = row["lieuLabel"].replace(" ", "_")
            row["paysLabel"] = row["paysLabel"].replace(" ", "_")
            row["description"] = row["description"].replace(" ", "_")

            key = row["seismeLabel"]
            if key not in unique_records:
                unique_records[key] = row

    # Créez un nouveau fichier CSV pour les enregistrements uniques
    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        fieldnames = reader.fieldnames  # Utilisez les mêmes en-têtes de colonnes que le fichier d'origine
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for record in unique_records.values():
            writer.writerow(record)