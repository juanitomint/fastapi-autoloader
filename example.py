# Example usage of fastapi-autoloader

from fastapi import FastAPI

from fastapi_dynamic_router import DynamicRouter

app = FastAPI()

# Initialize the dynamic router, pointing to your controllers directory
router = DynamicRouter(target_dir="controllers")
router.load(app)

# Run with: uvicorn main:app --reload
