import openai
from utils import obtener_dosis
from api import scrape_food_info
import dotenv   
import os

# Load environment variables
dotenv.load_dotenv()

# APIS
openai.api_key = os.getenv("OPENAI_API_KEY")

def main(user_prompt):

    context_prompt = """
    Vas a calcular la cantidad de carbohidratos de mi comida segun mi nivel de glicemia.
    Voy a decir mi glicemia, luego voy a describir mi comida con lenguaje natural, y tú harás una lista en el siguiente formato de todos los alimentos que te diga:

    Nombre del alimento, Cantidad de alimento, Unidad de medida

    Es importante mantener el formato correcto para poder usar su salida con una API.

    Luego, en la ultima linea, escribe el nivel de glicemia que te dije en numero solamente. Si no lo menciono, pon un 0.

    Ejemplo (solo ejemplo, no utilices estos datos en tu respuesta):

    Si digo: Tengo glicemia de 220, voy a comer una taza de arroz, 2 barras de chocolate quaker, y 20 gramos de choclo.

    Tu output seria:

    Arroz, 1, taza
    Barra de chocolate quaker, 2, unidad
    Choclo, 20, gramos
    220

    """

    context = {"role": "system",
                "content": context_prompt}

    messages = [context]

    messages.append({"role": "user", "content": user_prompt})

    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages)

    content = response.choices[0].message.content
    items = content.splitlines()[:-1]
    glicemia = int(content.splitlines()[-1])

    foods_input = []

    for item in items:
        food = {}
        try:
            item, quantity, measure = item.split(",")
            food["name"] = item.strip()
            food["measurement"] = measure.strip()
            food["quantity"] = int(quantity.strip())
            
            foods_input.append(food)
        except:
            print("Error parsing item " + item)
            continue

    carbs_amount = 0
    
    for food in foods_input:
        food_info = scrape_food_info(food["name"])

        if "gramos" in food["measurement"]:
            if food_info["grams"] is not None:
                food["carbs"] = food_info["carbs"] * food["quantity"] / food_info["grams"]
                food["valid"] = True
            else:
                food["carbs"] = 0
                food["valid"] = False
        else:
            if food_info["units"] is not None:
                food["carbs"] = int(food_info["carbs"] * food["quantity"] / food_info["units"])
                food["measurement"] = food_info["unit_measure"] # update measurement
                food["valid"] = True
            else:
                food["carbs"] = 0
                food["valid"] = False
        
        carbs_amount += food["carbs"]
    
    output = "Lo que vas a comer es: "

    for food in foods_input:
        if food["valid"]:
            output += f"{int(food['quantity'])} {food['measurement']} de {food['name']}, {int(food['carbs'])} carbohidratos, \n "
    
    # Check if there are invalid foods
    all_valid = True
    for food in foods_input:
        if not food["valid"]:
            all_valid = False
            break
    
    if not all_valid:
        output+= "No pude calcular lo siguiente:"

    for food in foods_input:
        if not food["valid"]:
            output += food["name"] + ", "

    output += f"El total de carbohidratos es de: {int(carbs_amount)}."

    output += f"\n Tienes {glicemia} de glicemia, asi que vas a necesitar {obtener_dosis(glicemia, carbs_amount)} unidades de insulina"

    print(output)

    return output

if __name__ == "__main__":
    user_prompt = "Tengo glicemia de 120. Voy a comer 3 naranjas, 1 barra de chocolate quaker y un huevo."
    output = main(user_prompt)
    print(output)

    print("placeholder")