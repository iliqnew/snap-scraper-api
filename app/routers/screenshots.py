from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.requests import Request
from sqlalchemy.orm import Session

from ..dependencies import SeleniumScreenshotScraper, get_db
from .. import crud


router = APIRouter(prefix="/screenshots")
templates = Jinja2Templates(directory="app/templates")


@router.post("/")
async def scrape(scraper: SeleniumScreenshotScraper, db: Session = Depends(get_db)):
    """
    Scrape the given URLs.
    Save the screenshots locally and the screenshots ID to the database.
    """
    async for screenshot in scraper.scrape():
        crud.create_screenshot(db, screenshot)
    return {"scrape_id": screenshot.scrape_id}


@router.get("/{scrape_id}")
async def get_screenshots(
    request: Request, scrape_id: str, db: Session = Depends(get_db)
):
    # get the files from database
    screenshots = crud.get_screenshots(db, scrape_id)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "scrape_id": scrape_id, "screenshots": screenshots},
    )


@router.get("/{scrape_id}/{file_name}")
async def get_screenshot(request: Request, scrape_id: str, file_name: str):
    return FileResponse(f"data/{file_name}", media_type="image/png", filename=file_name)
