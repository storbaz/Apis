# ViajApp API

API REST completa para la plataforma ViajApp — guia de viajes a Japon.

**Produccion:** https://japan-travel-api.onrender.com

## Stack

- **Framework:** FastAPI (Python 3.11)
- **Base de datos:** Supabase (PostgreSQL)
- **Auth:** JWT + Supabase
- **Despliegue:** Render (auto-deploy desde GitHub)

## Desarrollo Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
# http://localhost:8002/docs
```

## Endpoints (35+)

### Autenticacion (`/v1/auth`)
- `POST /register` — Registrar usuario
- `POST /login` — Iniciar sesion
- `GET /me` — Obtener perfil

### Itinerarios (`/v1/itineraries`)
- `GET /` — Listar itinerarios del usuario
- `POST /` — Crear itinerario
- `GET /shared/{id}` — Ver itinerario compartido (publico)
- `PUT /{id}` — Actualizar itinerario
- `DELETE /{id}` — Eliminar itinerario
- `PUT /{id}/share` — Activar/desactivar compartir
- `POST /{id}/items` — Anadir actividad
- `DELETE /{id}/items/{item_id}` — Eliminar actividad

### Valoraciones (`/v1/reviews`)
- `GET /itinerary/{id}` — Valoraciones de un itinerario + media
- `POST /` — Crear valoracion (1-5 estrellas + comentario)
- `DELETE /{id}` — Eliminar valoracion
- `GET /recent` — Valoraciones recientes

### Gastos Compartidos (`/v1/shared-expenses`)
- `POST /groups` — Crear grupo
- `GET /groups` — Listar grupos del usuario
- `GET /groups/{id}` — Detalle grupo + miembros + gastos
- `POST /groups/{id}/members` — Anadir miembro
- `POST /expenses` — Anadir gasto
- `DELETE /expenses/{id}` — Eliminar gasto
- `GET /groups/{id}/balance` — Calcular balances

### Consejos de la Comunidad (`/v1/community-tips`)
- `GET /` — Listar consejos aprobados
- `GET /recent` — Consejos recientes
- `POST /` — Crear consejo
- `POST /{id}/like` — Dar like
- `DELETE /{id}` — Eliminar consejo

### Favoritos (`/v1/favorites`)
- `GET /` — Listar favoritos
- `POST /` — Anadir favorito
- `DELETE /{id}` — Eliminar favorito

### Blog (`/v1/blog`)
- `GET /posts` — Listar articulos
- `GET /posts/{slug}` — Ver articulo

### Guia Cultural (`/v1/culture`)
- `GET /phrases` — Frases por contexto
- `GET /etiquette` — Reglas de etiqueta
- `GET /do-and-dont` — Que hacer y que no
- `GET /scenarios` — Situaciones comunes

### Presupuesto (`/v1/budget`)
- `GET /cities` — Costes por ciudad
- `GET /cities/{city}` — Detalle de ciudad
- `GET /taxfree` — Tiendas tax-free
- `GET /estimate` — Estimar gasto total

### Eventos (`/v1/events`)
- `GET /festivals` — Calendario de festivales
- `GET /seasons` — Info por temporada
- `GET /city/{city}` — Eventos por ciudad

### Transporte (`/v1/transport`)
- `GET /jrpass` — Info JR Pass
- `GET /connections` — Conexiones entre ciudades
- `GET /tips` — Consejos

### Comida (`/v1/food`)
- `GET /guide` — Guia gastronomica
- `GET /guide/{city}` — Comida por ciudad
- `GET /etiquette` — Etiqueta
- `GET /dishes` — Todos los platos

### Emergencias (`/v1/emergency`)
- `GET /contacts` — Numeros de emergencia
- `GET /phrases` — Frases de emergencia
- `GET /hospitals` — Hospitales
- `GET /embassies/{country}` — Embajadas

### Otros
- `GET /weather/{city}` — Clima (OpenWeather API)
- `POST /translator/translate` — Traduccion
- `GET /tips/save` — Tips de ahorro
- `GET /restaurants/{city}` — Restaurantes
- `GET /places/{city}` — Lugares populares
- `GET /stats` — Estadisticas de turismo

## Estructura

```
Japon-api/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuracion (env vars)
│   ├── core/
│   │   ├── security.py      # JWT auth
│   │   └── database.py      # Supabase client
│   ├── api/v1/
│   │   ├── router.py        # Router principal (19 modulos)
│   │   ├── auth.py
│   │   ├── itineraries.py
│   │   ├── reviews.py
│   │   ├── shared_expenses.py
│   │   ├── community_tips.py
│   │   ├── favorites.py
│   │   ├── blog.py
│   │   ├── culture.py
│   │   ├── budget.py
│   │   ├── events.py
│   │   ├── transport.py
│   │   ├── food.py
│   │   ├── emergency.py
│   │   ├── weather.py
│   │   ├── translator.py
│   │   ├── tips.py
│   │   ├── restaurants.py
│   │   ├── places.py
│   │   └── stats.py
│   ├── schemas/
│   └── services/
│       └── culture_service.py
├── data/
│   └── japan_stats.json     # Estadisticas de turismo
├── scripts/
│   ├── post_to_devto.py     # Blog rotation (4 articulos)
│   └── update_stats.py      # Actualizador mensual
├── tests/                   # 33 tests
├── .github/workflows/
│   └── update-stats.yml     # GitHub Action mensual
├── requirements.txt
└── render.yaml
```

## Tablas Supabase

Las siguientes tablas deben existir en Supabase:

- `users` — Usuarios (id, email, name, created_at)
- `itineraries` — Itinerarios (id, user_id, title, description, start_date, end_date, is_shared, created_at)
- `itinerary_items` — Actividades (id, itinerary_id, day_number, time, title, description, location, category)
- `reviews` — Valoraciones (id, itinerary_id, user_id, rating, comment, created_at)
- `expense_groups` — Grupos de gastos (id, user_id, name, description, created_at)
- `expense_group_members` — Miembros (id, group_id, user_id, name)
- `expenses` — Gastos (id, group_id, user_id, amount, currency, description, paid_by, split_with, created_at)
- `community_tips` — Consejos (id, user_id, title, content, category, city, tags, approved, likes, created_at)
- `favorites` — Favoritos (id, user_id, item_type, item_id, created_at)

## Tests

```bash
python -m pytest tests/ -v
# 33 tests passing
```

## Deploy

Auto-deploy desde GitHub master branch en Render.
