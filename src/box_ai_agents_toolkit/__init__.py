from box_sdk_gen import (
    BoxClient,  # noqa: F401
    BoxSDKError,  # noqa: F401
    File,  # noqa: F401
    Folder,  # noqa: F401
    SearchForContentContentTypes,  # noqa: F401
)

sdk = ["BoxClient", "BoxSDKError", "File", "Folder", "SearchForContentContentTypes"]


from box_ai_agents_toolkit.box_api_ai import (  # noqa: E402
    box_claude_ai_agent_ask,  # noqa: F401
    box_claude_ai_agent_extract,  # noqa: F401
    box_file_ai_ask,  # noqa: F401
    box_file_ai_extract,  # noqa: F401
    box_file_ai_extract_structured,  # noqa: F401
    box_folder_ai_ask,  # noqa: F401
    box_folder_ai_extract,  # noqa: F401
    box_folder_ai_extract_structured,  # noqa: F401
    box_hubs_ai_ask,  # noqa: F401
    box_multi_file_ai_ask,  # noqa: F401
    box_multi_file_ai_extract,  # noqa: F401
    box_multi_file_ai_extract_structured,  # noqa: F401
)

ai = [
    "box_file_ai_ask",
    "box_file_ai_extract",
    "box_file_ai_extract_structured",
    "box_claude_ai_agent_ask",
    "box_claude_ai_agent_extract",
    "box_folder_ai_ask",
    "box_folder_ai_extract",
    "box_folder_ai_extract_structured",
    "box_hubs_ai_ask",
    "box_multi_file_ai_ask",
    "box_multi_file_ai_extract",
    "box_multi_file_ai_extract_structured",
]

from box_ai_agents_toolkit.box_api_file import (  # noqa: E402
    box_file_download,  # noqa: F401
    box_file_get_by_id,  # noqa: F401
    box_file_text_extract,  # noqa: F401
    box_upload_file,  # noqa: F401
)

file = [
    "box_file_download",
    "box_file_get_by_id",
    "box_file_text_extract",
    "box_upload_file",
]

from box_ai_agents_toolkit.box_api_folder import (  # noqa: E402
    box_create_folder,  # noqa: F401
    box_delete_folder,  # noqa: F401
    box_folder_list_content,  # noqa: F401
    box_update_folder,  # noqa: F401
)

folder = [
    "box_create_folder",
    "box_folder_list_content",
    "box_update_folder",
    "box_delete_folder",
]


from box_ai_agents_toolkit.box_api_search import (  # noqa: E402
    box_locate_folder_by_name,  # noqa: F401
    box_search,  # noqa: F401
)

search = ["box_search", "box_locate_folder_by_name"]

from box_ai_agents_toolkit.box_api_util_classes import (  # noqa: E402
    BoxFileExtended,  # noqa: F401
    DocumentFiles,  # noqa: F401
    ImageFiles,  # noqa: F401
)

util_classes = ["ImageFiles", "BoxFileExtended", "DocumentFiles"]

from box_ai_agents_toolkit.box_authentication import (  # noqa: E402
    authorize_app,  # noqa: F401
    get_auth_config,  # noqa: F401
    get_ccg_client,  # noqa: F401
    get_ccg_config,  # noqa: F401
    get_oauth_client,  # noqa: F401
)

auth = [
    "get_auth_config",
    "get_ccg_config",
    "get_ccg_client",
    "get_oauth_client",
    "authorize_app",
]

from .box_api_docgen import (  # noqa: E402
    box_docgen_create_batch,  # noqa: F401
    box_docgen_create_batch_from_user_input,  # noqa: F401
    box_docgen_get_job_by_id,  # noqa: F401
    box_docgen_list_jobs,  # noqa: F401
    box_docgen_list_jobs_by_batch,  # noqa: F401
)

docgen = [
    "box_docgen_get_job_by_id",
    "box_docgen_list_jobs",
    "box_docgen_list_jobs_by_batch",
    "box_docgen_create_batch",
    "box_docgen_create_batch_from_user_input",
]
from .box_api_docgen_template import (  # noqa: E402
    box_docgen_template_create,  # noqa: F401
    box_docgen_template_delete,  # noqa: F401
    box_docgen_template_get_by_id,  # noqa: F401
    box_docgen_template_list,  # noqa: F401
    box_docgen_template_list_jobs,  # noqa: F401
    box_docgen_template_list_tags,  # noqa: F401
)

docgen_template = [
    "box_docgen_template_create",
    "box_docgen_template_list",
    "box_docgen_template_delete",
    "box_docgen_template_get_by_id",
    "box_docgen_template_list_tags",
    "box_docgen_template_list_jobs",
]
from .box_api_metadata_template import (  # noqa: E402
    box_metadata_template_create,  # noqa: F401
    box_metadata_template_delete,  # noqa: F401
    box_metadata_template_get,  # noqa: F401
    box_metadata_template_get_by_id,  # noqa: F401
    box_metadata_template_list,  # noqa: F401
    box_metadata_template_list_by_instance_id,  # noqa: F401
    box_metadata_template_update,  # noqa: F401
)

metadata_template = [
    "box_metadata_template_create",
    "box_metadata_template_list",
    "box_metadata_template_get",
    "box_metadata_template_get_by_id",
    "box_metadata_template_update",
    "box_metadata_template_delete",
    "box_metadata_template_list_by_instance_id",
]


__all__ = []

__all__.extend(sdk)
__all__.extend(ai)
__all__.extend(file)
__all__.extend(folder)
__all__.extend(search)
__all__.extend(auth)
__all__.extend(docgen)
__all__.extend(docgen_template)
__all__.extend(metadata_template)
__all__.extend(util_classes)
