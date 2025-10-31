import reflex as rx
from typing import TypedDict, Literal
import datetime
from enum import Enum


class WorkflowStage(Enum):
    DRAFT = "Draft"
    EXTRACTING_SPEC = "Extracting Specification"
    PLANNING_FILES = "Planning File Structure"
    GENERATING_CODE = "Generating Code"
    VALIDATING = "Validating Code"
    READY_FOR_REVIEW = "Ready for Review"
    APPROVED = "Approved"
    DEPLOYING = "Deploying"
    DEPLOYED = "Deployed"
    FAILED = "Failed"


class AgentType(Enum):
    ORCHESTRATOR = "Orchestrator"
    SPEC_EXTRACTOR = "Spec Extractor"
    FILE_PLANNER = "File Planner"
    CODE_GENERATOR = "Code Generator"
    VERIFIER = "Verifier"
    DEPLOYER = "Deployer"


class AgentLog(TypedDict):
    agent: str
    timestamp: str
    message: str
    details: dict | None


class AgentState(rx.State):
    current_project_id: str | None = None
    current_workflow_stage: WorkflowStage = WorkflowStage.DRAFT
    current_agent: AgentType | None = None
    workflow_progress: float = 0.0
    agent_logs: list[AgentLog] = []
    agent_outputs: dict = {}

    def _add_log(self, agent: AgentType, message: str, details: dict | None = None):
        log_entry = AgentLog(
            agent=agent.value,
            timestamp=datetime.datetime.now().isoformat(),
            message=message,
            details=details,
        )
        self.agent_logs.append(log_entry)

    @rx.event
    def start_spec_extraction(self, project_id: str):
        self.current_project_id = project_id
        self.current_workflow_stage = WorkflowStage.EXTRACTING_SPEC
        self.current_agent = AgentType.SPEC_EXTRACTOR
        self.workflow_progress = 10.0
        self._add_log(
            AgentType.ORCHESTRATOR,
            f"Starting specification extraction for project {project_id}.",
        )

    @rx.event
    def complete_spec_extraction(self, spec: dict):
        self.agent_outputs["store_spec"] = spec
        self.current_workflow_stage = WorkflowStage.PLANNING_FILES
        self.current_agent = AgentType.FILE_PLANNER
        self.workflow_progress = 25.0
        self._add_log(
            AgentType.SPEC_EXTRACTOR,
            "Successfully extracted store specification.",
            {"spec_keys": list(spec.keys())},
        )
        self._add_log(AgentType.ORCHESTRATOR, "Proceeding to file structure planning.")

    @rx.event
    def reset_workflow(self):
        self.current_workflow_stage = WorkflowStage.DRAFT
        self.current_agent = None
        self.workflow_progress = 0.0
        self.agent_logs = []
        self.agent_outputs = {}