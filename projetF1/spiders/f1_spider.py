import scrapy

class F1Spider(scrapy.Spider):
    name = "f1"
    allowed_domains = ["statsf1.com"]
    
    #Liste des pilotes à scraper (ajoute les URL de chaque pilote ici)
    start_urls = [
    "https://www.statsf1.com/fr/alexander-albon.aspx",
    "https://www.statsf1.com/fr/fernando-alonso.aspx",
    "https://www.statsf1.com/fr/andrea-kimi-antonelli.aspx",
    "https://www.statsf1.com/fr/oliver-bearman.aspx",
    "https://www.statsf1.com/fr/gabriel-bortoleto.aspx",
    "https://www.statsf1.com/fr/jack-doohan.aspx",
    "https://www.statsf1.com/fr/pierre-gasly.aspx",
    "https://www.statsf1.com/fr/isack-hadjar.aspx",
    "https://www.statsf1.com/fr/lewis-hamilton.aspx",
    "https://www.statsf1.com/fr/nico-hulkenberg.aspx",
    "https://www.statsf1.com/fr/liam-lawson.aspx",
    "https://www.statsf1.com/fr/charles-leclerc.aspx",
    "https://www.statsf1.com/fr/lando-norris.aspx",
    "https://www.statsf1.com/fr/esteban-ocon.aspx",
    "https://www.statsf1.com/fr/oscar-piastri.aspx",
    "https://www.statsf1.com/fr/george-russell.aspx",
    "https://www.statsf1.com/fr/carlos-sainz.aspx",
    "https://www.statsf1.com/fr/lance-stroll.aspx",
    "https://www.statsf1.com/fr/yuki-tsunoda.aspx",
    "https://www.statsf1.com/fr/max-verstappen.aspx",
]


    def parse(self, response):
        pilot_data = {}

        #Récupérer le nom du pilote
        name = response.css("div.field strong::text").get()
        if name:
            pilot_data["Nom"] = name.strip()

        #Récupérer la date de naissance
        birth_info = response.xpath("//div[@class='field']/text()").getall()
        birth_info = [text.strip() for text in birth_info if "Né le" in text]
        if birth_info:
            pilot_data["Naissance"] = birth_info[0]

        #Récupérer les autres informations (Premier GP, Meilleur Classement, etc.)
        key_values = response.xpath("//div[@class='field']/div[@class='firstbest']/text()").getall()
        values = response.xpath("//div[@class='field']/strong/a/text()").getall()

        for i in range(len(key_values)):
            key = key_values[i].strip().replace(" :", "")
            value = values[i].strip() if i < len(values) else ""
            pilot_data[key] = value


        values = response.xpath("//div[@class='piloteitem']//a/text()").getall()
        # Boucle sur chaque valeur trouvée pour créer une clé dynamique
        for i, value in enumerate(values, start=1):
            key = f"Stat_{i}"  # Générer une clé unique (ex: Stat_1, Stat_2, etc.)
            pilot_data[key] = value.strip()

        print(f"Données du pilote récupérées : {pilot_data}")

        yield pilot_data
