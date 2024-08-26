from sqlalchemy.orm import Session

from . import models, schemas


def get_screenshots(db: Session, scrape_id: str):
    return (
        db.query(models.Screenshot)
        .filter(models.Screenshot.scrape_id == scrape_id)
        .all()
    )


def create_screenshot(db: Session, screenshot: schemas.ScreenshotCreate):
    db_screenshot = models.Screenshot(**screenshot.model_dump())
    db.add(db_screenshot)
    db.commit()
    db.refresh(db_screenshot)
