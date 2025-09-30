from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Import routers from routes/
from routes.book import router as book_router
from routes.complete_ride import router as complete_router
from routes.driver_api import router as driver_router
from routes.job_api import router as job_router
from routes.job_view_api import router as job_view_router
from routes.booking_api import router as booking_router
from routes.fare_api import router as fare_router  # optional but recommended

app = FastAPI(title="Booking Agent API")

# ✅ CORS setup for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register all routers
app.include_router(book_router)
app.include_router(complete_router)
app.include_router(driver_router)
app.include_router(job_router)
app.include_router(job_view_router)
app.include_router(booking_router)
app.include_router(fare_router)