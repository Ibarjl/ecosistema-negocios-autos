"""
Servicio de base de datos
Contiene la lógica base para operaciones CRUD y acceso a datos.
"""
import reflex as rx
from sqlmodel import Session, select, and_, or_, func
from typing import List, Dict, Any, Optional, Type, TypeVar
from contextlib import contextmanager

T = TypeVar('T')

class DatabaseService:
    """Servicio base para operaciones de base de datos"""
    
    @contextmanager
    def get_session(self):
        with rx.session() as session:
            yield session
    
    def create(self, instance: T) -> T:
        with self.get_session() as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
    
    def get_by_id(self, model: Type[T], id: int) -> Optional[T]:
        with self.get_session() as session:
            return session.get(model, id)
    
    def update(self, instance: T) -> T:
        with self.get_session() as session:
            session.add(instance)
            session.commit()
            session.refresh(instance)
            return instance
    
    def search(self, model: Type[T], filtros: Dict[str, Any], 
            limit: int = 20, offset: int = 0, 
            order_by: str = 'id') -> List[T]:
        with self.get_session() as session:
            query = select(model)
            
            # Aplicar filtros
            for field, value in filtros.items():
                if hasattr(model, field):
                    if isinstance(value, dict):
                        # Filtros especiales como {'lte': 100}
                        if 'lte' in value:
                            query = query.where(getattr(model, field) <= value['lte'])
                        if 'gte' in value:
                            query = query.where(getattr(model, field) >= value['gte'])
                        if 'between' in value:
                            min_val, max_val = value['between']
                            query = query.where(getattr(model, field).between(min_val, max_val))
                    else:
                        query = query.where(getattr(model, field) == value)
            
            # Ordenamiento
            if order_by.startswith('-'):
                field = order_by[1:]
                if hasattr(model, field):
                    query = query.order_by(getattr(model, field).desc())
            else:
                if hasattr(model, order_by):
                    query = query.order_by(getattr(model, order_by))
            
            return list(session.exec(query.offset(offset).limit(limit)).all())
    
    def count(self, model: Type[T], filtros: Dict[str, Any]) -> int:
        with self.get_session() as session:
            query = select(func.count()).select_from(model)
            for field, value in filtros.items():
                if hasattr(model, field):
                    if isinstance(value, dict):
                        if 'lte' in value:
                            query = query.where(getattr(model, field) <= value['lte'])
                        if 'gte' in value:
                            query = query.where(getattr(model, field) >= value['gte'])
                    else:
                        query = query.where(getattr(model, field) == value)
            return session.exec(query).first() or 0
    
    def get_stats(self, model: Type[T]) -> Dict[str, Any]:
        with self.get_session() as session:
            total = session.exec(select(func.count()).select_from(model)).first()
            return {"total": total or 0}

# Instancia global
db_service = DatabaseService()

# Decorator para transacciones
def transactional(func):
    """Decorator para operaciones transaccionales"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # En una implementación real, aquí harías rollback
            raise e
    return wrapper