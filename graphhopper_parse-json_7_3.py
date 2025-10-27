import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "02b014d8-5ee4-410b-bd36-e58c54e43c12"   


def geocoding(location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        json_data = requests.get(url).json()
        lat = (json_data["hits"][0]["point"]["lat"])
        lng = (json_data["hits"][0]["point"]["lng"])
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country = ""
        
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state = ""
        
        if len(state) != 0 and len(country) != 0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        
        print("URL de la API de geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")\n" + url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status, lat, lng, new_loc


while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Ingrese un perfil de vehículo de la lista anterior: ")
    if vehicle == "salir" or vehicle == "s":
        break
    elif vehicle in profile:
        vehicle = vehicle
    else: 
        vehicle = "car"
        print("No se ingresó un perfil de vehículo válido. Se usará el perfil 'car'.")
    
    loc1 = input("Ubicación de inicio: ")
    if loc1 == "salir" or loc1 == "s":
        break
    orig = geocoding(loc1, key)
    print(orig)
    
    loc2 = input("Destino: ")
    if loc2 == "salir" or loc2 == "s":
        break
    dest = geocoding(loc2, key)
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle, "locale": "es"}) + op + dp
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de enrutamiento: " + str(paths_status) + "\nURL de la API de enrutamiento:\n" + paths_url)
        print("=================================================")
        print("Direcciones desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle)
        print("=================================================")
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61
            km = (paths_data["paths"][0]["distance"]) / 1000
            sec = (paths_data["paths"][0]["time"] / 1000) % 60
            min = (paths_data["paths"][0]["time"] / 1000 / 60) % 60
            hr = (paths_data["paths"][0]["time"] / 1000 / 60 / 60)
            print("Distancia recorrida: {:.2f} millas / {:.2f} km".format(miles, km))
            print("Duración del viaje: {:.2f} horas / {:.2f} minutos / {:.2f} segundos".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.2f} km / {2:.2f} millas )".format(path, distance / 1000, distance / 1000 / 1.61))
            print("=============================================")
        else:
            print("Mensaje de error: " + paths_data["message"])
            print("*************************************************")








