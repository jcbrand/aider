"""
Aider Plugin: Prose Editor
==========================

This plugin provides commands for editing written prose like papers, books,
or articles with a focus on clarity, style, and readability.

Plugin Architecture
-------------------

Aider plugins are Python files that can define:

1. Command functions: `cmd_<name>(commands, args)`
   - Become available as /<name> commands
   - `commands` is the Commands instance (has .io, .coder, .args, etc.)
   - `args` is the string of arguments passed to the command

2. Completion functions: `completions_<name>(commands)`
   - Provide tab completion suggestions for the /<name> command
   - Return a list of completion strings

3. Raw completion functions: `completions_raw_<name>(commands, document, complete_event)`
   - For advanced prompt_toolkit-style completions
   - Yield Completion objects

4. Optional metadata:
   - `__plugin_name__`: Display name for the plugin (defaults to filename)

Loading Plugins
---------------

Plugins can be loaded via:
  - Command line: `aider --plugin path/to/plugin.py`
  - Plugin directory: `aider --plugins-dir path/to/plugins/`
  - Default directories (auto-loaded if they exist):
    - ~/.aider/plugins/
    - .aider/plugins/ (in git root or cwd)

Use `/plugins` in aider to see loaded plugins.

Example Usage
-------------

    aider --plugin examples/plugins/example_prose.py my_document.md

Then in aider:
    /prose              (enters sticky prose editing mode via /ask)
    /prose improve the clarity of the introduction
    /grammar check for errors
    /plugins

"""

__plugin_name__ = "prose"


def cmd_prose(commands, args):
    """Edit prose with focus on clarity, style, and readability"""
    if not args.strip():
        commands.io.tool_output("Entering prose mode.")
        commands.io.tool_output("Your prompts will be interpreted as prose editing requests.")
        commands.io.tool_output("Use /code or /architect to return to code editing mode.")
        return commands.cmd_chat_mode("ask")

    if not commands.coder:
        commands.io.tool_error("No active coder session.")
        return

    # Create a specialized prompt for prose editing
    prose_prompt = f"""You are an expert editor helping to improve written prose.
Focus on:
- Clarity and readability
- Grammar and punctuation
- Flow and transitions between ideas
- Eliminating redundancy and wordiness
- Maintaining the author's voice and style

The user's editing request:
{args}

Please review the files in the chat and make the requested edits.
Preserve the overall structure and meaning while improving the writing quality."""

    # Use the coder to process the prose editing request
    commands.coder.run(prose_prompt)


def cmd_grammar(commands, args):
    """Check and fix grammar issues in the current files"""
    if not commands.coder:
        commands.io.tool_error("No active coder session.")
        return

    if not commands.coder.abs_fnames:
        commands.io.tool_error("No files in chat. Add files with /add first.")
        return

    grammar_prompt = """Please review all files in the chat for grammar and writing issues:

1. Subject-verb agreement errors
2. Tense consistency problems
3. Punctuation errors (commas, periods, semicolons)
4. Spelling mistakes
5. Sentence fragments or run-on sentences
6. Awkward phrasing or unclear constructions

Fix any issues you find while preserving the author's voice and style.
Make minimal changes - only fix actual errors, don't rewrite for style."""

    if args.strip():
        grammar_prompt += f"\n\nAdditional instructions: {args}"

    commands.coder.run(grammar_prompt)


def cmd_outline(commands, args):
    """Generate or analyze the outline/structure of a document"""
    if not commands.coder:
        commands.io.tool_error("No active coder session.")
        return

    if not commands.coder.abs_fnames:
        commands.io.tool_error("No files in chat. Add files with /add first.")
        return

    if not args.strip():
        # Analyze existing structure
        outline_prompt = """Please analyze the structure of the documents in the chat.
Provide:
1. A hierarchical outline showing the main sections and subsections
2. A brief summary of what each section covers
3. Suggestions for improving the document structure if applicable"""
    else:
        # Generate or modify structure based on instructions
        outline_prompt = f"""Please help with the document structure.
User's request: {args}

If creating a new outline, provide a clear hierarchical structure.
If modifying existing structure, explain the changes and update the files."""

    commands.coder.run(outline_prompt)


def completions_prose(commands):
    """Provide completions for the /prose command"""
    return [
        "improve clarity",
        "fix grammar",
        "simplify sentences",
        "enhance flow",
        "strengthen transitions",
        "reduce wordiness",
        "make more engaging",
        "improve readability",
    ]


def completions_grammar(commands):
    """Provide completions for the /grammar command"""
    return [
        "check spelling",
        "fix punctuation",
        "check tense consistency",
    ]


def completions_outline(commands):
    """Provide completions for the /outline command"""
    return [
        "analyze structure",
        "create outline for",
        "reorganize sections",
        "add section for",
    ]
