# Japan Travel API

API completa para viajeros a Japon con informacion cultural, presupuesto, eventos, transporte, comida y emergencias.

## Endpoints Disponibles

### Autenticacion (`/v1/auth`)
- `POST /register` - Registrar usuario
- `POST /login` - Iniciar sesion
- `GET /me` - Obtener perfil (requiere token)

### Guia Cultural (`/v1/culture`)
- `GET /phrases` - Frases por contexto (basico, restaurante, compras, transporte, hotel, emergencia)
- `GET /etiquette` - Reglas de etiqueta por situacion
- `GET /do-and-dont` - Que hacer y que no hacer
- `GET /scenarios` - Situaciones comunes con dialogos

### Presupuesto (`/v1/budget`)
- `GET /cities` - Costes diarios por ciudad
- `GET /cities/{city}` - Detalle de ciudad
- `GET /taxfree` - Informacion de tiendas tax-free
- `GET /estimate` - Estimar gasto total del viaje

### Eventos y Festivales (`/v1/events`)
- `GET /festivals` - Calendario de festivales
- `GET /seasons` - Informacion por temporada
- `GET /seasons/{season}` - Detalle de temporada
- `GET /city/{city}` - Eventos por ciudad

### Transporte (`/v1/transport`)
- `GET /jrpass` - Informacion del JR Pass
- `GET /connections` - Conexiones entre ciudades
- `GET /connections/{from}/{to}` - Ruta especifica
- `GET /tips` - Consejos de transporte

### Comida (`/v1/food`)
- `GET /guide` - Guia gastronomica por ciudad
- `GET /guide/{city}` - Comida tipica de ciudad
- `GET /etiquette` - Etiqueta en restaurantes
- `GET /dishes` - Todos los platos

### Emergencias (`/v1/emergency`)
- `GET /contacts` - Numeros de emergencia
- `GET /phrases` - Frases de emergencia
- `GET /hospitals` - Hospitales por ciudad
- `GET /embassies/{country}` - Embajadas
- `GET /tips` - Consejos de salud

## Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn app.main:app --reload

# Abrir docs
# http://localhost:8000/docs
```

## Despliegue en Render

1. Conectar repositorio GitHub
2. Seleccionar Python
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Estructura del Proyecto

```
Japon-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuracion
│   ├── core/
│   │   ├── security.py      # JWT y autenticacion
│   ├── api/v1/
│   │   ├── router.py        # Router principal
│   │   ├── auth.py          # Autenticacion
│   │   ├── culture.py       # Guia cultural
│   │   ├── budget.py        # Presupuesto
│   │   ├── events.py        # Eventos
│   │   ├── transport.py     # Transporte
│   │   ├── food.py          # Comida
│   │   └── emergency.py     # Emergencias
│   ├── schemas/
│   │   └── culture.py       # Modelos de datos
│   └── services/
│       └── culture_service.py # Logica de negocio
├── tests/
├── requirements.txt
├── render.yaml
└── README.md
```

## Monetizacion (Proximo Futuro)

- **Tier Gratis**: 100 requests/dia
- **Tier Premium**: 10,000 requests/dia ($5/mes)
- **Tier Business**: Ilimitado ($20/mes)

## Licencia

MIT
