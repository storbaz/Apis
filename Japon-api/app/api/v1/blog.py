from fastapi import APIRouter
from datetime import datetime
from typing import Optional
import random

router = APIRouter(prefix="/blog", tags=["blog"])

BLOG_POOL = [
    {
        "slug": "curiosidades-japón-que-no-conocías",
        "title": "15 Curiosidades de Japón que No Conocías",
        "description": "Japón es un país lleno de tradiciones únicas, costumbres sorprendentes y datos fascinantes. Descubre cosas que solo existen en Japón.",
        "category": "Curiosidades",
        "readTime": "6 min",
        "tags": ["curiosidades japón", "datos japón", "tradiciones japonesas", "cosas raras japón"],
        "content": """
## 1. Hay más de 1,500 terremotos al año

Japón se encuentra en el Cinturón de Fuego del Pacífico. La mayoría son micro-terremotos que no sientes, pero el país tiene uno de los mejores sistemas de alerta del mundo.

## 2. Los_ascensores tienen música

Cada ascensor en Japón tiene una melodía única para indicar en qué piso estás. Las estaciones de tren también tienen jingles personalizados.

## 3. El vendedor de karaoke más del mundo

Japón tiene más de 100,000 salas de karaoke. Es la actividad social número uno después del trabajo.

## 4. Los vagones de tren son silenciosos

En los trenes de Tokio hay vagones "silenciosos" donde no se puede hablar por teléfono ni conversar en voz alta.

## 5. Comida que parece arte

Los bento japoneses son obras de arte comestible. Las madres dedican horas a crear diseños kawaii (bonitos) para los almuerzos de sus hijos.

## 6. Los templos cambian de color

Durante el otoño, los 2,000+ templos de Kioto se pintan de rojo, naranja y dorado. Es como si la ciudad entera se transformara.

## 7. Existe un festival del sollozo

El Hadaka Matsuri (Festival Desnudo) en Okayama tiene a 10,000 hombres compitiendo por palillos sagrados. Se celebra en pleno invierno.

## 8. Los konbini son mini ciudades

7-Eleven en Japón no es una tienda normal. Puedes pagar facturas, recargar tu tarjeta de tren, imprimir documentos y hasta enviar paquetes.

## 9. El tren más rápido del mundo

El Shinkansen de Hokkaido alcanza 320 km/h y tiene un historial de puntualidad de 0.09 minutos de retraso promedio.

## 10. Los japoneses duermen poco

La jornada laboral promedio es de 10+ horas, pero la cultura del "inemuri" (dormir en público) es completamente aceptada. Puedes ver gente durmiendo en estaciones de tren.

## 11. Hay más de 100,000 festivales al año

Japón tiene un matsuri (festival) casi cada día del año. Desde el Nebuta Matsuri en Aomori hasta el Gion Matsuri en Kioto.

## 12. El ramen tiene su propio instituto

El Ramen Museum de Yokohama recrea Tokio de 1958 y tiene las mejores sopas de ramen de todo el país.

## 13. Los baños termales son sagrados

Los onsen tienen reglas estrictas: te lavas completamente antes de entrar, no puedes meter la toalla al agua, y hay separación por género.

## 14. Japón tiene 6,800 islas

Solo 430 están habitadas. Las islas de Okinawa tienen una cultura completamente diferente al resto del país.

## 15. La propina es un insulto

En Japón, dar propina es grosero. Significa que la persona necesita caridad. El servicio es perfecto sin propina.

---
**Descubre más curiosidades en ViajApp**: Nuestra app tiene guías culturales detalladas para que entiendas cada tradición antes de llegar.
"""
    },
    {
        "slug": "temporada-cerezas-guia-completa",
        "title": "Temporada de Cerezas en Japón: Guía Completa 2026",
        "description": "Todo lo que necesitas saber para disfrutar los sakura en Japón: fechas, mejores lugares, dónde dormir y cómo evitar multitudes.",
        "category": "Planificación",
        "readTime": "8 min",
        "tags": ["cerezas japón", "sakura 2026", "hanami", "primavera japón"],
        "content": """
## ¿Cuándo florecen los cerezos?

La temporada de sakura comienza en Okinawa a finales de enero y llega a Tokio entre finales de marzo y principios de abril. Kioto sigue poco después.

### Fechas aproximadas 2026:
- **Okinawa**: Enero-Febrero
- **Fukuoka**: 25 Marzo
- **Osaka**: 28 Marzo
- **Kioto**: 29 Marzo
- **Tokio**: 27 Marzo
- **Hakone**: 1 Abril

## Los mejores lugares para ver sakura

### Tokio
- **Ueno Park**: El más famoso, pero también el más concurrido. Llega antes de las 8am.
- **Shinjuku Gyoen**: 65 hectáreas de jardines. Perfecto para picnic.
- **Meguro River**: 800 cerezos a ambos lados del río. Espectacular de noche.
- **Chidorigafuchi**: Alquilar un bote y remar entre pétalos.

### Kioto
- **Maruyama Park**: El cerezo centenario iluminado de noche es mágico.
- **Arashiyama**: El bosque de bambú + cerezos = foto perfecta.
- **Tofuku-ji**: El puente Tsutenkyo con valle de cerezos abajo.
- **Filosofía del Camino**: Caminar bajo los cerezos entre templos.

### Osaka
- **Osaka Castle**: El castillo rodeado de 3,000 cerezos es impresionante.
- **Kema Sakuranomiya Park**: 4.2 km de cerezos a orillas del río.

## Cómo planificar tu viaje

1. **Reserva con 3-6 meses de antelación**: Los hoteles se llenan y los precios suben 50-100%.
2. **Usa el Japan Meteorological Corporation**: Dan pronósticos de floración con semanas de antelación.
3. **Visita entre semana**: Los fines de semana están abarrotados.
4. **Lleva manta para picnic**: La tradición del hanami es sentarse bajo un cerezo a comer y beber.
5. **Prueba los snacks de sakura**: Daifuku de sakura, helado de sakura, cerveza de sakura.

## El hanami: tradición de picnic bajo los cerezos

El hanami (花見) es la tradición de celebrar la floración de los cerezos. Las familias y amigos se reúnen con mantas, bento y sake bajo los árboles.

**Tip**: Llega temprano para reservar un buen spot. En parques populares como Ueno, la gente llega a las 6am.

## Después de los sakura: el "sakura fubuki"

Cuando los pétalos caen, crean un efecto de "nieve rosa" llamado sakura fubuki. Es igual de fotogénico que los árboles en flor.

---
**Planifica tu viaje con ViajApp**: Nuestra app tiene mapa interactivo de sakura con fechas de floración en tiempo real.
"""
    },
    {
        "slug": "guia-transporte-japon",
        "title": "Guía de Transporte en Japón: Todo lo que Necesitas Saber",
        "description": "Desde el JR Pass hasta el metro de Tokio. Aprende a moverte por Japón como un local con esta guía completa de transporte.",
        "category": "Guías",
        "readTime": "7 min",
        "tags": ["transporte japón", "JR Pass", "metro tokio", "shinkansen"],
        "content": """
## JR Pass: ¿Vale la pena?

El JR Pass de 7 días cuesta ~50,000 yenes. Solo conviene si vas a hacer:
- Tokio → Kioto → Osaka (ida y vuelta = ~26,000¥ cada viaje)
- Cualquier viaje de más de 3 horas en Shinkansen

**Si solo vas a estar en Tokio**: Compra una Suica o Pasmo card y paga por viaje.

## Metro de Tokio

El metro de Tokio tiene 13 líneas y es el más complejo del mundo. Pero es fácil de usar:

1. **Compra una Suica o Pasmo** en cualquier estación (500¥ depósito + recarga)
2. **Usa Google Maps**: Te dice exactamente qué línea tomar y a qué hora sale
3. **Evita las horas pico**: 7:30-9:30am y 5:30-8:00pm

### Precios por viaje:
- Dentro de la zona central: 170-230¥
- Hasta la periferia: 300-500¥

## Shinkansen (tren bala)

Velocidad máxima: 320 km/h. Puntualidad: promedio de 0.09 minutos de retraso.

### Rutas principales:
- **Tokio → Kioto**: 2h 15min, ~13,000¥
- **Tokio → Osaka**: 2h 30min, ~14,000¥
- **Kioto → Hiroshima**: 1h 40min, ~11,000¥

**Tip**: Reserva asiento en la ventanilla del lado de la montaña (oeste) para ver el Monte Fuji.

## Buses nocturnos

Willer Express opera buses nocturnos desde 2,000¥. Ahorras hotel y transporte. Durmiendo llegas a tu destino.

## Bicicleta

Muchas ciudades tienen sistemas de alquiler de bicicletas. Kioto es perfecto en bici: plano, bonito y con poco tráfico en ciertas zonas.

## Taxis

Los taxis son caros pero útiles para equipaje pesado o late night. El metro cierra a medianocho.

---
**Usa ViajApp para planificar tu ruta**: Nuestra app calcula la mejor ruta y el costo de transporte entre ciudades.
"""
    },
    {
        "slug": "comida-callejera-japon",
        "title": "Comida Callejera en Japón: Los Mejores Street Food",
        "description": "Japón no es solo sushi y ramen. Descubre la increíble comida callejera que encontrarás en mercados y festivales.",
        "category": "Comida",
        "readTime": "6 min",
        "tags": ["street food japón", "comida callejera", "mercados japón", "yatai"],
        "content": """
## Los mercados imprescindibles

### Mercado de Tsukiji (Tokio)
El mercado más famoso del mundo. Aunque el mercado mayorista se movió, el mercado exterior sigue vibrante.

**Prueba**: Tamagoyaki (tortilla japonesa), ostras gigantes, matcha de los mejores.

### Mercado de Nishiki (Kioto)
"La cocina de Kioto". 400+ tiendas en 5 cuadras. Todo fresco y local.

**Prueba**: Tsukemono (encurtidos), tofu fresco, dulces tradicionales.

### Mercado de Kuromon (Osaka)
El mercado de los mariscos. Pueden comer langostinos, erizos de mar y pescado crudo recién preparado.

## Street food clásico

### Takoyaki (Osaka)
Bolas de masa rellenas de pulpo. Crujientes por fuera, suaves por dentro. ~500¥ por 8 piezas.

### Okonomiyaki (Osaka)
"Tortilla japonesa". Mezcla de masa, col, cerdo y salsas. Se cocina frente a ti en una plancha.

### Yakitori
Brochetas de pollo a la parrilla. Perfectas con cerveza. 100-200¥ por brocheta.

### Taiyaki
Pastel en forma de pez relleno de anko (pasta de frijol rojo). Caliente y dulce.

### Ikayaki
Calamar entero asado. Común en festivales de verano.

## Yatai: puestos de comida móvil

En Fukuoka, los yatai son puestos de comida callejera que aparecen por la noche. Sirven ramen, yakitori y gyoza. Son una experiencia única.

## Temporadas de festivales

En verano, los matsuri tienen puestos de comida: okonomiyaki, yakisoba, helado de matcha, kakigori (hielo raspado con sirope).

---
**Encuentra los mejores mercados en ViajApp**: Nuestra app tiene mapa interactivo con todos los mercados y puestos de comida.
"""
    },
    {
        "slug": "etiqueta-japonesa-errores-comunes",
        "title": "Etiqueta en Japón: 12 Errores que los Turistas Cometen",
        "description": "Japón tiene reglas sociales no escritas. Evita estos errores comunes para no ser el turista incómodo que nadie quiere cerca.",
        "category": "Consejos",
        "readTime": "5 min",
        "tags": ["etiqueta japón", "errores turistas", "cultura japonesa", "modales"],
        "content": """
## En restaurantes

### 1. No des propina
En Japón, la propina es un insulto. El servicio es perfecto sin ella. Si dejas propina, te la devolverán pensando que cometiste un error.

### 2. No cruces los palillos en el plato
Cruzar palillos en forma de X simboliza la muerte. Siéntalos en el soporte o en el plato en paralelo.

### 3. No pases comida de palillo a palillo
Esto se hace en funerales. Usa la parte limpia de tus palillos o pide un plato extra.

## En templos y santuarios

### 4. No camines por el centro del pasillo
En los santuarios, el camino central es para los dioses. Camina por los lados.

### 5. No toques las estatuas
Muchas estatuas tienen poderes sagrados. No las toques, especialmente las de animales.

### 6. No saques fotos donde está prohibido
Algunos templos no permiten fotos del interior. Respeta las señales.

## En el transporte

### 7. No comas en el metro
Excepto en los trenes de larga distancia (Shinkansen), no se come ni se bebe en el metro.

### 8. No hables por teléfono
En el metro, pon el teléfono en modo silencio y no hables. Si debes contestar, habla muy bajo.

### 9. No reserves asientos que no vayas a usar
Los asientos reservados son para personas mayores, embarazadas o con discapacidad.

## En baños y onsen

### 10. No metas la toalla en el agua del onsen
La toalla va en la cabeza o en el suelo. Nunca dentro del agua termal.

### 11. No te laves en la tina
El agua de la tina es para relajarse. Te lavas en las duchas antes de entrar.

## En la calle

### 12. No comas caminando
En Japón se come sentado. Comer caminando se considera grosero (excepto en festivales).

---
**ViajApp te prepara**: Nuestra sección de cultura tiene toda la información para que viajes como un local.
"""
    },
    {
        "slug": "mejores-onsen-japon",
        "title": "Los Mejores Onsen de Japón: Baños Termales Imperdibles",
        "description": "Los onsen son la experiencia más relajante de Japón. Descubre cuáles visitar y cómo disfrutarlos como un local.",
        "category": "Guias",
        "readTime": "7 min",
        "tags": ["onsen japón", "baños termales", "relajación japon", "ryokan"],
        "content": """
## ¿Qué es un onsen?

Un onsen (温泉) es un baño termal natural. Japón tiene más de 27,000 fuentes termales. La tradición tiene más de 1,000 años.

## Los mejores onsen

### Hakone (cerca de Tokio)
A 90 minutos de Tokio. Onsen con vistas al Monte Fuji. Hay ryokans (posadas tradicionales) con onsen privados.

**Recomendado**: Hakone Yuryo o Tenzan Tohji-kyo

### Kinosaki Onsen (cerca de Kioto)
Pueblo termal con 7 baños públicos. Pasear con yukata (bata ligera) de un baño a otro es la experiencia.

### Beppu (Kyushu)
La capital termal de Japón. Tiene baños de arena, baños de barro y hasta un baño de demonios (Jigoku Mud).

### Kurokawa Onsen (Kyushu)
Pueblo tradicional rodeado de bosque. Los ryokans tienen onsen privados al aire libre.

### Noboribetsu (Hokkaido)
El "valle del infierno" con vapor saliendo de la tierra. El Jigokudani es impresionante.

## Cómo disfrutar un onsen

1. **Desnúdate completamente**: No hay baños internos en la cultura tradicional
2. **Lávate antes de entrar**: Hay duchas y jabón en la entrada
3. **No metas la toalla en el agua**: Ponla en la cabeza o en el suelo
4. **Relájate**: No es un baño rápido. Tómate tu tiempo
5. **Hidrátate**: Bebe agua después del baño

## Onsen con tatuajes

Antes, los onsen prohibían personas con tatuajes (asociación con yakuza). Ahora muchos aceptan, pero verifica antes.

**Tip**: Algunos ryokans tienen onsen privados donde puedes bañarte sin problemas.

## Ryokan: la experiencia completa

Un ryokan es una posada tradicional japonesa. Incluye:
- Habitación con futón en tatami
- Cena y desayuno kaiseki (platos tradicionales)
- Acceso al onsen
- Yukata para usar durante la estancia

**Precio**: Desde 15,000¥ por noche hasta 50,000¥+ en ryokans de lujo.

---
**Encuentra onsen en ViajApp**: Nuestra app tiene mapa de onsen con filtros por tipo, precio y accesibilidad.
"""
    },
    {
        "slug": "tokyo-oculto-lugares-secretos",
        "title": "Tokio Oculto: 10 Lugares Secretos que los Turistas No Conocen",
        "description": "Más allá de Shibuya y Shinjuku, Tokio tiene tesoros escondidos. Descubre los lugares que solo conocen los locales.",
        "category": "Curiosidades",
        "readTime": "6 min",
        "tags": ["tokio oculto", "lugares secretos tokio", "off the beaten path", "tokio local"],
        "content": """
## 1. Yanaka Ginza (barrio de gatos)

Un pueblo antiguo atrapado en medio de la ciudad moderna. Calles estrechas, tiendas tradicionales y gatos por todas partes. Es como viajar 50 años al pasado.

**Cómo llegar**: Estación Nippori, línea Yamanote

## 2. Nezu Shrine (santuario de las torii)

Similar al Fushimi Inari de Kioto pero sin multitudes. Un pasillo de torii rojas que serpentear por una colina verde.

**Tip**: Ve en semana para evitar multitudes

## 3. Golden Gai (barrio de bares)

200+ bares en 6 callejuelas. Cada bar tiene capacidad para 6-10 personas. La mayoría cobran 500-1,000¥ de entrada por las bebidas.

**Tip**: Algunos bares tienen reglas (solo japoneses, solo fumadores). Mira las señales antes de entrar.

## 4. Shimokitazawa (barrio bohemio)

El barrio indie de Tokio. Teatros, tiendas de segunda mano, cafés con encanto y escena musical underground.

## 5. Meguro River (río de los cerezos)

4 km de cerezos a ambos lados. En primavera es mágico. Fuera de temporada es un paseo tranquilo con cafés y tiendas.

## 6. Omoide Yokocho (callejón de los recuerdos)

Callejón de puestos de yakitori y ramen desde los años 40. Humo, gente y olores. La verdadera Tokio.

## 7. Kagurazaka (barrio francés)

Calles empedradas con restaurantes franceses y japoneses. Un cruce cultural único. Los martes hay mercado francés.

## 8. Ueno Park de noche

El parque es bonito de día, pero de noche los templos iluminados son espectaculares. Pocos turistas.

## 9. Tokyo Station subterráneo

La estación tiene pasillos subterráneos con tiendas de lujo y restaurantes que la mayoría ignora.

## 10. Koenji (barrio vintage)

El centro de la contracultura tokita. Tiendas de ropa vintage, bares de rock y una escena LGBTQ+ vibrante.

---
**Descubre más con ViajApp**: Nuestra app tiene mapa de lugares ocultos en Tokio, actualizado por locales.
"""
    },
    {
        "slug": "presupuesto-viaje-japon-10-dias",
        "title": "Presupuesto Realista: Viaje a Japón de 10 Días",
        "description": "¿Cuánto cuesta realmente viajar a Japón? Desglose realista con precios de 2026 para diferentes estilos de viaje.",
        "category": "Ahorro",
        "readTime": "6 min",
        "tags": ["presupuesto japon", "cuanto cuesta japon", "viaje barato japon", "coste vida japon"],
        "content": """
## Viaje Económico: 80,000-120,000¥ (500-750€)

### Alojamiento (10 noches): 30,000-40,000¥
- Hostels: 2,500-4,000¥/noche
- Cápsulas: 3,000-5,000¥/noche
- Airbnb compartido: 3,000-5,000¥/noche

### Comida (10 días): 25,000-35,000¥
- Desayuno en konbini: 300-500¥
- Almuerzo: 800-1,200¥
- Cena: 1,000-2,000¥
- Snacks: 500¥

### Transporte: 20,000-30,000¥
- JR Pass 7 días: 50,000¥ (si lo necesitas)
- Metro de Tokio: 500-800¥/día
- Trenes locales: 200-500¥ por viaje

### Actividades: 5,000-10,000¥
- Templos gratuitos: 0¥
- Templos de pago: 500-2,000¥ cada uno
- Experiencias: 3,000-5,000¥

## Viaje Medio: 150,000-200,000¥ (950-1,250€)

### Alojamiento: 60,000-80,000¥
- Hoteles económicos: 6,000-8,000¥/noche
- Ryokan 1 noche: 15,000-25,000¥

### Comida: 40,000-50,000¥
- Restaurantes variados
- 1-2 comidas premium

### Transporte: 30,000-40,000¥
- JR Pass + metro
- Algún taxi

### Actividades: 15,000-20,000¥
- Experiencias guiadas
- Talleres de cocina
- Karaoke nocturno

## Viaje Premium: 300,000+¥ (1,900€+)

### Alojamiento: 150,000+¥
- Hoteles de lujo: 20,000-50,000¥/noche
- Ryokan de lujo: 40,000-80,000¥/noche

### Comida: 80,000+¥
- Restaurantes con estrella Michelin
- Wagyu premium
- Sushi omakase

### Transporte: 50,000+¥
- JR Pass Green (primera clase)
- Taxis privados

### Actividades: 30,000+¥
- Tours privados
- Experiencias exclusivas

## Tips para ahorrar

1. **Come en konbini**: 30-40% de tu presupuesto de comida
2. **Usa buses nocturnos**: Ahorras hotel
3. **Templos gratuitos**: Hay cientos
4. **100-yen shops**: Souvenirs baratos
5. **Almuerza en vez de cenar**: Los lunch sets son más baratos

---
**Calcula tu presupuesto en ViajApp**: Nuestra herramienta de presupuesto te da un desglose personalizado según tu estilo de viaje.
"""
    },
    {
        "slug": "fiestas-tradicionales-japon",
        "title": "Las 8 Fiestas Tradicionales de Japón que Debes Vivir",
        "description": "Los matsuri son la esencia cultural de Japón. Estas son las fiestas más impresionantes que no puedes perderte.",
        "category": "Cultura",
        "readTime": "7 min",
        "tags": ["matsuri japón", "fiestas japonesas", "festivales japon", "cultura japonesa"],
        "content": """
## 1. Gion Matsuri (Kioto) - Julio

El festival más famoso de Japón. Dura todo julio con desfiles de carrozas gigantes llamadas "yamahoko". La noche del yoiyama (16 julio) las calles se llenan de gente, comida y faroles.

**Tip**: Ve la noche anterior para evitar la multitud del día principal.

## 2. Nebuta Matsuri (Aomori) - Agosto

Carrozas gigantes de papel iluminadas con escenas de guerreros y dioses. La gente baila y grita "Rassera! Rassera!" por las calles.

Espectacular y único. Los turistas pueden unirse al desfile.

## 3. Tanabata Matsuri (Sendai) - Agosto

El Festival de las Estrellas. Las calles se cuelgan con papel decorations llamadas "tanzaku" con deseos escritos. Miles de colores.

## 4. Awa Odori (Tokushima) - Agosto

El festival de baile más grande de Japón. 1.3 millones de personas bailan en las calles con trajes tradicionales. La frase es: "Los tontos bailan y los que no miran son más tontos".

## 5. Sapporo Snow Festival - Febrero

Esculturas de nieve y hielo gigantes. Algunas tienen 15 metros de altura. Iluminadas de noche son mágicas.

## 6. Hakata Gion Yamakasa (Fukuoka) - Julio

Hombres corriendo con carrozas de 1 tonelada por las calles. Velocidad increíble. El último día (24 julio) es una carrera a muerte.

## 7. Tenjin Matsuri (Osaka) - Julio

Uno de los tres festivales más importantes de Japón. Procesión fluvial con barcos iluminados en el río Okawa.

## 8. Kanamara Matsuri (Kawasaki) - Abril

El festival de la fertilidad. Sí, es exactamente lo que parece. Carrozas con forma fáfica. Divertido y culturalmente fascinante.

---
**Planea tu matsuri con ViajApp**: Nuestra app tiene calendario de festivales con fechas exactas y ubicaciones.
"""
    },
    {
        "slug": "japones-basico-guia-practica",
        "title": "Japonés Básico: Guía Práctica para Viajeros",
        "description": "No necesitas dominar el japonés. Con estas 20 frases y palabras clave, podrás comunicarte en cualquier situación de viaje.",
        "category": "Idioma",
        "readTime": "5 min",
        "tags": ["japonés básico", "frases japones", "aprender japonés", "comunicación japon"],
        "content": """
## Saludos esenciales

- **Konnichiwa** (こんにちは) - Hola (día)
- **Ohayou gozaimasu** (おはようございます) - Buenos días
- **Konbanwa** (こんばんは) - Buenas tardes
- **Sayounara** (さようなら) - Adiós (permanente)
- **Ja ne** (じゃあね) - Hasta luego (casual)

## Agradecimiento y cortesía

- **Arigatou gozaimasu** (ありがとうございます) - Muchas gracias (formal)
- **Sumimasen** (すみません) - Disculpe / Perdón (el más útil)
- **Gomen nasai** (ごめんなさい) - Lo siento
- **Onegai shimasu** (お願いします) - Por favor

## En restaurantes

- **Kore wo kudasai** (これをください) - Este, por favor (señalando)
- **Oishii** (おいしい) - Delicioso
- **Okaikei onegaishimasu** (お会計お願いします) - La cuenta, por favor
- **Tabemasen** (食べません) - No como esto
- **Biiru hitotsu** (ビール一つ) - Una cerveza

## Números útiles

- **Hitotsu** (一つ) - Uno
- **Futatsu** (二つ) - Dos
- **Ikura desu ka?** (いくらですか) - ¿Cuánto cuesta?
- **Takai** (高い) - Caro
- **Yasui** (安い) - Barato

## Emergencias

- **Tasukete** (助けて) - Ayuda
- **Keisatsu** (警察) - Policía
- **Byouin** (病院) - Hospital
- **Benjo** (便所) - Baño (¡muy útil!)

## La frase mágica

**Wakarimasen** (わかりません) - No entiendo. Con una sonrisa, esto abre puertas.

---
**Usa el traductor de ViajApp**: Nuestra app tiene traductor de voz en tiempo real para comunicarte sin barreras.
"""
    },
    {
        "slug": "islas-secretas-japon",
        "title": "Islas Secretas de Japón: 5 Destinos Fuera del Mapa Turístico",
        "description": "Más allá de Tokio y Kioto, Japón tiene islas paradisíacas que pocos turistas conocen. Descubre paraísos ocultos.",
        "category": "Curiosidades",
        "readTime": "6 min",
        "tags": ["islas japón", "destinos secretos", "off the beaten path", "islas paradisíacas"],
        "content": """
## 1. Yakushima (Kyushu)

Una isla cubierta de bosque primordial con árboles de 3,000+ años. La inspiración para la película "El Viaje de Chihiro" de Miyazaki.

**Qué ver**: Bosque de cedros gigantes, monos de cola blanca, playas vírgenes.

**Cómo llegar**: Ferry desde Kagoshima (2h) o avión (35 min).

## 2. Naoshima (Mar Interior)

La isla del arte. Museos de arte contemporáneo enterrados en la tierra, esculturas de Yayoi Kusama y pueblos de pescadores.

**Qué ver**: Chichu Art Museum, Yayoi Kusama's Yellow Pumpkin, Benesse House.

## 3. Okinawa (sur de Japón)

Cultura completamente diferente. Playas de arena blanca, arrecifes de coral y una historia de reino independiente.

**Qué ver**: Shuri Castle, playas de Kerama, museo de la paz de Hiroshima (cerca).

## 4. Sado Island (Mar de Japón)

Isla minera con tradición de música taiko. Los prisioneros políticos fueron exiliados aquí durante siglos.

**Qué ver**: Minas de oro, playas de conchas, danza de tambores Sado.

## 5. Iriomote Island (Okinawa)

90% cubierta de selva subtropical. El último hábitat del gato montés de Iriomote, en peligro de extinción.

**Qué ver**: Manglares, río Nagura, snorkel en arrecifes.

---
**Explora las islas con ViajApp**: Nuestra app tiene guías completas de todas las islas de Japón con rutas y consejos.
"""
    },
    {
        "slug": "japon-nocturno-guia-completa",
        "title": "Japón de Noche: La Guía Completa para Disfrutar After Dark",
        "description": "Cuando el sol se pone, Japón cobra vida de otra manera. Desde bares de karaoke hasta mercados nocturnos.",
        "category": "Guias",
        "readTime": "7 min",
        "tags": ["vida nocturna japon", "karaoke", "bares tokio", "noche japon"],
        "content": """
## Tokio after dark

### Golden Gai (Shinjuku)
200+ bares diminutos. Cada uno tiene personalidad única: jazz, manga, punk rock, cine. La mayoría cobran 500-1,000¥ de entrada.

### Shibuya
El cruce más famoso del mundo iluminado de neón. Para después:-bars en Shibuya Center-gai o en Miyashita Park.

### Roppongi
El barrio internacional. Bares, discotecas y restaurantes abiertos hasta tarde. Para turistas y expats.

## Izakaya: la experiencia japonesa

Una izakaya es un bar-restaurante donde pides pequeños platos para compartir con bebidas. Es donde los japoneses van después del trabajo.

**Qué pedir**: Yakitori, edamame, karaage, sashimi, cerveza o sake.

**Precios**: 2,000-4,000¥ por persona con bebidas.

## Karaoke

La actividad nacional. Salas privadas donde cantas lo que quieras. Hay canciones en inglés, español y muchos idiomas.

**Precios**: 500-2,000¥/hora por persona. Bebidas ilimitadas por 1,000-2,000¥/hora.

**Mejores cadenas**: Big Echo, Joysound, Karaoke Kan.

## Mercados nocturnos

### Ameya Yokocho (Tokio)
Mercado callejero que abre hasta tarde. Comida, ropa y souvenirs.

### Yatai de Fukuoka
Puestos de comida callejera a orillas del río. Ramen, yakitori y gyoza.

## Taxis nocturnos

El metro cierra a medianocho. Los taxis son la opción después de las 12am. No son baratos (1,500-3,000¥ por trayecto corto) pero son seguros.

---
**Planifica tu noche con ViajApp**: Nuestra app tiene mapa de bares, izakayas y karaoke abiertos hasta tarde.
"""
    },
    {
        "slug": "arte-ikebana-japones",
        "title": "Ikebana: El Arte Floral de Japón que Debes Conocer",
        "description": "Ikebana no es solo arreglar flores. Es una filosofía, una meditación y una conexión con la naturaleza. Descubre este arte milenario.",
        "category": "Cultura",
        "readTime": "5 min",
        "tags": ["ikebana", "arte japonés", "flores japonesas", "cultura japonesa"],
        "content": """
## ¿Qué es el ikebana?

Ikebana (生け花) significa "dar vida a las flores". Es el arte japonés de arreglar flores que data del siglo VII. Más que decoración, es una forma de meditación y conexión con la naturaleza.

## Filosofía detrás del arte

El ikebana se basa en tres principios:
- **Shin** (真): Cielo o verdad
- **Soe** (副): Hombre o soporte
- **Hikae** (控): Tierra o base

Cada arreglo representa la armonía entre cielo, tierra y hombre.

## Las escuelas principales

### Ikenobo (池坊)
La escuela más antigua (500+ años). Estilos clásicos y formales.

### Ohara (小原)
Introdujo el uso de flores occidentales. Estilo más natural y moderno.

### Misho-ryu (未生流)
Enfocado en la simplicidad y la espiritualidad.

## Arreglos populares

### Moribana (盛花)
Arreglo en un plato poco profundo con pinches de metal (kenzan). Es el estilo más común hoy.

### Nageire (投入)
Arreglo en un florero alto. Las flores se colocan naturalmente, sin kenzan.

### Shoka (生花)
Estilo clásico con tres ramas principales que representan cielo, tierra y hombre.

## Aprender ikebana

En Japón hay escuelas que ofrecen clases para turistas (1,000-3,000¥ por sesión). Es una actividad perfecta para una tarde tranquila.

**Tip**: En Kioto, Manyo Club ofrece clases de ikebana con traducción al inglés.

---
**Aprende ikebana con ViajApp**: Nuestra app tiene guías de actividades culturales, incluyendo clases de ikebana en las principales ciudades.
"""
    },
    {
        "slug": "japones-para-trabajar-guia",
        "title": "Cómo Trabajar en Japón: Guía para Nómadas Digitales",
        "description": "Japón es ideal para nómadas digitales: café, wifi rápido, seguridad y cultura de trabajo. Descubre cómo vivir y trabajar en Japón.",
        "category": "Guías",
        "readTime": "7 min",
        "tags": ["nómada digital japon", "trabajar japón", "coworking tokio", "vida japón"],
        "content": """
## Visa para nómadas digitales

Japón lanzó la visa "Digital Nomad" en 2024. Requisitos:
- Ingresos de más de 10 millones de yen/año (~65,000€)
- Seguro médico privado
- Estancia máxima: 6 meses

## Los mejores coworkings

### Tokio
- **Andwork**: Red de espacios en toda la ciudad
- **Basis Point**: Múltiples ubicaciones, ambiente internacional
- **WeWork**: Estándar internacional

### Kioto
- **The Notch**: Coworking boutique en machiya tradicional
- **Kioto International Community House**: Gratis para extranjeros

### Osaka
- **Namba Parks**: Coworking con vistas
- **Basis Point Namba**: Económico y bien equipado

## Café para trabajar

Japón tiene cafés excelentes con wifi gratuito:
- **Doutor**: Cadena grande, wifi estable
- **Tully's Coffee**: Cómodo para sesiones largas
- **Starbucks Reserve**: Experiencia premium

**Tip**: Muchos cafés cierran temprano (7-8pm). Los manga cafés están abiertos 24h.

## Coste de vida

### Tokio
- Alojamiento: 80,000-120,000¥/mes
- Comida: 40,000-60,000¥/mes
- Transporte: 10,000-15,000¥/mes
- **Total**: 130,000-195,000¥/mes (820-1,230€)

### Kioto
- Alojamiento: 60,000-90,000¥/mes
- Comida: 35,000-50,000¥/mes
- Transporte: 8,000-12,000¥/mes
- **Total**: 103,000-152,000¥/mes (650-960€)

## WiFi y conectividad

- **eSIM**: 2,000-3,000¥/mes por 10GB
- **Pocket WiFi**: 500-1,000¥/día
- **WiFi público**: Gratis en estaciones, konbini y parques

## Consejos para nómadas

1. **Aprende japonés básico**: Los locales aprecian el esfuerzo
2. **Respeta la cultura de trabajo**: Los japoneses son muy disciplinados
3. **Usa los onsen después de trabajar**: La mejor relajación
4. **Come en konbini**: Ahorra tiempo y dinero

---
**Vive y trabaja en Japón con ViajApp**: Nuestra app tiene guías de coworkings, cafés y consejos para nómadas digitales.
"""
    },
    {
        "slug": "comida-kaiseki-arte-culinario",
        "title": "Kaiseki: El Arte Culinario Más Elegante de Japón",
        "description": "El kaiseki es la alta cocina japonesa. Cada plato es una obra de arte que combina sabor, textura y presentación.",
        "category": "Comida",
        "readTime": "6 min",
        "tags": ["kaiseki", "alta cocina japonesa", "gastronomía japon", "restaurante japon"],
        "content": """
## ¿Qué es el kaiseki?

Kaiseki (懐石) es la tradición gastronómica más refinada de Japón. Una cena kaiseki tiene 7-14 platos, cada uno preparado con ingredientes de temporada y presentación impecable.

## La filosofía

- **Shun** (旬): Ingredientes en su punto óptimo de temporada
- **Moritsuke** (盛り付け): Arte de presentación en el plato
- **Omiase** (お見せ): Cada plato se presenta y explica

## Estructura de una cena kaiseki

1. **Sakizuke**: Aperitivo ligero
2. **Hassun**: Mar y tierra en armonía
3. **Mukozuke**: Sashimi de temporada
4. **Yakimono**: Plato a la parrilla
5. **Takiawase**: Verduras cocinadas
6. **Gohan**: Arroz de temporada
7. **Kō no mono**: Encurtidos
8. **Tome-wan**: Sopa ligera
9. **Mizumono**: Postre

## Los mejores lugares

### Tokio
- **Kohaku**: 3 estrellas Michelin. Kaiseki moderno.
- **Ishikawa**: 3 estrellas. Tradición y innovación.

### Kioto
- **Kikunoi**: 3 estrellas. El kaiseki más tradicional.
- **Hyotei**: 3 estrellas. Dentro de un jardín de té.

### Osaka
- **Koryu**: 2 estrellas. Kaiseki accesible.

## Precio

- **Económico**: 8,000-15,000¥ por persona
- **Medio**: 15,000-30,000¥
- **Lujo**: 30,000-80,000¥+

## Reservar

La mayoría de restaurantes kaiseki requieren reserva con semanas o meses de antelación. Muchos solo aceptan clientes referidos por hoteles.

**Tip**: Algunos ryokans incluyen cena kaiseki en el precio.

---
**Encuentra kaiseki en ViajApp**: Nuestra app tiene directorio de restaurantes kaiseki con información de reserva y precios.
"""
    },
    {
        "slug": "japón-con-niños-guia-familiar",
        "title": "Viajar a Japón con Niños: Guía Familiar Completa",
        "description": "Japón es uno de los países más seguros y amigables con niños del mundo. Descubre cómo planificar el viaje perfecto en familia.",
        "category": "Guías",
        "readTime": "7 min",
        "tags": ["japón con niños", "viaje familiar", "niños en japon", "familia japón"],
        "content": """
## ¿Por qué Japón con niños?

1. **Seguridad**: Los niños pueden caminar solos desde los 5 años
2. **Limpieza**: Calles impecables, baños limpios en todas partes
3. **Amabilidad**: Los locales adoran a los niños
4. **Comida**: Los niños japoneses comen de todo
5. **Transporte**: Fácil y puntual

## Edades ideales

- **0-3 años**: Si el niño viaja en cochecito, Japón es accesible
- **4-8 años**: Edad perfecta para DisneySea y acuarios
- **9-12 años**: Pueden caminar más y disfrutar templos
- **13+ años**: Ya pueden participar en todas las actividades

## Planificación por edades

### Niños pequeños (0-5)
- **DisneySea**: Tiene atracciones para toda la familia
- **Acuario de Okinawa**: El más grande de Asia
- **Parques**: Shinjuku Gyoen, Ueno Park

### Niños medios (6-10)
- **TeamLab Borderless**: Arte digital interactivo
- **Robot Restaurant**: Show robotizado (no apto para sensibles)
- **Tren bala**: Los niños están fascinados

### Niños grandes (11-15)
- **Akihabara**: Videojuegos y manga
- **Karaoke**: Diversión familiar
- **Senderismo**: Monte Fuji (con guía)

## Logística práctica

### Equipaje
- Trae un cochecito plegable ligeras
- Muchos hoteles tienen cunas gratuitas
- Las konbini tienen pañales y comida para bebés

### Comida
- Los niños japoneses comen arroz, fideos, pescado
- En McDonald's hay Happy Meals locales (teriyaki burger)
- Las konbini tienen onigiri que a todos les gustan

### Transporte
- Los niños menores de 6 años viajan gratis en trenes
- Hay asientos familiares en el metro
- Los autobuses tienen espacio para cochecitos

## Destinos familiares

1. **Tokio**: Disney, acuarios, parques
2. **Osaka**: Universal Studios, aquarium
3. **Kioto**: Templos + bamboo grove (paseos cortos)
4. **Okinawa**: Playas + acuario

---
**Planifica tu viaje familiar con ViajApp**: Nuestra app tiene filtros para familias con niños y recomendaciones por edad.
"""
    },
    {
        "slug": "mercadostokio-guia-completa",
        "title": "Los 7 Mejores Mercados de Tokio que Debes Visitar",
        "description": "Los mercados de Tokio son mundos de sabores, colores y tradiciones. Descubre cuáles son los imprescindibles y qué probar en cada uno.",
        "category": "Comida",
        "readTime": "6 min",
        "tags": ["mercados tokio", "mercados japón", "comida tokio", "shopping tokio"],
        "content": """
## 1. Tsukiji Outer Market

El más famoso del mundo. Aunque el mercado mayorista se mudó, el exterior sigue vibrante.

**Qué probar**: Tamagoyaki (tortilla), ostras gigantes, matcha, fruta fresca.

**Horario**: 5am-2pm (cierra temprano)

## 2. Ameya Yokocho (Ameyoko)

Mercado callejero bajo las vías del tren. Ropa, comida, cosméticos y souvenirs a precios de ganga.

**Qué probar**: Fruta fresca, pescado, snacks japoneses.

## 3. Nishiki Market (Kioto)

"La cocina de Kioto". 400+ tiendas en 5 cuadras. Todo fresco y tradicional.

**Qué probar**: Tsukemono (encurtidos), tofu, dulces de matcha.

## 4. Kuromon Market (Osaka)

"La cocina de Osaka". Mercado de mariscos donde puedes comer langostinos recién preparados.

**Qué probar**: Sashimi, langostinos, erizo de mar.

## 5. Omoide Yokocho (Shinjuku)

"Callejón de los recuerdos". Puestos de yakitori y ramen desde los años 40.

**Qué probar**: Yakitori, ramen, gyoza.

## 6. Yanaka Ginza

Pueblo antiguo con gatos callejeros. Tiendas tradicionales y snacks locales.

**Qué probar**: Croquetas, dango, helado artesanal.

## 7. Nakamise-dori (Asakusa)

Calle de souvenirs frente al templo Sensoji. Artesanías tradicionales y snacks.

**Qué probar**: Ningyo-yaki (pasteles con forma de muñeca), senbei (galletas de arroz).

---
**Navega los mercados con ViajApp**: Nuestra app tiene mapa interactivo con horarios y qué probar en cada mercado.
"""
    },
    {
        "slug": "japón-verde-naturaleza",
        "title": "Japón Verde: 8 Destinos Naturales que No Son Solo Templos",
        "description": "Japón tiene montañas, bosques, cascadas y playas espectaculares. Descubre la naturaleza que pocos turistas conocen.",
        "category": "Curiosidades",
        "readTime": "6 min",
        "tags": ["naturaleza japon", "senderismo japon", "montañas japón", "playas japon"],
        "content": """
## 1. Monte Fuji

El volcán más icónico de Japón. La temporada de escalada es julio-agosto. La vista del amanecer desde la cima (goraiko) es mística.

**Tip**: Empieza la subida por la noche para llegar al amanecer.

## 2. Valle de Kamikochi (Alpes japoneses)

Valle glaciar con montañas nevadas, ríos cristalinos y bosques de abedules. Senderismo para todos los niveles.

**Temporada**: Abril-Noviembre (cerrado en invierno)

## 3. Bosque de bambú de Arashiyama (Kioto)

Un bosque de bambú gigantes que te hace sentir en otro planeta. La luz que se filtra entre los tallos es mágica.

**Tip**: Ve temprano (antes de las 8am) para evitar multitudes.

## 4. Monte Koya (Koyasan)

Monte sagrado del budismo shingon. Hay templos que ofrecen alojamiento (shukubo). La experiencia es espiritual.

**Qué ver**: Cementerio Okunoin (el más grande de Japón), templos, onsen.

## 5. Iya Valley (Shikoku)

Valle remoto con puentes de liana, casas en acantilados y ríos turquesa. Uno de los lugares menos turísticos de Japón.

**Qué hacer**: Puente de Kazurabashi, kayak, onsen rural.

## 6. Jigokudani (Nagano)

El valle del "infierno" donde los monos japoneses se bañan en onsen. Una foto icónica de Japón.

**Tip**: Los monos están más activos en invierno cuando hay nieve.

## 7. Isla de Miyajima (Hiroshima)

La isla del torii flotante. Templos, ciervos salvajes y vistas al mar Interior.

**Qué ver**: Torii de Itsukushima, Monte Misen, templo Daishoin.

## 8. Bosque de Aokigahara (Monte Fuji)

Bosque denso al pie del Fuji. Senderismo entre árboles gigantes y formaciones de lava.

**Tip**: Hay senderos marcados. No te apartes del camino.

---
**Explora la naturaleza con ViajApp**: Nuestra app tiene mapa de senderismo con dificultad, duración y puntos de interés.
"""
    },
    {
        "slug": "shibuya-shinjuku-guia-barrios",
        "title": "Shibuya vs Shinjuku: ¿Qué Barrio Elegir en Tokio?",
        "description": "Shibuya y Shinjuku son los barrios más famosos de Tokio. Cada uno tiene personalidad única. Descubre cuál es mejor para ti.",
        "category": "Guias",
        "readTime": "6 min",
        "tags": ["shibuya", "shinjuku", "barrios tokio", "guía tokio"],
        "content": """
## Shibuya: El corazón moderno

### Personalidad
Joven, trendy, energético. Es el centro de la moda y la cultura pop japonesa.

### Qué ver
- **Cruce de Shibuya**: El más famoso del mundo. 3,000 personas cruzando a la vez.
- **Hachiko Statue**: El perro más fiel del mundo.
- **Shibuya Sky**: Vistas panorámicas desde el piso 46.
- **Center-gai**: Calle principal con tiendas y restaurantes.

### Para quién es
- Amantes de la moda y el streetwear
- Quiere vida nocturna joven
- Fan de la cultura pop japonesa

### Mejores restaurantes
- **Ichiran Ramen**: Ramen tonkotsu en cabinas privadas
- **Afuri**: Ramen de limón ligero
- **Nonbei Yokocho**: Callejón de bares tradicionales

## Shinjuku: El coloso urbano

### Personalidad
Caótico, diverso, infinito. Es el barrio más grande y con más opciones de Tokio.

### Qué ver
- **Estación Shinjuku**: La estación más grande del mundo (200+ salidas)
- **Kabukicho**: Barrio rojo / entretenimiento nocturno
- **Golden Gai**: 200+ bares diminutos
- **Omoide Yokocho**: Yakitori y ramen callejero
- **Tokyo Metropolitan Government**: Vistas gratis

### Para quién es
- Quiere opciones infinitas
- Amante de la vida nocturna
- Foodie que quiere variedad

### Mejores restaurantes
- **Fuunji**: Los mejores tsukemen de Tokio
- **Omoide Yokocho**: Yakitori callejero
- **Tsunahachi**: Tempura desde 1924

## ¿Cuál elegir?

| Característica | Shibuya | Shinjuku |
|----------------|---------|----------|
| Ambiente | Joven, trendy | Diverso, caótico |
| Compras | Fashion | Todo tipo |
| Noche | Discotecas | Bares, izakayas |
| Comida | Tendencia | Tradicional + moderna |
| Alojamiento | Más caro | Más opciones |

**Tip**: ¡No elijas! Los dos están a 5 minutos en tren.

---
**Navega Tokio con ViajApp**: Nuestra app tiene mapa detallado de cada barrio con restaurantes, tiendas y atracciones.
"""
    },
    {
        "slug": "vending-machines-mas-raras-japon",
        "title": "Las Vending Machines Más Raras de Japón",
        "description": "Japón tiene más de 5 millones de vending machines, y algunas son absolutamente increíbles. Desde comida viva hasta ropa interior.",
        "category": "Freaky",
        "readTime": "5 min",
        "tags": ["vending machines japón", "máquinas japón", "cosas raras japón", "japón freaky"],
        "content": """
## ¿Por qué Japón tiene tantas vending machines?

Japón tiene más de 5 millones de vending machines (una por cada 23 personas). Es el segundo país del mundo en densidad de máquinas automáticas.

La razón: mano de obra cara + alta demanda + cultura de conveniencia.

## Las más raras

### 1. Vending Machine de Insectos Fritos
En Akihabara puedes comprar grillos, escarabajos y gusanos fritos. Son crujientes y ricos en proteínas.
**Precio**: 500-1,000 yenes

### 2. Vending Machine de Ropa Interior Usada
Sí, existe. En Akihabara hay máquinas que venden ropa interior. Algunas son nuevas, otras... usadas.
**Precio**: 1,000-5,000 yenes

### 3. Vending Machine de Comida Caliente
Máquinas que sirven ramen, takoyaki, gyoza y curry. Todo caliente en 60 segundos.
**Precio**: 300-800 yenes

### 4. Vending Machine de Cangrejos Vivos
En el aeropuerto de Narita puedes comprar cangrejos vivos para llevar a casa.
**Precio**: 3,000-5,000 yenes

### 5. Vending Machine de Bebidas Calientes y Frías
Esta es normal en Japón, pero fuera del país es raro. La misma máquina tiene bebidas calientes (café, té) y frías (refrescos, agua).

### 6. Vending Machine de Flores
En estaciones de tren hay máquinas que venden ramos de flores frescas. Perfecto para un regalo de última hora.
**Precio**: 500-2,000 yenes

### 7. Vending Machine de Bolsas de Sangre
En hospitales y clínicas. Para donantes de sangre, dan bolsas de café o jugo.
**Gratis** (como agradecimiento)

### 8. Vending Machine de Arroz Caliente
Ensupermercados y estaciones. Arroz recién cocido en tazón.
**Precio**: 200-400 yenes

### 9. Vending Machine de Helados Extraños
Sabor de wasabi, salsa de soja, sake, matcha, y hasta... queso.
**Precio**: 200-500 yenes

### 10. Vending Machine de Artículos de Emergencia
Después de terremotos, estas máquinas se abren y regalan agua y comida gratis.

---
**Encuentra vending machines en ViajApp**: Nuestra app tiene mapa interactivo con ubicaciones de vending machines únicas.
"""
    },
    {
        "slug": "maid-cafe-guia-completa",
        "title": "Maid Cafés en Japón: Guía Completa para No Perderte",
        "description": "Los maid cafés son la experiencia más representativa de la cultura otaku. Descubre cómo funcionan, cuáles visitar y qué esperar.",
        "category": "Freaky",
        "readTime": "6 min",
        "tags": ["maid cafe", "akihabara", "otaku japan", "japón freaky"],
        "content": """
## ¿Qué es un Maid Café?

Un maid café (メイドカフェ) es un restaurante temático donde las camareras vestidas de maid (sirvienta) te atienden con un estilo kawaii (lindo). Inventado en Akihabara en 2001, ahora hay cientos en todo Japón.

## Cómo funciona

1. **Pago de entrada**: Muchos cobran 500-1,000 yenes solo por entrar
2. **Ordenas comida/bebida**: Precios normales (1,000-2,000 yenes)
3. **Shows**: Las maid hacen juegos, cantan y dibujan en tu comida
4. **Fotos**: Puedes sacar fotos (con permiso, normalmente 500 yenes extra)

## Reglas importantes

- **No tocar** a las maid (prohibido absolutamente)
- **No fotos** sin permiso
- **No seguir** a las maid cuando se van
- **Sé respetuoso**: Es un trabajo, no un servicio especial

## Los mejores maid cafés

### Akihabara (Tokio)
- **@Home Café**: El más famoso y original. 7 plantas.
- **Maidreamin**: Cadena grande con shows en vivo.
- **Popoposhopu**: Temático de anime.

### Ikebukuro (Tokio)
- **Butler Café**: Versión masculina. Chicos elegantes te atienden.

### Osaka
- **@Home Café Osaka**: La sucursal de Kansai.

## Qué esperar

- Te dan un "carta de bienvenida" con reglas
- La maid dice "¡Bienvenido a casa, amo!" (おかえりなさいませ、ご主人様)
- Dibuja un corazón en tu café con ketchup
- Hay juegos y competiciones
- El ambiente es familiar, no turbio

## Precio típico

- **Entrada**: 0-1,000 yenes
- **Comida**: 1,000-2,000 yenes
- **Bebida**: 500-800 yenes
- **Total**: 2,000-4,000 yenes por persona

## Consejos

- Ve entre semana para evitar colas
- Reserva online si es posible
- Aprende algunas frases en japonés
- Disfruta la experiencia sin prejuicios

---
**Encuentra maid cafés en ViajApp**: Nuestra app tiene mapa con todos los maid cafés de Akihabara y más ciudades.
"""
    },
    {
        "slug": "themed-cafes-japon-guia",
        "title": "Themed Cafés de Japón: Gatos, Lechuzas, Pokémon y Más",
        "description": "Japón inventó los themed cafés. Desde gatos hasta robots, hay un café para cada pasión. Descubre los mejores.",
        "category": "Freaky",
        "readTime": "6 min",
        "tags": ["themed cafe", "cat cafe", "pokemon cafe", "japón freaky"],
        "content": """
## Los themed cafés más populares

### Cat Cafés (Neko Café)
Japón inventó los cat cafés en 2004. Puedes jugar con gatos mientras tomas café. Hay de todas las razas: Scottish Fold, Sphynx, Maine Coon y más.

**Precio**: 1,000-2,000 yenes/hora
**Dónde**: Todos los barrios principales

### Owl Cafés (Lechuzas)
Puedes interactuar con lechuzas reales mientras tomas té. Algunas son gigantes y pueden posarse en tu brazo.

**Precio**: 1,500-2,500 yenes
**Dónde**: Harajuku, Akihabara

### Pokémon Café
El café oficial de Pokémon en Tokio. Comida temática, figuras y experiencias interactivas. Reserva con semanas de antelación.

**Precio**: 2,000-4,000 yenes
**Dónde**: Tokyo DX, Tokio

### Hedgehog Café (Erizos)
Puedes jugar con erizos africanos. Son adorables y muy mansos.

**Precio**: 1,500-2,000 yenes
**Dónde**: Harajuku, Roppongi

### Rabbit Café (Conejos)
Conejos enanos que puedes acariciar. Perfecto para familias.

**Precio**: 1,000-1,500 yenes
**Dónde**: Varios en Tokio

### Robot Café
Shows de robots gigantes con luces neon y música. La experiencia más futurista de Tokio.

**Precio**: 5,000-10,000 yenes
**Dónde**: Shinjuku (verificar disponibilidad)

### Ninja Café
Comida ninja, trucos de magia y decoración de castillo japonés.

**Precio**: 2,000-3,000 yenes
**Dónde**: Asakusa, Tokio

### Vampire Café
Decoración gótica, sangre falsa en los platos y camareros vestidos de vampiro.

**Precio**: 2,500-4,000 yenes
**Dónde**: Ginza, Tokio

## Tips para disfrutar

- **Reserva online**: Muchos están llenos siempre
- **Ve temprano**: Para evitar colas
- **Respeta a los animales**: No los despiertes ni los asustes
- **Paga la entrada**: Muchos cobran por hora más la comida

---
**Descubre todos los themed cafés en ViajApp**: Nuestra app tiene directorio completo con precios, ubicaciones y reserva online.
"""
    },
    {
        "slug": "akihabara-guia-otaku-completa",
        "title": "Akihabara: La Guía Completa del Barrio Otaku",
        "description": "Akihabara es el paraíso de los animes, manga, figures y videojuegos. Todo lo que necesitas saber para visitarlo.",
        "category": "Freaky",
        "readTime": "7 min",
        "tags": ["akihabara", "otaku", "anime", "figures", "japón freaky"],
        "content": """
## ¿Qué es Akihabara?

Akihabara (秋葉原), conocido como "Electric Town", es el barrio otaku más famoso del mundo. Antes era el centro de electrónica, ahora es el epicentro del anime, manga y cultura pop japonesa.

## Qué encontrarás

### Tiendas de Figures y Anime
- **Mandarake**: 8 plantas de manga, figures y coleccionables vintage
- **Animate**: La cadena más grande de productos anime
- **Kotobukiya**: Figures de alta calidad
- **AmiAmi**: Figures nuevas y de segunda mano

### Tiendas de Videojuegos
- **Super Potato**: Videojuegos retro (NES, SNES, PlayStation 1)
- **Game Star**: Cartuchos y consolas antiguas
- **Sega Arcade**: Máquinas de arcade modernas

### Maid Cafés
Ver guía dedicada de maid cafés.

### Manga
- **Manga shops**: Miles de tomos de manga
- **Doujinshi**: Comics independientes (contenido para adultos)

### Electrónica
- **Yodobashi Camera**: Electrónica de última generación
- **Laox**: Souvenirs electrónicos y duty-free

## Circuitos recomendados

### Circuito Básico (3 horas)
1. Estación Akihabara → Salida Electric Town
2. Mandarake (1 hora)
3. Yodobashi Camera (30 min)
4. Maid Café (1 hora)

### Circuito Completo (6 horas)
1. Mandarake (2 horas)
2. Super Potato (1 hora)
3. AmiAmi (1 hora)
4. Maid Café (1 hora)
5. Sega Arcade (1 hora)

## Mejor hora para ir

- **Entre semana**: Menos gente
- **Fines de semana**: Más tiendas abiertas pero lleno
- **Por la noche**: La iluminación es espectacular

## Presupuesto típico

- **Figures**: 3,000-50,000 yenes
- **Manga**: 500-1,000 yenes por tomo
- **Videojuegos retro**: 1,000-10,000 yenes
- **Comida**: 1,000-3,000 yenes
- **Entrada arcade**: 100-500 yenes por juego

---
**Navega Akihabara con ViajApp**: Nuestra app tiene mapa interactivo con las mejores tiendas y rutas optimizadas.
"""
    },
    {
        "slug": "capsule-hotels-experiencia-completa",
        "title": "Capsule Hotels: La Experiencia que Debes Vivir en Japón",
        "description": "Los capsule hotels son mucho más que dormir en una caja. Son una experiencia futurista, económica y única de Japón.",
        "category": "Freaky",
        "readTime": "6 min",
        "tags": ["capsule hotel", "alojamiento japon", "japón freaky", "hostales japon"],
        "content": """
## ¿Qué es un Capsule Hotel?

Un capsule hotel es un alojamiento donde duermes en una "cápsula" (una cabina individual) en vez de una habitación. Inventado en Osaka en 1979, ahora son experiencias de lujo.

## Tipos de Capsule Hotels

### Básicos (3,000-5,000 yenes/noche)
- Cápsula simple con colchón
- Baños compartidos
- Lockers para equipaje
- Ideal para una noche

### Modernos (5,000-8,000 yenes/noche)
- Cápsula con TV, USB, WiFi
- Baños privados
- Zonas de relax
- Diseño futurista

### Premium (8,000-15,000 yenes/noche)
- Cápsula tipo suite
- Baño privado completo
- Onsen incluido
- Desayuno incluido

## Los mejores capsule hotels

### Nine Hours (Tokio, Osaka)
El más minimalista y moderno. Diseño de arquitectos famosos. Limpieza impecable.

**Precio**: 4,000-6,000 yenes
**Ubicaciones**: Aeropuerto de Narita, Shinjuku, Kyoto

### First Cabin (Tokio, Osaka)
Cabinas tipo "primera clase de avión". Espacio para sentarse, TV grande.

**Precio**: 6,000-10,000 yenes
**Ubicaciones**: Shinjuku, Tokyo Station, Osaka

### The Millennials (Kyoto)
El más tech. Control por smartphone, cama articulada, proyección en la pared.

**Precio**: 5,000-8,000 yenes
**Ubicaciones**: Kyoto

### Book and Bed (Tokio, Osaka)
Dormir entre libros. Estanterías de manga y libros como decoración.

**Precio**: 5,000-8,000 yenes
**Ubicaciones**: Ikebukuro, Shinjuku, Osaka

## La experiencia paso a paso

1. **Check-in**: Recibes una llave numérica y una bolsa con toalla y pijama
2. **Zona de camas**: Te quitas los zapatos y guardas todo en el locker
3. **Tu cápsula**: Tamaño típico: 1m x 1m x 2m. Colchón, almohada, cortina
4. **Baños**: Duchas, aseo, secador de pelo
5. **Zonas comunes**: Sofás, vending machines, manga
6. **Dormir**: Es sorprendentemente cómodo
7. **Check-out**: Dejas la bolsa y te vas

## Pros y Contras

**Pros:**
- Económico (desde 3,000 yenes)
- Experiencia única
- Limpio y seguro
- En el centro de la ciudad

**Contras:**
- Ruido (algunos tienen orejeras)
- Poco espacio
- No apto para claustrofóbicos
- Baños compartidos (en los básicos)

## Consejos

- **Trae tapones para los oídos**
- **Usa el pijama que te dan** (es gratis)
- **No hables en la zona de cápsulas**
- **Guarda el móvil en modo silencio**
- **Disfruta la experiencia**: Es más cómodo de lo que parece

---
**Reserva capsule hotels en ViajApp**: Nuestra app tiene comparador de precios y disponibilidad en tiempo real.
"""
    }
]

_published_posts = []

@router.get("/posts")
async def get_blog_posts():
    """Obtiene todos los posts del blog (estáticos + generados)"""
    from app.api.v1.blog import BLOG_POOL, _published_posts
    from datetime import datetime
    
    static_posts = []
    for post in BLOG_POOL[:6]:
        static_posts.append({
            **post,
            "date": "2026-07-" + str(15 - BLOG_POOL.index(post)).zfill(2),
            "generated": False
        })
    
    return {"posts": static_posts + _published_posts}

@router.post("/generate")
async def generate_new_post():
    """Genera y publica un nuevo post del blog"""
    from datetime import datetime
    import random
    
    available = [p for p in BLOG_POOL if p["slug"] not in [pp["slug"] for pp in _published_posts]]
    
    if not available:
        return {"message": "No hay más posts disponibles en el pool", "published": False}
    
    post = random.choice(available)
    new_post = {
        **post,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generated": True
    }
    
    _published_posts.append(new_post)
    
    return {
        "message": "Post generado exitosamente",
        "post": new_post,
        "published": True,
        "remaining": len(available) - 1
    }

@router.get("/posts/{slug}")
async def get_blog_post(slug: str):
    """Obtiene un post específico por slug"""
    from fastapi import HTTPException
    
    all_posts = []
    
    for post in BLOG_POOL:
        all_posts.append(post)
    
    for post in _published_posts:
        all_posts.append(post)
    
    for post in all_posts:
        if post["slug"] == slug:
            return post
    
    raise HTTPException(status_code=404, detail="Post no encontrado")

@router.get("/stats")
async def get_blog_stats():
    """Estadísticas del blog"""
    return {
        "total_pool": len(BLOG_POOL),
        "published": len(_published_posts),
        "remaining": len(BLOG_POOL) - len(_published_posts)
    }
