from src.backend.presentation.api.v1.funnel.routers.funnel import router
from src.backend.presentation.api.v1.funnel.routers.funnel_stage import router as stage_router

router.include_router(stage_router)