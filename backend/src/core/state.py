"""
LangGraph workflow state definition.
"""

from typing import Annotated, Dict, List, Optional

from typing_extensions import TypedDict


def merge_dicts(left: Dict, right: Dict) -> Dict:
    """Merge two dictionaries, with right taking precedence."""
    return {**left, **right}


class WorkflowState(TypedDict):
    """State for the paper processing workflow.

    This state is passed between nodes in the LangGraph workflow.
    """

    # Input materials
    paper_md: str
    """Paper markdown content"""

    paper_meta: Dict
    """Paper metadata (from JSON file)"""

    image_paths: List[str]
    """Local paths to paper images"""

    # Intermediate data
    image_urls: Annotated[Dict[str, str], merge_dicts]
    """Mapping from image filename to HTTP URL"""

    image_server_process: Optional[object]
    """Image server process handle (for cleanup)"""

    # P1 output (core dependency)
    p1_markdown: str
    """P1 generated Gamma API markdown"""

    # Final outputs (parallel execution)
    gamma_ppt_url: Optional[str]
    """URL to generated Gamma PPT"""

    gamma_export_path: Optional[str]
    """Local path to downloaded Gamma export (PDF/PPTX)"""

    p2_document: Optional[str]
    """P2 deep analysis document"""

    p3_article: Optional[str]
    """P3 technical article"""

    p4_script: Optional[str]
    """P4 speech script"""

    # Metadata
    errors: Annotated[List[str], lambda x, y: x + y]
    """Error messages collected during execution"""

    execution_time: Annotated[Dict[str, float], merge_dicts]
    """Execution time for each node in seconds"""

    paper_id: str
    """Unique identifier for this paper (e.g., arxiv ID)"""


def create_initial_state(
    paper_md: str,
    paper_meta: Dict,
    image_paths: List[str],
    paper_id: str,
) -> WorkflowState:
    """Create initial workflow state.

    Args:
        paper_md: Paper markdown content
        paper_meta: Paper metadata dictionary
        image_paths: List of local image file paths
        paper_id: Unique paper identifier

    Returns:
        Initial workflow state
    """
    return WorkflowState(
        paper_md=paper_md,
        paper_meta=paper_meta,
        image_paths=image_paths,
        paper_id=paper_id,
        image_urls={},
        image_server_process=None,
        p1_markdown="",
        gamma_ppt_url=None,
        gamma_export_path=None,
        p2_document=None,
        p3_article=None,
        p4_script=None,
        errors=[],
        execution_time={},
    )
