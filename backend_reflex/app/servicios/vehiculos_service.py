"""
Servicio de Gestión de Vehículos
Contiene la lógica de negocio para la gestión de vehículos en el ecosistema de negocios de autos.
Autor: Ibar - Tech Lead Backend
"""
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from sqlmodel import select, and_, or_, desc, asc, func

# Importar modelos y servicios
from ..modelos.vehiculo import Vehiculo, TipoMotor, EstadoVehiculo, TipoVehiculo
from ..modelos.usuario import Usuario, TipoUsuario
from ..modelos.validaciones import validar_datos_vehiculo
from .base_datos import db_service, transactional

class VehiculosService:
    """Servicio para gestión completa de vehículos"""
    
    def __init__(self):
        self.db = db_service
    
    # ==================== OPERACIONES BÁSICAS CRUD ====================
    
    def crear_vehiculo(self, datos_vehiculo: Dict[str, Any], vendedor_id: int) -> Tuple[bool, str, Optional[Vehiculo]]:
        """Crea un nuevo vehículo con validaciones"""
        try:
            # Validar datos del vehículo
            es_valido, mensaje_error = validar_datos_vehiculo(datos_vehiculo)
            if not es_valido:
                return False, mensaje_error, None
            
            # Verificar que el vendedor existe y puede publicar
            vendedor = self.db.get_by_id(Usuario, vendedor_id)
            if not vendedor:
                return False, "Vendedor no encontrado", None
            
            if not vendedor.puede_publicar:
                return False, "El usuario no puede publicar vehículos", None
            
            # Crear instancia del vehículo
            vehiculo = Vehiculo(
                **datos_vehiculo,
                vendedor_id=vendedor_id,
                fecha_creacion=datetime.now(),
                estado=EstadoVehiculo.DISPONIBLE,
                activo=True,
                vistas=0
            )
            
            # Guardar en base de datos
            vehiculo_creado = self.db.create(vehiculo)
            
            # Actualizar estadísticas del vendedor
            vendedor.vehiculos_publicados += 1
            self.db.update(vendedor)
            
            return True, "Vehículo creado exitosamente", vehiculo_creado
            
        except Exception as e:
            return False, f"Error al crear vehículo: {str(e)}", None
    
    def obtener_vehiculo(self, vehiculo_id: int, incrementar_vista: bool = False) -> Optional[Vehiculo]:
        """Obtiene un vehículo por ID con opción de incrementar vistas"""
        vehiculo = self.db.get_by_id(Vehiculo, vehiculo_id)
        
        if vehiculo and incrementar_vista and vehiculo.activo:
            vehiculo.incrementar_vistas()
            self.db.update(vehiculo)
        
        return vehiculo
    
    def actualizar_vehiculo(self, vehiculo_id: int, datos_actualizacion: Dict[str, Any], 
                        usuario_id: int) -> Tuple[bool, str, Optional[Vehiculo]]:
        """Actualiza un vehículo existente"""
        try:
            vehiculo = self.db.get_by_id(Vehiculo, vehiculo_id)
            if not vehiculo:
                return False, "Vehículo no encontrado", None
            
            # Verificar permisos (solo el vendedor o admin puede actualizar)
            if vehiculo.vendedor_id != usuario_id:
                usuario = self.db.get_by_id(Usuario, usuario_id)
                if not usuario or usuario.tipo_usuario != TipoUsuario.ADMIN:
                    return False, "Sin permisos para actualizar este vehículo", None
            
            # Actualizar campos permitidos
            campos_actualizables = [
                'precio', 'precio_negociable', 'descripcion', 'caracteristicas_extras',
                'color_exterior', 'color_interior', 'disponible_financiacion', 
                'acepta_parte_pago', 'ubicacion_ciudad', 'ubicacion_provincia'
            ]
            
            for campo, valor in datos_actualizacion.items():
                if campo in campos_actualizables and hasattr(vehiculo, campo):
                    setattr(vehiculo, campo, valor)
            
            vehiculo.fecha_actualizacion = datetime.now()
            vehiculo_actualizado = self.db.update(vehiculo)
            
            return True, "Vehículo actualizado exitosamente", vehiculo_actualizado
            
        except Exception as e:
            return False, f"Error al actualizar vehículo: {str(e)}", None
    
    def eliminar_vehiculo(self, vehiculo_id: int, usuario_id: int, 
                        motivo: str = "Eliminado por el usuario") -> Tuple[bool, str]:
        """Elimina (soft delete) un vehículo"""
        try:
            vehiculo = self.db.get_by_id(Vehiculo, vehiculo_id)
            if not vehiculo:
                return False, "Vehículo no encontrado"
            
            # Verificar permisos
            if vehiculo.vendedor_id != usuario_id:
                usuario = self.db.get_by_id(Usuario, usuario_id)
                if not usuario or usuario.tipo_usuario != TipoUsuario.ADMIN:
                    return False, "Sin permisos para eliminar este vehículo"
            
            # Soft delete
            vehiculo.activo = False
            vehiculo.motivo_inactivo = motivo
            vehiculo.fecha_actualizacion = datetime.now()
            self.db.update(vehiculo)
            
            return True, "Vehículo eliminado exitosamente"
            
        except Exception as e:
            return False, f"Error al eliminar vehículo: {str(e)}"
    
    # ==================== BÚSQUEDA Y FILTRADO ====================
    
    def buscar_vehiculos(self, filtros: Dict[str, Any] = None, 
                        limite: int = 20, pagina: int = 1) -> Dict[str, Any]:
        """Búsqueda avanzada de vehículos con filtros y paginación"""
        offset = (pagina - 1) * limite
        filtros = filtros or {}
        
        # Filtros base (solo vehículos activos y disponibles)
        filtros_base = {
            "activo": True,
            "estado": EstadoVehiculo.DISPONIBLE
        }
        
        # Combinar filtros
        filtros_finales = {**filtros_base, **filtros}
        
        try:
            vehiculos = self.db.search(
                Vehiculo, 
                filtros_finales, 
                limit=limite, 
                offset=offset,
                order_by=filtros.get('order_by', '-fecha_creacion')
            )
            
            total = self.db.count(Vehiculo, filtros_finales)
            total_paginas = (total + limite - 1) // limite
            
            return {
                "vehiculos": vehiculos,
                "total": total,
                "pagina_actual": pagina,
                "total_paginas": total_paginas,
                "has_siguiente": pagina < total_paginas,
                "has_anterior": pagina > 1,
                "limite": limite
            }
            
        except Exception as e:
            return {
                "vehiculos": [],
                "total": 0,
                "pagina_actual": 1,
                "total_paginas": 0,
                "has_siguiente": False,
                "has_anterior": False,
                "limite": limite,
                "error": str(e)
            }
    
    def buscar_por_texto(self, query: str, limite: int = 20) -> List[Vehiculo]:
        """Búsqueda de texto libre en marca, modelo y descripción"""
        with self.db.get_session() as session:
            query_lower = query.lower()
            
            statement = select(Vehiculo).where(
                and_(
                    Vehiculo.activo == True,
                    Vehiculo.estado == EstadoVehiculo.DISPONIBLE,
                    or_(
                        func.lower(Vehiculo.marca).contains(query_lower),
                        func.lower(Vehiculo.modelo).contains(query_lower),
                        func.lower(Vehiculo.descripcion).contains(query_lower)
                    )
                )
            ).limit(limite)
            
            return list(session.exec(statement).all())
    
    def obtener_filtros_disponibles(self) -> Dict[str, List[Any]]:
        """Obtiene todos los valores únicos para filtros"""
        with self.db.get_session() as session:
            # Obtener marcas únicas
            marcas = list(session.exec(
                select(Vehiculo.marca).distinct().where(Vehiculo.activo == True)
            ).all())
            
            # Obtener provincias únicas
            provincias = list(session.exec(
                select(Vehiculo.ubicacion_provincia).distinct().where(Vehiculo.activo == True)
            ).all())
            
            # Tipos de motor disponibles
            tipos_motor = [motor.value for motor in TipoMotor]
            
            # Tipos de vehículo disponibles
            tipos_vehiculo = [tipo.value for tipo in TipoVehiculo]
            
            # Rangos de años
            años = list(range(datetime.now().year, 1950, -1))
            
            # Rangos de precios predefinidos
            rangos_precios = [
                {"label": "< 5.000€", "min": 0, "max": 5000},
                {"label": "5.000€ - 10.000€", "min": 5000, "max": 10000},
                {"label": "10.000€ - 20.000€", "min": 10000, "max": 20000},
                {"label": "20.000€ - 35.000€", "min": 20000, "max": 35000},
                {"label": "35.000€ - 50.000€", "min": 35000, "max": 50000},
                {"label": "> 50.000€", "min": 50000, "max": 999999}
            ]
            
            return {
                "marcas": sorted(marcas),
                "provincias": sorted(provincias),
                "tipos_motor": tipos_motor,
                "tipos_vehiculo": tipos_vehiculo,
                "años": años,
                "rangos_precios": rangos_precios
            }
    
    # ==================== VEHÍCULOS DESTACADOS Y RECOMENDACIONES ====================
    
    def obtener_destacados(self, limite: int = 10) -> List[Vehiculo]:
        """Obtiene vehículos marcados como destacados"""
        filtros = {
            "activo": True,
            "estado": EstadoVehiculo.DISPONIBLE,
            "destacado": True
        }
        return self.db.search(Vehiculo, filtros, limit=limite, order_by='-fecha_creacion')
    
    def obtener_recientes(self, limite: int = 10, dias: int = 7) -> List[Vehiculo]:
        """Obtiene vehículos publicados recientemente"""
        fecha_limite = datetime.now() - timedelta(days=dias)
        
        with self.db.get_session() as session:
            statement = select(Vehiculo).where(
                and_(
                    Vehiculo.activo == True,
                    Vehiculo.estado == EstadoVehiculo.DISPONIBLE,
                    Vehiculo.fecha_creacion >= fecha_limite
                )
            ).order_by(desc(Vehiculo.fecha_creacion)).limit(limite)
            
            return list(session.exec(statement).all())
    
    def obtener_mas_visitados(self, limite: int = 10) -> List[Vehiculo]:
        """Obtiene vehículos más visitados"""
        filtros = {
            "activo": True,
            "estado": EstadoVehiculo.DISPONIBLE
        }
        return self.db.search(Vehiculo, filtros, limit=limite, order_by='-vistas')
    
    def obtener_similares(self, vehiculo_id: int, limite: int = 5) -> List[Vehiculo]:
        """Obtiene vehículos similares basados en marca, precio y tipo"""
        vehiculo = self.db.get_by_id(Vehiculo, vehiculo_id)
        if not vehiculo:
            return []
        
        # Rango de precios (±20%)
        precio_min = vehiculo.precio * 0.8
        precio_max = vehiculo.precio * 1.2
        
        with self.db.get_session() as session:
            statement = select(Vehiculo).where(
                and_(
                    Vehiculo.id != vehiculo_id,
                    Vehiculo.activo == True,
                    Vehiculo.estado == EstadoVehiculo.DISPONIBLE,
                    Vehiculo.marca == vehiculo.marca,
                    Vehiculo.precio.between(precio_min, precio_max)
                )
            ).limit(limite)
            
            similares = list(session.exec(statement).all())
            
            # Si no hay suficientes de la misma marca, buscar por tipo de vehículo
            if len(similares) < limite:
                statement2 = select(Vehiculo).where(
                    and_(
                        Vehiculo.id != vehiculo_id,
                        Vehiculo.activo == True,
                        Vehiculo.estado == EstadoVehiculo.DISPONIBLE,
                        Vehiculo.tipo_vehiculo == vehiculo.tipo_vehiculo,
                        Vehiculo.precio.between(precio_min, precio_max),
                        Vehiculo.marca != vehiculo.marca  # Diferente marca
                    )
                ).limit(limite - len(similares))
                
                similares.extend(list(session.exec(statement2).all()))
            
            return similares[:limite]
    
    # ==================== GESTIÓN DE ESTADO ====================
    
    def marcar_como_vendido(self, vehiculo_id: int, usuario_id: int) -> Tuple[bool, str]:
        """Marca un vehículo como vendido"""
        try:
            vehiculo = self.db.get_by_id(Vehiculo, vehiculo_id)
            if not vehiculo:
                return False, "Vehículo no encontrado"
            
            # Verificar permisos
            if vehiculo.vendedor_id != usuario_id:
                usuario = self.db.get_by_id(Usuario, usuario_id)
                if not usuario or usuario.tipo_usuario != TipoUsuario.ADMIN:
                    return False, "Sin permisos para modificar este vehículo"
            
            vehiculo.marcar_como_vendido()
            self.db.update(vehiculo)
            
            # Actualizar estadísticas del vendedor
            vendedor = self.db.get_by_id(Usuario, vehiculo.vendedor_id)
            if vendedor:
                vendedor.actualizar_estadisticas(vehiculo_vendido=True)
                self.db.update(vendedor)
            
            return True, "Vehículo marcado como vendido"
            
        except Exception as e:
            return False, f"Error al marcar como vendido: {str(e)}"
    
    def destacar_vehiculo(self, vehiculo_id: int, usuario_id: int) -> Tuple[bool, str]:
        """Marca un vehículo como destacado"""
        try:
            vehiculo = self.db.get_by_id(Vehiculo, vehiculo_id)
            if not vehiculo:
                return False, "Vehículo no encontrado"
            
            # Verificar permisos (solo el vendedor)
            if vehiculo.vendedor_id != usuario_id:
                return False, "Solo el vendedor puede destacar el vehículo"
            
            vehiculo.activar_destacado()
            self.db.update(vehiculo)
            
            return True, "Vehículo destacado exitosamente"
            
        except Exception as e:
            return False, f"Error al destacar vehículo: {str(e)}"
    
    # ==================== ESTADÍSTICAS Y REPORTES ====================
    
    def obtener_estadisticas_generales(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales de vehículos"""
        stats = self.db.get_stats(Vehiculo)
        
        # Estadísticas adicionales específicas de vehículos
        with self.db.get_session() as session:
            # Vehículos por estado
            por_estado = {}
            for estado in EstadoVehiculo:
                count = len(list(session.exec(
                    select(Vehiculo).where(
                        and_(Vehiculo.estado == estado, Vehiculo.activo == True)
                    )
                ).all()))
                por_estado[estado.value] = count
            
            # Top 5 marcas
            from sqlmodel import func
            top_marcas = list(session.exec(
                select(Vehiculo.marca, func.count(Vehiculo.id).label('count'))
                .where(Vehiculo.activo == True)
                .group_by(Vehiculo.marca)
                .order_by(desc('count'))
                .limit(5)
            ).all())
            
            # Precio promedio por tipo de motor
            precio_por_motor = {}
            for tipo_motor in TipoMotor:
                avg_precio = session.exec(
                    select(func.avg(Vehiculo.precio))
                    .where(
                        and_(
                            Vehiculo.tipo_motor == tipo_motor,
                            Vehiculo.activo == True
                        )
                    )
                ).first()
                precio_por_motor[tipo_motor.value] = round(float(avg_precio or 0), 2)
        
        stats.update({
            "por_estado": por_estado,
            "top_marcas": [{"marca": marca, "count": count} for marca, count in top_marcas],
            "precio_promedio_por_motor": precio_por_motor
        })
        
        return stats
    
    def obtener_vehiculos_vendedor(self, vendedor_id: int, incluir_inactivos: bool = False) -> List[Vehiculo]:
        """Obtiene todos los vehículos de un vendedor"""
        filtros = {"vendedor_id": vendedor_id}
        if not incluir_inactivos:
            filtros["activo"] = True
        
        return self.db.search(Vehiculo, filtros, limit=1000, order_by='-fecha_creacion')

# Instancia global del servicio
vehiculos_service = VehiculosService()