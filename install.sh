#!/bin/bash
set -e

SKILLS_DIR="$HOME/.claude/skills"
COMMANDS_DIR="$HOME/.claude/commands"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$SKILLS_DIR"

# Remove links to skills that no longer exist in this repo (renamed or deleted),
# including the old single-file commands in ~/.claude/commands/
for link in "$SKILLS_DIR/"* "$COMMANDS_DIR/"*.md; do
    [ -L "$link" ] || continue
    target=$(readlink "$link")
    if [[ "$target" == "$SCRIPT_DIR/"* && ! -e "$target" ]]; then
        rm "$link"
        name=$(basename "$link")
        echo "Removed: /${name%.md}"
    fi
done

for skill in "$SCRIPT_DIR/skills/"*/; do
    [ -f "$skill/SKILL.md" ] || continue
    name=$(basename "$skill")
    target="$SKILLS_DIR/$name"
    if [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "Skipped: /$name (a skill with this name already exists in $SKILLS_DIR and is not managed by this repo)"
        continue
    fi
    ln -sfn "${skill%/}" "$target"
    echo "Installed: /$name"
done

# Install post-merge hook so git pull auto-installs new skills
HOOK_DIR="$SCRIPT_DIR/.git/hooks"
HOOK_FILE="$HOOK_DIR/post-merge"

mkdir -p "$HOOK_DIR"
cat > "$HOOK_FILE" << 'EOF'
#!/bin/bash
"$(git rev-parse --show-toplevel)/install.sh"
EOF
chmod +x "$HOOK_FILE"

echo ""
echo "Done. Restart Claude Code to activate the skills."
echo "Future 'git pull' will auto-install new skills."
