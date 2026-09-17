from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from pydantic_classes import *
from sql_alchemy import *
from database import get_db
from bal_stdlib import *

router = APIRouter()


@router.get("/class/", response_model=None, tags=["Class"])
def get_all_class(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    return database.query(Class).all()


@router.get("/class/count/", response_model=None, tags=["Class"])
def get_count_class(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Class entities"""
    count = database.query(Class).count()
    return {"count": count}


@router.get("/class/paginated/", response_model=None, tags=["Class"])
def get_paginated_class(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Class entities"""
    total = database.query(Class).count()
    class_list = database.query(Class).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": class_list
    }
@router.get("/class/search/", response_model=None, tags=["Class"])
def search_class(
    Attribute: str = None,
    database: Session = Depends(get_db)
) -> list:
    """Search Class entities by attributes"""
    query = database.query(Class)

    if Attribute is not None:
        query = query.filter(Class.Attribute.ilike(f"%{Attribute}%"))

    results = query.all()
    return results


@router.get("/class/{class_id}/", response_model=None, tags=["Class"])
async def get_class(class_id: int, database: Session = Depends(get_db)) -> Class:
    db_class = database.query(Class).filter(Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    response_data = {
        "class": db_class,
}
    return response_data



@router.post("/class/", response_model=None, tags=["Class"])
async def create_class(class_data: ClassCreate, database: Session = Depends(get_db)) -> Class:


    db_class = Class(
        Attribute=class_data.Attribute        )

    database.add(db_class)
    database.commit()
    database.refresh(db_class)




    return db_class


@router.post("/class/bulk/", response_model=None, tags=["Class"])
async def bulk_create_class(items: list[ClassCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Class entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_class = Class(
                Attribute=item_data.Attribute            )
            database.add(db_class)
            database.flush()  # Get ID without committing
            created_items.append(db_class.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Class entities"
    }


@router.delete("/class/bulk/", response_model=None, tags=["Class"])
async def bulk_delete_class(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Class entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_class = database.query(Class).filter(Class.id == item_id).first()
        if db_class:
            database.delete(db_class)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Class entities"
    }

@router.put("/class/{class_id}/", response_model=None, tags=["Class"])
async def update_class(class_id: int, class_data: ClassCreate, database: Session = Depends(get_db)) -> Class:
    db_class = database.query(Class).filter(Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    setattr(db_class, 'Attribute', class_data.Attribute)
    database.commit()
    database.refresh(db_class)

    return db_class


@router.delete("/class/{class_id}/", response_model=None, tags=["Class"])
async def delete_class(class_id: int, database: Session = Depends(get_db)):
    db_class = database.query(Class).filter(Class.id == class_id).first()
    if db_class is None:
        raise HTTPException(status_code=404, detail="Class not found")
    # Snapshot the columns before deleting: cascading the association-class
    # links loads relationship collections whose back-references would make
    # the JSON encoder recurse endlessly on the live object.
    deleted_class = {
        attr.key: getattr(db_class, attr.key)
        for attr in db_class.__mapper__.column_attrs
    }
    database.delete(db_class)
    database.commit()
    return deleted_class




