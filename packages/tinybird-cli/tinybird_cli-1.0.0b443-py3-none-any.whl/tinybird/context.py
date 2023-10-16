from contextvars import ContextVar


workspace_id: ContextVar[str] = ContextVar('workspace_id')
workspace: ContextVar[str] = ContextVar('workspace')
table_id: ContextVar[str] = ContextVar('table_id')
hfi_frequency: ContextVar[float] = ContextVar('hfi_frequency')
disable_template_security_validation: ContextVar[bool] = ContextVar('disable_template_security_validation')
origin: ContextVar[str] = ContextVar('origin')
request_id: ContextVar[str] = ContextVar('request_id')
engine: ContextVar[str] = ContextVar('engine')
wait_parameter: ContextVar[bool] = ContextVar('wait_parameter')
