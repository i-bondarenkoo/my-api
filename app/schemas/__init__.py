from app.schemas.user import (
    CreateUser,
    ResponseUser,
    PatchUpdateUser,
    ResponseUserWithTaskAndProject,
    ResponseUserOut,
)
from app.schemas.project import (
    CreateProject,
    ResponseProject,
    PatchUpdateProject,
    ResponseProjectOut,
    ResponseProjectWithTasksAndUsers,
)
from app.schemas.task import (
    CreateTask,
    ResponseTask,
    PartialUpdateTask,
    ResponseTaskOut,
)


ResponseUserWithTaskAndProject.model_rebuild()
ResponseProjectWithTasksAndUsers.model_rebuild()
