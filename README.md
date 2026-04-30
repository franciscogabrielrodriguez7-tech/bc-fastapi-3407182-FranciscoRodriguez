# 🚀 AeroTech - empresa de trasnporte aéreo

Sistema backend para la gestión de vuelos, flota y servicios aéreos desarrollado con **FastAPI**.

## ✈️ Dominio del Proyecto
El sistema está dentro del dominio **Aéreo**, centrándose específicamente en la gestión operativa de una aerolínea comercial.

## 🛠️ Entidades Principales
* **Aircraft (Aviones):** Gestionados mediante un sistema de niveles de detalle (Short-haul, Medium-haul, Long-haul).
* **Crews (Tripulación):** Roles profesionales que incluyen Pilotos, Copilotos y Auxiliares de vuelo.
* **Passengers (Pasajeros):** Usuarios registrados con identificación de pasaporte y estatus de viajero.
* **Flights (Vuelos):** El agregador central que conecta un avión, una tripulación específica y una lista de pasajeros a una ruta definida.

## 📡 Endpoints de la API

### 🏠 Estado del Sistema
* `GET /`: Información básica de la API y lenguajes soportados.
* `GET /health`: Estado de salud del sistema y marca de tiempo del servidor.

### 👤 Servicios al Pasajero
* `GET /welcome/{name}?lang={code}`: Mensajes de bienvenida localizados en más de 10 idiomas (ES, EN, PT, IT, FR, etc.).
* `GET /services/lounge?hour={int}`: Estado dinámico de la sala VIP según la hora del día.

### 🛫 Gestión de Vuelos y Flota
* `GET /fleet/{aircraft_id}?detail_level={1|2}`: Especificaciones técnicas de aviones por niveles.
* `GET /crews/{crew_id}`: Perfil detallado de miembros de la tripulación.
* `GET /flights/all`: Listado de todas las operaciones de vuelo programadas.
* `GET /flights/{flight_number}`: **Endpoint Asociativo**. Devuelve un objeto completo con datos vinculados de Avión, Tripulación y Pasajeros.

## 🌟 Características Técnicas y Buenas Prácticas
1.  **Agregación de Datos Relacionales:** Demuestra relaciones complejas entre entidades mediante el uso de bases de datos en memoria (Mock).
2.  **Estandarización Internacional:** Código y documentación desarrollados íntegramente en inglés para alineación con estándares de la industria.
3.  **Clean Code:** Implementación de convenciones **PEP 8** (estilo) y **PEP 257** (documentación de funciones/Docstrings).
4.  **Manejo de Errores:** Uso de `HTTPException` para garantizar respuestas claras ante datos no encontrados (404).
5.  **Tipado Estático:** Implementación de `typing` para mejorar la seguridad del código y la auto-documentación en Swagger/ReDoc.

---
*Desarrollado como parte del Bootcamp FastAPI Zero to Hero - Semana 01.*