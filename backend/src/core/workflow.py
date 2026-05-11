"""
LangGraph workflow for paper processing.
"""

import time
from typing import Dict

from langgraph.graph import StateGraph, END

from src.agents.prompt_p1 import P1Agent
from src.agents.prompt_p2 import P2Agent
from src.agents.prompt_p3 import P3Agent
from src.agents.prompt_p4 import P4Agent
from src.core.config import get_settings
from src.core.state import WorkflowState
from src.services.gamma_client import get_gamma_client
from src.services.image_server import start_image_server, stop_image_server
from src.utils.logger import get_logger

logger = get_logger(__name__)


# Node functions


async def prepare_images_node(state: WorkflowState) -> WorkflowState:
    """Start image server and generate image URLs.

    Args:
        state: Current workflow state

    Returns:
        Updated state with image_urls and image_server_process
    """
    start_time = time.time()
    logger.info("Node: prepare_images")

    try:
        server, image_urls = await start_image_server(state["image_paths"])

        state["image_urls"] = image_urls
        state["image_server_process"] = server
        state["execution_time"]["prepare_images"] = time.time() - start_time

        logger.info(f"Image server started with {len(image_urls)} images")

    except Exception as e:
        error_msg = f"Failed to start image server: {e}"
        logger.error(error_msg)
        state["errors"].append(error_msg)
        state["execution_time"]["prepare_images"] = time.time() - start_time

    return state


async def execute_p1_node(state: WorkflowState) -> WorkflowState:
    """Execute P1 agent to generate Gamma markdown.

    Args:
        state: Current workflow state

    Returns:
        Updated state with p1_markdown
    """
    start_time = time.time()
    logger.info("Node: execute_p1")

    try:
        agent = P1Agent()
        result = await agent.execute(
            paper_md=state["paper_md"],
            paper_meta=state["paper_meta"],
            image_paths=state["image_paths"],
            image_urls=state["image_urls"],
        )

        state["p1_markdown"] = result
        state["execution_time"]["execute_p1"] = time.time() - start_time

        logger.info(f"P1 completed, generated {len(result)} chars")

    except Exception as e:
        error_msg = f"P1 agent failed: {e}"
        logger.error(error_msg)
        state["errors"].append(error_msg)
        state["execution_time"]["execute_p1"] = time.time() - start_time

    return state


async def call_gamma_node(state: WorkflowState) -> Dict:
    """Call Gamma API to generate PPT.

    Args:
        state: Current workflow state

    Returns:
        Dict with only gamma_ppt_url, errors, and execution_time updates
    """
    start_time = time.time()
    logger.info("Node: call_gamma")

    result_dict = {
        "execution_time": {},
        "errors": [],
    }

    try:
        if not state.get("p1_markdown"):
            raise ValueError("P1 markdown not available")

        settings = get_settings()
        client = get_gamma_client()

        # Generate presentation with export
        response = await client.generate_presentation(
            input_text=state["p1_markdown"],
            card_split="inputTextBreaks",
            export_as=settings.gamma_export_format,
            max_wait_time=180,  # 3 minutes max wait
            poll_interval=5,  # Check every 5 seconds
        )

        # Extract PPT URL from response
        gamma_url = response.get("gammaUrl")
        if gamma_url:
            result_dict["gamma_ppt_url"] = gamma_url
            logger.info(f"Gamma PPT generated: {gamma_url}")
        else:
            logger.warning(f"No gammaUrl in response: {response}")
            result_dict["gamma_ppt_url"] = None

        # Download exported file if available
        export_url = response.get("exportUrl")
        if export_url:
            paper_id = state.get("paper_id", "unknown")
            export_format = settings.gamma_export_format or "pdf"
            output_path = settings.output_dir / paper_id / f"gamma_presentation.{export_format}"

            downloaded_path = await client.download_export(export_url, output_path)
            result_dict["gamma_export_path"] = str(downloaded_path)
            logger.info(f"Gamma export downloaded: {downloaded_path}")
        else:
            logger.warning("No exportUrl in response - file not downloaded")

        result_dict["execution_time"]["call_gamma"] = time.time() - start_time

    except Exception as e:
        error_msg = f"Gamma API call failed: {e}"
        logger.error(error_msg)
        result_dict["errors"].append(error_msg)
        result_dict["execution_time"]["call_gamma"] = time.time() - start_time

    return result_dict


async def execute_p2_node(state: WorkflowState) -> Dict:
    """Execute P2 agent to generate deep analysis.

    Args:
        state: Current workflow state

    Returns:
        Dict with only p2_document, errors, and execution_time updates
    """
    start_time = time.time()
    logger.info("Node: execute_p2")

    result_dict = {
        "execution_time": {},
        "errors": [],
    }

    try:
        if not state.get("p1_markdown"):
            raise ValueError("P1 markdown not available")

        agent = P2Agent()
        result = await agent.execute(
            p1_markdown=state["p1_markdown"],
            paper_md=state["paper_md"],
        )

        result_dict["p2_document"] = result
        result_dict["execution_time"]["execute_p2"] = time.time() - start_time

        logger.info(f"P2 completed, generated {len(result)} chars")

    except Exception as e:
        error_msg = f"P2 agent failed: {e}"
        logger.error(error_msg)
        result_dict["errors"].append(error_msg)
        result_dict["execution_time"]["execute_p2"] = time.time() - start_time

    return result_dict


async def execute_p3_node(state: WorkflowState) -> Dict:
    """Execute P3 agent to generate technical article.

    Args:
        state: Current workflow state

    Returns:
        Dict with only p3_article, errors, and execution_time updates
    """
    start_time = time.time()
    logger.info("Node: execute_p3")

    result_dict = {
        "execution_time": {},
        "errors": [],
    }

    try:
        if not state.get("p1_markdown"):
            raise ValueError("P1 markdown not available")

        agent = P3Agent()
        result = await agent.execute(
            p1_markdown=state["p1_markdown"],
            paper_md=state["paper_md"],
        )

        result_dict["p3_article"] = result
        result_dict["execution_time"]["execute_p3"] = time.time() - start_time

        logger.info(f"P3 completed, generated {len(result)} chars")

    except Exception as e:
        error_msg = f"P3 agent failed: {e}"
        logger.error(error_msg)
        result_dict["errors"].append(error_msg)
        result_dict["execution_time"]["execute_p3"] = time.time() - start_time

    return result_dict


async def execute_p4_node(state: WorkflowState) -> Dict:
    """Execute P4 agent to generate speech script.

    Args:
        state: Current workflow state

    Returns:
        Dict with only p4_script, errors, and execution_time updates
    """
    start_time = time.time()
    logger.info("Node: execute_p4")

    result_dict = {
        "execution_time": {},
        "errors": [],
    }

    try:
        if not state.get("p1_markdown"):
            raise ValueError("P1 markdown not available")

        agent = P4Agent()
        result = await agent.execute(
            p1_markdown=state["p1_markdown"],
            paper_md=state["paper_md"],
        )

        result_dict["p4_script"] = result
        result_dict["execution_time"]["execute_p4"] = time.time() - start_time

        logger.info(f"P4 completed, generated {len(result)} chars")

    except Exception as e:
        error_msg = f"P4 agent failed: {e}"
        logger.error(error_msg)
        result_dict["errors"].append(error_msg)
        result_dict["execution_time"]["execute_p4"] = time.time() - start_time

    return result_dict


async def finalize_node(state: WorkflowState) -> WorkflowState:
    """Finalize workflow: stop image server and log results.

    Args:
        state: Current workflow state

    Returns:
        Final state
    """
    start_time = time.time()
    logger.info("Node: finalize")

    # Stop image server
    if state.get("image_server_process"):
        try:
            stop_image_server(state["image_server_process"])
            logger.info("Image server stopped")
        except Exception as e:
            logger.warning(f"Error stopping image server: {e}")

    state["execution_time"]["finalize"] = time.time() - start_time

    # Log summary
    total_time = sum(state["execution_time"].values())
    logger.info(f"Workflow completed in {total_time:.2f} seconds")
    logger.info(f"Execution times: {state['execution_time']}")

    if state["errors"]:
        logger.warning(f"Workflow completed with {len(state['errors'])} errors")
        for error in state["errors"]:
            logger.error(f"  - {error}")
    else:
        logger.info("Workflow completed successfully with no errors")

    return state


def create_workflow() -> StateGraph:
    """Create the LangGraph workflow.

    Returns:
        Compiled StateGraph
    """
    logger.info("Creating LangGraph workflow")

    # Create graph
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("prepare_images", prepare_images_node)
    workflow.add_node("execute_p1", execute_p1_node)
    workflow.add_node("call_gamma", call_gamma_node)
    workflow.add_node("execute_p2", execute_p2_node)
    workflow.add_node("execute_p3", execute_p3_node)
    workflow.add_node("execute_p4", execute_p4_node)
    workflow.add_node("finalize", finalize_node)

    # Define edges (execution flow)
    workflow.set_entry_point("prepare_images")
    workflow.add_edge("prepare_images", "execute_p1")

    # After P1, branch to all parallel tasks
    workflow.add_edge("execute_p1", "call_gamma")
    workflow.add_edge("execute_p1", "execute_p2")
    workflow.add_edge("execute_p1", "execute_p3")
    workflow.add_edge("execute_p1", "execute_p4")

    # All parallel tasks converge to finalize
    workflow.add_edge("call_gamma", "finalize")
    workflow.add_edge("execute_p2", "finalize")
    workflow.add_edge("execute_p3", "finalize")
    workflow.add_edge("execute_p4", "finalize")

    workflow.add_edge("finalize", END)

    logger.info("Workflow created successfully")

    return workflow.compile()


async def run_workflow(initial_state: WorkflowState) -> WorkflowState:
    """Run the workflow with given initial state.

    Args:
        initial_state: Initial workflow state

    Returns:
        Final workflow state
    """
    logger.info(f"Starting workflow for paper: {initial_state['paper_id']}")

    workflow = create_workflow()

    try:
        final_state = await workflow.ainvoke(initial_state)
        logger.info("Workflow execution completed")
        return final_state

    except Exception as e:
        logger.error(f"Workflow execution failed: {e}")
        raise
