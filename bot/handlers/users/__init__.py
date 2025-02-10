__all__ = ("router",)

from aiogram import Router
from .start import router as start_commands_router
from .register import router as register_commands_router
from .help import router as help_commands_router
from .set_reminder import router as set_reminder_routr
from .tracking_habit import router as tracking_habits

router = Router(name=__name__)

router.include_routers(start_commands_router, register_commands_router)
router.include_router(set_reminder_routr)
router.include_router(help_commands_router)
router.include_router(tracking_habits)
