from app.schemas.user import (
    CreateUser,
    ResponseUser,
    PatchUpdateUser,
    ResponseUserInfo,
    ResponseUserWithProjects,
    UserSchemaLogin,
    UserSchemaResponse,
)
from app.schemas.project import (
    CreateProject,
    ResponseProject,
    PatchUpdateProject,
    ResponseProjectWithOutID,
    ResponseProjectWithTasksInfo,
    ResponseProjectWithUsersInfo,
)
from app.schemas.task import (
    CreateTask,
    ResponseTask,
    PartialUpdateTask,
    ResponseTaskWithOutID,
    ResponseTaskWithUserInfo,
    ResponseTaskInfo,
    ResponseTaskWithProjectInfo,
)
from app.schemas.token import TokenResponse

ResponseUserInfo.model_rebuild()
ResponseUserWithProjects.model_rebuild()
ResponseTaskWithUserInfo.model_rebuild()
ResponseProjectWithUsersInfo.model_rebuild()
ResponseProjectWithTasksInfo.model_rebuild()
ResponseTaskWithProjectInfo.model_rebuild()
