# AI Agents Reference

## Overview

The system uses 4 specialized AI agents (P1-P4) that generate different types of content from academic papers. All agents use Gemini 3 with thinking mode enabled.

## Base Agent

### Class: `BaseAgent`

**Location**: `src/agents/base.py`

#### Abstract Interface

```python
class BaseAgent(ABC):
    def __init__(self):
        self.gemini_client = get_gemini_client()
        self.logger = get_logger(self.__class__.__name__)

    @abstractmethod
    async def execute(self, **kwargs) -> str:
        """Execute agent logic and return generated content."""
        pass
```

#### Key Methods

- `execute(**kwargs)`: Main execution method (must be implemented)
- Automatic Gemini client initialization
- Built-in logging with agent name

---

## P1 Agent: Gamma PPT Blueprint Generator

### Purpose
Generate Gamma API-compatible markdown for PPT creation.

**Location**: `src/agents/prompt_p1.py`

### Inputs
```python
async def execute(
    paper_md: str,
    paper_meta: Dict,
    image_paths: List[str],
    image_urls: Dict[str, str],
) -> str
```

- `paper_md`: Original paper markdown content
- `paper_meta`: Paper metadata (title, authors, etc.)
- `image_paths`: List of local image paths
- `image_urls`: Mapping of filename → HTTP URL

### Output Format
Markdown with Gamma API specifications:
- Card separator: `---` (triple dash)
- Page titles: `#` or `##` headers
- Content: Bullet points (`*` or `-`)
- Images: `[IMAGE_URL]` placeholders at appropriate positions

### Example Output
```markdown
# LightRAG: Simple and Fast RAG

* Revolutionary approach to retrieval-augmented generation
* Combines graph structures with vector search
* Achieves state-of-the-art performance

[IMAGE_URL]

---

## Core Innovation

* Dual-level retrieval mechanism
* Low-level: Specific entities and relationships
* High-level: Abstract concepts and themes

---

## Methodology

* Graph-based knowledge organization
* Vector embeddings for semantic search
* Hybrid retrieval strategy

[IMAGE_URL]

---

...
```

### Prompt Template
**File**: `docs/Prompt-P1.md`

**Key Instructions**:
1. Analyze paper structure and content
2. Extract key points, innovations, methodology
3. Generate narrative framework (storyline)
4. Create detailed PPT blueprint with:
   - 15-20 slides
   - Clear hierarchy (title → sections → details)
   - Strategic image placement
   - Gamma API format compliance

### Execution Time
- Typical: 40-140 seconds
- Depends on paper length and complexity

---

## P2 Agent: Deep Analysis Generator

### Purpose
Generate comprehensive technical analysis document.

**Location**: `src/agents/prompt_p2.py`

### Inputs
```python
async def execute(
    p1_markdown: str,
    paper_md: str,
) -> str
```

- `p1_markdown`: P1 generated PPT blueprint (for structure reference)
- `paper_md`: Original paper markdown

### Output
Detailed markdown document covering:
1. **Executive Summary**: High-level overview
2. **Technical Background**: Prerequisites and context
3. **Core Innovations**: Novel contributions
4. **Methodology Deep Dive**: Detailed technical analysis
5. **Experimental Results**: Performance evaluation
6. **Limitations**: Critical assessment
7. **Future Directions**: Research implications
8. **Conclusion**: Summary of findings

### Output Size
- Typical: 20-250 KB (25,000-250,000 characters)
- Most comprehensive output

### Prompt Template
**File**: `docs/Prompt-P2.md`

### Execution Time
- Typical: 95-186 seconds
- Longest running agent

---

## P3 Agent: Technical Article Generator

### Purpose
Generate accessible technical article for broader audience.

**Location**: `src/agents/prompt_p3.py`

### Inputs
```python
async def execute(
    p1_markdown: str,
    paper_md: str,
) -> str
```

### Output
Medium-style article with:
1. **Engaging Introduction**: Hook and context
2. **Problem Statement**: Why this matters
3. **Solution Overview**: Key innovations explained simply
4. **How It Works**: Technical details made accessible
5. **Impact & Applications**: Real-world relevance
6. **Conclusion**: Takeaways

### Style Guidelines
- Clear, engaging writing
- Minimal jargon
- Concrete examples
- Accessible to technical readers without domain expertise

### Output Size
- Typical: 3-10 KB (3,000-10,000 characters)
- Most concise output

### Prompt Template
**File**: `docs/Prompt-P3.md`

### Execution Time
- Typical: 28-114 seconds

---

## P4 Agent: Speech Script Generator

### Purpose
Generate presentation speech script for conference talks.

**Location**: `src/agents/prompt_p4.py`

### Inputs
```python
async def execute(
    p1_markdown: str,
    paper_md: str,
) -> str
```

### Output
Spoken presentation script with:
1. **Opening**: Attention grabber and introduction
2. **Problem & Motivation**: Why audience should care
3. **Core Content**: Main technical points
4. **Visual Cues**: References to slides/figures
5. **Transitions**: Smooth flow between topics
6. **Q&A Prep**: Anticipated questions and answers
7. **Closing**: Summary and call to action

### Format
```markdown
# Speech Script: [Paper Title]

## Opening (2 minutes)

[Script text with natural speaking style...]

**[VISUAL CUE: Show title slide]**

---

## Problem Statement (3 minutes)

[Script text...]

**[VISUAL CUE: Show problem illustration]**

---

...

## Q&A Preparation

**Q: How does this compare to existing methods?**
A: [Response script...]

**Q: What are the computational requirements?**
A: [Response script...]
```

### Output Size
- Typical: 9-10 KB (9,000-10,000 characters)

### Prompt Template
**File**: `docs/Prompt-P4.md`

### Execution Time
- Typical: 38-45 seconds
- Fastest agent

---

## Agent Execution Flow

### Sequential Phase
```
prepare_images → execute_p1
```

P1 must complete first as it provides context for P2, P3, P4.

### Parallel Phase
```
         ┌─→ call_gamma (Gamma API)
         │
execute_p1 ─┼─→ execute_p2 (Deep Analysis)
         │
         ├─→ execute_p3 (Article)
         │
         └─→ execute_p4 (Script)
```

All run concurrently, max 4 parallel tasks.

---

## Common Patterns

### 1. Loading Prompt Template
```python
from src.utils.file_handler import read_prompt_template

prompt_template = read_prompt_template("Prompt-P1")
```

### 2. Gemini Client Usage
```python
from src.services.gemini_client import get_gemini_client

client = get_gemini_client()
response = await client.generate(
    prompt=filled_prompt,
    thinking_level="high"
)
```

### 3. Error Handling
```python
try:
    result = await agent.execute(**params)
    return result
except Exception as e:
    logger.error(f"Agent failed: {e}")
    raise
```

### 4. Logging
```python
self.logger.info("Executing P1 agent")
self.logger.debug(f"Input length: {len(paper_md)}")
self.logger.info(f"Generated {len(result)} chars")
```

---

## Customization Guide

### Adding a New Agent

1. **Create Agent Class**
```python
# src/agents/prompt_p5.py
from src.agents.base import BaseAgent
from typing import Dict

class P5Agent(BaseAgent):
    async def execute(
        self,
        p1_markdown: str,
        paper_md: str,
    ) -> str:
        # Load prompt template
        from src.utils.file_handler import read_prompt_template
        template = read_prompt_template("Prompt-P5")

        # Fill template with inputs
        filled_prompt = template.format(
            p1_markdown=p1_markdown,
            paper_md=paper_md
        )

        # Call Gemini
        result = await self.gemini_client.generate(
            prompt=filled_prompt,
            thinking_level="high"
        )

        return result
```

2. **Create Prompt Template**
```markdown
<!-- docs/Prompt-P5.md -->
# Your Custom Task Instructions

Given:
- P1 Markdown: {p1_markdown}
- Original Paper: {paper_md}

Generate: [Your specific output requirements]
```

3. **Add to Workflow**
```python
# src/core/workflow.py
from src.agents.prompt_p5 import P5Agent

async def execute_p5_node(state: WorkflowState) -> Dict:
    agent = P5Agent()
    result = await agent.execute(
        p1_markdown=state["p1_markdown"],
        paper_md=state["paper_md"]
    )
    return {"p5_output": result}

# In create_workflow():
workflow.add_node("execute_p5", execute_p5_node)
workflow.add_edge("execute_p1", "execute_p5")  # Parallel
workflow.add_edge("execute_p5", "finalize")
```

4. **Update State**
```python
# src/core/state.py
class WorkflowState(TypedDict):
    # ... existing fields ...
    p5_output: Optional[str]
```

---

## Performance Tips

### 1. Prompt Engineering
- Be specific about output format
- Include examples in prompts
- Use clear section markers
- Specify length constraints

### 2. Gemini Optimization
- Use `thinking_level="high"` for complex tasks
- No timeout on Gemini (it's reliable)
- Temperature=1.0 for creative outputs

### 3. Parallel Execution
- Keep agents independent (no inter-dependencies)
- Use `Dict` returns for parallel nodes
- Avoid shared state mutations

### 4. Error Recovery
- Catch exceptions at agent level
- Log detailed error context
- Continue workflow even if one agent fails
- Collect errors in `state["errors"]`
