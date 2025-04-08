from app.schemas.user import (
    CreateUser,
    ResponseUser,
    PatchUpdateUser,
    ResponseUserInfo,
    ResponseUserWithProjects,
)
from app.schemas.project import (
    CreateProject,
    ResponseProject,
    PatchUpdateProject,
    ResponseProjectWithOutID,
)
from app.schemas.task import (
    CreateTask,
    ResponseTask,
    PartialUpdateTask,
    ResponseTaskWithOutID,
)

ResponseUserInfo.model_rebuild()
ResponseUserWithProjects.model_rebuild()
