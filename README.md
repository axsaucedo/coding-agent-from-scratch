# Progressive Coding Agent Framework

A simple educational framework demonstrating the evolution from basic LLM calls to a complete coding agent, built for teaching the internals of agentic systems.

## Overview

This project showcases how to build a "Claude-like" coding agent from scratch through 7 progressive phases, each adding core capabilities that transform a chat model into an intelligent coding assistant.

## Prerequisites

- Python 3.11+
- [ollama](https://ollama.ai/) running locally with `devstral-2-small` model
- uv (for dependency management)

## Setup

```bash
# Install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Ensure ollama is running with devstral-2-small
ollama pull devstral-2-small
ollama serve  # In another terminal
```

## Phase Progression

### Phase 1: Basic LLM Interaction
**Directory**: `1-phase-basic-llm/`
- Raw LLM communication via ollama
- Simple prompt/response handling
- Foundation for all other phases

```bash
cd 1-phase-basic-llm
python main.py
pytest test.py
```

### Phase 2: Tool Calling
**Directory**: `2-phase-tool-calling/`
- File reading capabilities
- Keyword-based tool detection
- Introduction to structured outputs

```bash
cd 2-phase-tool-calling
python main.py
pytest test.py
```

### Phase 3: Context Awareness
**Directory**: `3-phase-context-aware/`
- Python project structure analysis
- Multi-file context building
- Codebase understanding

```bash
cd 3-phase-context-aware
python main.py
pytest test.py
```

### Phase 4: Planning Agent
**Directory**: `4-phase-planning-agent/`
- Step-by-step task planning
- Development strategy creation
- Strategic thinking before action

```bash
cd 4-phase-planning-agent
python main.py
pytest test.py
```

### Phase 5: Code Creator
**Directory**: `5-phase-code-creator/`
- Python file generation from descriptions
- Working code creation
- Automatic filename assignment

```bash
cd 5-phase-code-creator
python main.py
pytest test.py
```

### Phase 6: Testing Agent
**Directory**: `6-phase-testing-agent/`
- Code validation and testing
- Syntax error detection
- Quality assurance loops

```bash
cd 6-phase-testing-agent
python main.py
pytest test.py
```

### Phase 7: Full Agent
**Directory**: `7-phase-full-agent/`
- Complete development workflow
- All capabilities integrated
- Production-ready patterns

```bash
cd 7-phase-full-agent
python main.py
pytest test.py
```

## Educational Journey

Each phase builds incrementally:

1. **Start Simple**: Raw LLM calls (Phase 1)
2. **Add Tools**: File operations and structured responses (Phase 2)
3. **Build Context**: Understanding project structure (Phase 3)
4. **Plan First**: Strategic thinking and task breakdown (Phase 4)
5. **Create Code**: Generate working Python files (Phase 5)
6. **Validate Work**: Testing and quality assurance (Phase 6)
7. **Complete Agent**: Full development workflow (Phase 7)

## Key Patterns Demonstrated

- **Tool calling** with function schemas
- **Context building** from multiple sources
- **Planning systems** for complex tasks
- **Code generation** with validation
- **Quality gates** and evaluation loops
- **Error handling** and recovery
- **Agent architecture** patterns

## Testing Strategy

Each phase includes pytest tests using an LLM judge pattern:
- End-to-end behavior validation
- Response quality assessment
- Working code verification

## Project Philosophy

This framework follows the **KEEP IT SIMPLE** principle:
- Minimal implementations without over-engineering
- Clear progression showing exactly what each phase adds
- Direct patterns that can be understood and extended
- Focus on core concepts rather than elaborate abstractions

## Use Cases

- **Learning**: Understand how coding agents work internally
- **Teaching**: Demonstrate agent architecture progression
- **Prototyping**: Base for building custom coding agents
- **Research**: Explore agent capabilities and limitations

## Architecture Notes

- Each phase is self-contained and runnable
- Common patterns are copied rather than abstracted (until Phase 7)
- LLM communication is handled consistently across phases
- Test validation uses LLM judges for flexible behavior checking

## Next Steps

After completing all phases, consider:
- Adding more sophisticated tool schemas
- Implementing memory and conversation state
- Exploring different LLM models and providers
- Building domain-specific agents for other tasks
- Adding safety and security considerations

## Contributing

This is an educational framework designed for learning and teaching. Feel free to:
- Extend phases with additional capabilities
- Add new phases showing other agent patterns
- Improve test coverage and validation
- Create variants for other programming languages

---

Built with ❤️ for understanding how coding agents really work.