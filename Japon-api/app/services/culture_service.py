from app.schemas.culture import Phrase, EtiquetteRule, DoAndDont, Scenario


PHRASES_DATA = {
    "basico": [
        {
            "japanese": "こんにちは",
            "romaji": "Konnichiwa",
            "translation": "Hola (buenos dias/tardes)",
            "context": "Saludo general durante el dia",
            "pronunciation_tip": "Kohn-nee-chee-wah"
        },
        {
            "japanese": "おはようございます",
            "romaji": "Ohayou gozaimasu",
            "translation": "Buenos dias",
            "context": "Saludo formal por la manana",
            "pronunciation_tip": "Oh-ha-yoh go-zai-mass"
        },
        {
            "japanese": "こんばんは",
            "romaji": "Konbanwa",
            "translation": "Buenas noches",
            "context": "Saludo por la noche",
            "pronunciation_tip": "Kohn-bahn-wah"
        },
        {
            "japanese": "ありがとうございます",
            "romaji": "Arigatou gozaimasu",
            "translation": "Muchas gracias (formal)",
            "context": "Agradecimiento formal, usar con desconocidos",
            "pronunciation_tip": "Ah-ree-gah-toh go-zai-mass"
        },
        {
            "japanese": "すみません",
            "romaji": "Sumimasen",
            "translation": "Perdon / Disculpe",
            "context": "Para disculparse, llamar la atención, o pedir perdón",
            "pronunciation_tip": "Soo-mee-mah-sen"
        },
        {
            "japanese": "はい",
            "romaji": "Hai",
            "translation": "Si",
            "context": "Respuesta afirmativa",
            "pronunciation_tip": "Hi (como la H inglesa)"
        },
        {
            "japanese": "いいえ",
            "romaji": "Iie",
            "translation": "No",
            "context": "Respuesta negativa (usar con cuidado, puede sonar brusco)",
            "pronunciation_tip": "Ee-eh"
        },
        {
            "japanese": "お願いします",
            "romaji": "Onegai shimasu",
            "translation": "Por favor",
            "context": "Pedir algo formalmente",
            "pronunciation_tip": "Oh-neh-gai shee-mass"
        },
        {
            "japanese": "失礼します",
            "romaji": "Shitsurei shimasu",
            "translation": "Disculpe (para irse o interrumpir)",
            "context": "Cuando te vas de un lugar o interrumpes a alguien",
            "pronunciation_tip": "Shee-tsoo-reh shee-mass"
        },
        {
            "japanese": "さようなら",
            "romaji": "Sayounara",
            "translation": "Adios (despedida formal/larga)",
            "context": "Usar cuando no sabes si volveras a ver a la persona",
            "pronunciation_tip": "Sah-yoh-nah-rah"
        }
    ],
    "restaurante": [
        {
            "japanese": "いただきます",
            "romaji": "Itadakimasu",
            "translation": "Buen provecho (expresion de gratitud antes de comer)",
            "context": "SIEMPRE decir antes de empezar a comer",
            "pronunciation_tip": "Ee-tah-dah-kee-mass"
        },
        {
            "japanese": "ごちそうさまでした",
            "romaji": "Gochisousama deshita",
            "translation": "Gracias por la comida (despues de comer)",
            "context": "Decir al terminar de comer, antes de irte",
            "pronunciation_tip": "Go-chee-soh-sah-mah desh-tah"
        },
        {
            "japanese": "メニューをおねがいします",
            "romaji": "Menuu wo onegai shimasu",
            "translation": "El menu, por favor",
            "context": "Para pedir el menu",
            "pronunciation_tip": "Meh-nyoo oh oh-neh-gai shee-mass"
        },
        {
            "japanese": "おすすめはありますか？",
            "romaji": "Osusume wa arimasu ka?",
            "translation": "Tienen alguna recomendacion?",
            "context": "Para pedir recomendaciones",
            "pronunciation_tip": "Oh-soo-soo-meh wah ah-ree-mass kah?"
        },
        {
            "japanese": "これをください",
            "romaji": "Kore wo kudasai",
            "translation": "Quiero esto, por favor",
            "context": "Para pedir algo specifico (senalar en el menu)",
            "pronunciation_tip": "Koh-reh oh koo-dah-sai"
        },
        {
            "japanese": "お会計お願いします",
            "romaji": "Okaikei onegai shimasu",
            "translation": "La cuenta, por favor",
            "context": "Para pedir la cuenta",
            "pronunciation_tip": "Oh-kai-keh oh-neh-gai shee-mass"
        },
        {
            "japanese": "おいしいです",
            "romaji": "Oishii desu",
            "translation": "Esta delicioso",
            "context": "Para halagar la comida",
            "pronunciation_tip": "Oy-shee desu"
        }
    ],
    "compras": [
        {
            "japanese": "いくらですか？",
            "romaji": "Ikura desu ka?",
            "translation": "Cuanto cuesta?",
            "context": "Para preguntar el precio",
            "pronunciation_tip": "Ee-koo-rah desu kah?"
        },
        {
            "japanese": "これをください",
            "romaji": "Kore wo kudasai",
            "translation": "Quiero esto, por favor",
            "context": "Para comprar algo",
            "pronunciation_tip": "Koh-reh oh koo-dah-sai"
        },
        {
            "japanese": "カードで払えますか？",
            "romaji": "Kaado de haraemasu ka?",
            "translation": "Puedo pagar con tarjeta?",
            "context": "Para preguntar si aceptan tarjeta",
            "pronunciation_tip": "Kah-doh deh hah-rah-eh-mass kah?"
        },
        {
            "japanese": "免税できますか？",
            "romaji": "Menzei dekimasu ka?",
            "translation": "Puedo hacer tax-free?",
            "context": "Para pedir exencion de impuestos (compras > 5000 yen)",
            "pronunciation_tip": "Mehn-zeh-ee deh-kee-mass kah?"
        },
        {
            "japanese": "もっと安くなるのはありますか？",
            "romaji": "Motto yasuku naru no wa arimasu ka?",
            "translation": "Hay algun descuento?",
            "context": "Para preguntar por descuentos",
            "pronunciation_tip": "Mohl-toh yah-soo-koo noo noo wah ah-ree-mass kah?"
        }
    ],
    "transporte": [
        {
            "japanese": "すみません、トイレはどこですか？",
            "romaji": "Sumimasen, toire wa doko desu ka?",
            "translation": "Perdon, donde esta el bano?",
            "context": "Para preguntar ubicacion (ej: bano, estacion, salida)",
            "pronunciation_tip": "Soo-mee-mah-sen, toh-ee-reh wah doh koh desu kah?"
        },
        {
            "japanese": "駅はどこですか？",
            "romaji": "Eki wa doko desu ka?",
            "translation": "Donde esta la estacion?",
            "context": "Para encontrar la estacion de tren",
            "pronunciation_tip": "Eh-kee wah doh koh desu kah?"
        },
        {
            "japanese": "この電車は東京に行きますか？",
            "romaji": "Kono densha wa Tokyo ni ikimasu ka?",
            "translation": "Este tren va a Tokio?",
            "context": "Para confirmar la direccion del tren (cambia Tokyo por tu destino)",
            "pronunciation_tip": "Koh-noh dehn-shah wah Toh-kyoh nee ee-kee-mass kah?"
        },
        {
            "japanese": "どちらが近いですか？",
            "romaji": "Docchi ga chikai desu ka?",
            "translation": "Cual es mas cercano?",
            "context": "Para comparar rutas",
            "pronunciation_tip": "Doh-chee gah chee-kai desu kah?"
        },
        {
            "japanese": "タクシーを呼んでください",
            "romaji": "Takushii wo yonde kudasai",
            "translation": "Llame un taxi, por favor",
            "context": "Para pedir un taxi",
            "pronunciation_tip": "Tah-koo-shee oh yohn-deh koo-dah-sai"
        }
    ],
    "hotel": [
        {
            "japanese": "予約があります",
            "romaji": "Yoyaku ga arimasu",
            "translation": "Tengo una reservacion",
            "context": "Para hacer check-in",
            "pronunciation_tip": "Yoh-yah-koo gah ah-ree-mass"
        },
        {
            "japanese": "チェックインお願いします",
            "romaji": "Chekku-in onegai shimasu",
            "translation": "Check-in, por favor",
            "context": "Para registrarse en el hotel",
            "pronunciation_tip": "Cheh-koo-in oh-neh-gai shee-mass"
        },
        {
            "japanese": "WiFiのパスワードは？",
            "romaji": "Waifai no pasuwaado wa?",
            "translation": "Cual es el password del WiFi?",
            "context": "Para pedir el WiFi",
            "pronunciation_tip": "Wai-fai no pah-soo-wah-doh wah?"
        },
        {
            "japanese": "朝食は何時からですか？",
            "romaji": "Choushoku wa nanji kara desu ka?",
            "translation": "A que hora es el desayuno?",
            "context": "Para preguntar por el desayuno",
            "pronunciation_tip": "Choh-shoh-koo wah nan-jee kah-rah desu kah?"
        }
    ],
    "emergencia": [
        {
            "japanese": "助けてください！",
            "romaji": "Tasukete kudasai!",
            "translation": "Ayuda, por favor!",
            "context": "Para pedir ayuda urgente",
            "pronunciation_tip": "Tah-soo-keh-teh koo-dah-sai!"
        },
        {
            "japanese": "警察を呼んでください",
            "romaji": "Keisatsu wo yonde kudasai",
            "translation": "Llame a la policia, por favor",
            "context": "Para emergencias policiales",
            "pronunciation_tip": "Kay-sah-tsoo oh yohn-deh koo-dah-sai"
        },
        {
            "japanese": "病院に行きたいです",
            "romaji": "Byouin ni ikitai desu",
            "translation": "Quiero ir al hospital",
            "context": "Para emergencias medicas",
            "pronunciation_tip": "Byoh-in nee ee-kee-tai desu"
        },
        {
            "japanese": "水土産病です",
            "romaji": "Suido-san byou desu",
            "translation": "Tengo diarrea del viajero",
            "context": "Para describir malestar estomacal comun",
            "pronunciation_tip": "Swee-doh-sahn byoh desu"
        },
        {
            "japanese": "アレルギーがあります",
            "romaji": "Arerugii ga arimasu",
            "translation": "Tengo una alergia",
            "context": "Para informar sobre alergias alimentarias",
            "pronunciation_tip": "Ah-reh-roo-gee gah ah-ree-mass"
        }
    ]
}

ETIQUETTE_DATA = [
    {
        "category": "zapatos",
        "title": "Quitar zapatos al entrar",
        "description": "En casas, restaurantes tradicionales, templos y algunos hoteles debes quitar los zapatos. Usa los pantuflas que te proporcionan.",
        "importance": "alta",
        "tip": "Usa calcetines sin agujeros! Los japoneses lo consideran de mala educacion."
    },
    {
        "category": "comida",
        "title": "Palillos: nunca los claves verticalmente",
        "description": "Clavar palillos en el arroz recuerda a los funerales. Nunca los pases de palillo a palillo.",
        "importance": "alta",
        "tip": "Deja los palillos sobre el soporte cuando no los uses."
    },
    {
        "category": "comida",
        "title": "Bebida: sirve a los demas primero",
        "description": "En grupo, sirve la bebida de otros antes que la tuya. Ellos haran lo mismo por ti.",
        "importance": "media",
        "tip": "Sostén la botella con ambas manos al servir."
    },
    {
        "category": "transporte",
        "title": "No hablar en el tren",
        "description": "En trenes y autobuses, el telefono debe estar en modo silencio y no se debe hablar. Los japoneses duermen o leen.",
        "importance": "alta",
        "tip": "Si debes atender una llamada, baja la voz y cubre el microfono."
    },
    {
        "category": "baño",
        "title": "Uso del inodoro",
        "description": "Los inodoros japoneses tienen many botones. No te asustes! Los mas comunes son: enjuague, limpieza, y secado.",
        "importance": "media",
        "tip": "El boton rojo es para emergencias. Los demas son para funciones del inodoro."
    },
    {
        "category": "social",
        "title": "No propinas",
        "description": "En Japon no se da propina. De hecho, puede ser considerado ofensivo. El servicio ya esta incluido.",
        "importance": "alta",
        "tip": "Simplemente di 'arigatou gozaimasu' al irte."
    },
    {
        "category": "templo",
        "title": "Respeto en templos y santuarios",
        "description": "Quita el sombrero, habla bajo, no corras. En los santuarios, haz una reverencia antes de entrar.",
        "importance": "alta",
        "tip": "Sigue a los locales para saber que hacer."
    },
    {
        "category": "banio",
        "title": "Limpiarte los zapatos",
        "description": "Antes de entrar a un baño publico, hay un area para limpiarte los zapatos. Dejalo limpio para el siguiente.",
        "importance": "media",
        "tip": "Los banos publicos son gratis y muy limpios."
    },
    {
        "category": "onzen",
        "title": "Baños termales (Onsen)",
        "description": "Debes entrar completamente desnudo. No se permite tatuajes en muchos onsen. Lava tu cuerpo antes de entrar al agua.",
        "importance": "alta",
        "tip": "Los tatuajes estan asociados con yakuza. Algunos onsen los aceptan, otros no."
    },
    {
        "category": "basura",
        "title": "No hay papelera en la calle",
        "description": "Japon no tiene papelera en la calle. Guarda tu basura y tirala en tu hotel o en las estaciones de tren.",
        "importance": "media",
        "tip": "Lleva una bolsa pequeña para tu basura."
    }
]

DO_DONT_DATA = [
    {
        "category": "comida",
        "do": [
            "Decir 'itadakimasu' antes de comer",
            "Decir 'gochisousama' despues de comer",
            "Probar todo lo que te ofrezcan",
            "Usar palillos para comer",
            "Comer en el orden que te sirvan"
        ],
        "dont": [
            "Clavar palillos verticalmente en el arroz",
            "Pasar comida de palillo a palillo",
            "Soplar sopa fria (el ramen se come con ruidito)",
            "Poner salsa de soja en el arroz",
            "Levantar los platos del suelo para comer"
        ]
    },
    {
        "category": "social",
        "do": [
            "Hacer una leve reverencia al saludar",
            "Dar y recibir cosas con ambas manos",
            " quits los zapatos al entrar",
            "Ser puntual (los trenes salen al segundo)",
            "Agradecer siempre"
        ],
        "dont": [
            "Dar propina (se considera ofensivo)",
            "Tocar a la gente (ni abrazos ni besos)",
            "Hablar en voz alta en publico",
            "Comer caminando",
            "Mandar textos mientras caminas"
        ]
    },
    {
        "category": "transporte",
        "do": [
            "Esperar a que bajen los pasajeros antes de subir",
            "Usar la escalera mecánica (izquierda en Tokyo, derecha en Osaka)",
            "Hacer fila ordenadamente",
            "Pagar con tarjeta o efectivo exacto",
            "Descargar la app de trenes"
        ],
        "dont": [
            "Hablar en el tren",
            "Comer en el tren (excepto trenes bala)",
            "Ocupar los asientos reservados",
            "Dormirse y perder tu parada",
            "Subir al tren con maletas grandes en hora pico"
        ]
    }
]

SCENARIOS_DATA = [
    {
        "id": "llegada-aeropuerto",
        "title": "Llegada al Aeropuerto",
        "description": "Primeras frases al llegar a Japon",
        "phrases": PHRASES_DATA["basico"][:3] + PHRASES_DATA["transporte"][:2],
        "etiquette_rules": [r for r in ETIQUETTE_DATA if r["category"] in ["transporte", "social"]][:3]
    },
    {
        "id": "restaurante-ramen",
        "title": "En un Restaurante de Ramen",
        "description": "Como ordenar y comportarte en un ramen shop",
        "phrases": PHRASES_DATA["restaurante"],
        "etiquette_rules": [r for r in ETIQUETTE_DATA if r["category"] == "comida"]
    },
    {
        "id": "tienda-conveniencia",
        "title": "En una Tienda de Conveniencia",
        "description": "7-Eleven, FamilyMart, Lawson",
        "phrases": PHRASES_DATA["compras"][:3],
        "etiquette_rules": [r for r in ETIQUETTE_DATA if r["category"] in ["social", "compras"]][:2]
    },
    {
        "id": "templo-santuario",
        "title": "Visita a un Templo/Santuario",
        "description": "Como comportarte en lugares sagrados",
        "phrases": PHRASES_DATA["social"] if "social" in PHRASES_DATA else PHRASES_DATA["basico"][:2],
        "etiquette_rules": [r for r in ETIQUETTE_DATA if r["category"] in ["templo", "social"]]
    },
    {
        "id": "emergencia-medica",
        "title": "Emergencia Medica",
        "description": "Que hacer si necesitas atencion medica",
        "phrases": PHRASES_DATA["emergencia"],
        "etiquette_rules": [r for r in ETIQUETTE_DATA if r["category"] in ["emergencia"]]
    }
]


def get_phrases(category: str = None, language: str = "es") -> list[dict]:
    if category and category in PHRASES_DATA:
        return PHRASES_DATA[category]
    return [p for phrases in PHRASES_DATA.values() for p in phrases]


def get_etiquette(category: str = None) -> list[dict]:
    if category:
        return [r for r in ETIQUETTE_DATA if r["category"] == category]
    return ETIQUETTE_DATA


def get_do_and_dont(category: str = None) -> list[dict]:
    if category:
        return [d for d in DO_DONT_DATA if d["category"] == category]
    return DO_DONT_DATA


def get_scenario(scenario_id: str) -> dict | None:
    for s in SCENARIOS_DATA:
        if s["id"] == scenario_id:
            return s
    return None


def get_all_scenarios() -> list[dict]:
    return SCENARIOS_DATA
