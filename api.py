from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_measure_info(measure):
    grams = None
    units = None
    unit_measure = None

    if "(" in measure:
        grams = int(measure[measure.find("(")+1:measure.find("g")])
        units = int(measure[0:measure.find(" ")].strip())
        unit_measure = measure[measure.find(" ")+1:measure.find("(")].strip()
    elif " " not in measure:
        grams = int(measure[0:measure.find("g")])
        unit_measure = f"unidades de {str(grams)} gramos"
        units = 1
    else:
        units = int(measure[0:measure.find(" ")].strip())
        unit_measure = measure[measure.find(" ")+1:].strip()
    
    return unit_measure, units, grams
    
def scrape_food_info(search, result_id =0):
    # Get and parse url
    search = search.replace(" ", "%20")
    # Sacar los acentos
    search = search.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u")

    url = f"https://www.fatsecret.cl/calor%C3%ADas-nutrici%C3%B3n/search?q={search}"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    # Get search results
    results = soup.find(class_="generic searchResult")
    results_list =results.find_all("tr")

    first_result = results_list[result_id]
    name = first_result.find("a").text

    info_card =  first_result.find(class_ = "smallText greyText greyLink").text.split("|")

    measure = info_card[0].strip().split("-")[0].strip()
    index = measure.find('por')
    measure = measure[index+4:]

    unit_measure, units, grams = get_measure_info(measure)

    carbs = int(float(info_card[2].split(":")[1].strip().replace("g", "").replace(",", ".")))

    food_info = {}

    food_info["name"] = name
    food_info["carbs"] = carbs
    food_info["units"] = units
    food_info["grams"] = grams
    food_info["unit_measure"] = unit_measure

    return food_info

if __name__ == '__main__':
    print(scrape_food_info("pan perfecto"))