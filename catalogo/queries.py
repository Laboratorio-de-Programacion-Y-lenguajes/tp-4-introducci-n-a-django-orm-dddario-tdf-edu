from __future__ import annotations

from django.db.models import Count, F, Q

from .models import Autor, Libro


def libros_por_categoria(nombre_categoria: str):
    """Devuelve un QuerySet de Libros que pertenecen a la categoría indicada."""
    return Libro.objects.filter(categorias__nombre=nombre_categoria)



def autores_con_mas_de_n_libros(n: int):
    """Devuelve un QuerySet de Autores que tienen más de n libros en el catálogo."""
    return Autor.objects.annotate(cantidad_libros=Count("libro")).filter(cantidad_libros__gt=n)



def libros_sin_disponibilidad():
    """Devuelve un QuerySet de Libros donde no hay copias disponibles."""
    return Libro.objects.annotate(
        activos=Count("prestamo", filter=Q(prestamo__fecha_devolucion__isnull=True))
    ).filter(activos=F("cantidad_total"))


def top_n_libros_mas_prestados(n: int):
    """Devuelve los N libros con más préstamos totales, ordenados de más a menos."""
    return Libro.objects.annotate(total_prestamos=Count("prestamo")).order_by("-total_prestamos")[:n]
