from pydantic import BaseModel


class BaseScreenshot(BaseModel):
    id: int
    name: str
    path: str
    scrape_id: str


class ScreenshotCreate(BaseModel):
    name: str
    path: str
    scrape_id: str


class Screenshot(ScreenshotCreate):
    class Config:
        from_attributes = True


class SeleniumScreenshotScraperCreate(BaseModel):
    start_url: str
    max_urls: int
