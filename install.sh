#!/bin/bash
set -e

COMMANDS_DIR="$HOME/.claude/commands"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$COMMANDS_DIR"

# Remove links to skills that no longer exist in this repo
for link in "$COMMANDS_DIR/"*.md; do
    [ -L "$link" ] || continue
    target=$(readlink "$link")
    if [[ "$target" == "$SCRIPT_DIR/commands/"* && ! -e "$target" ]]; then
        rm "$link"
        filename=$(basename "$link")
        echo "Removed: /${filename%.md}"
    fi
done

for file in "$SCRIPT_DIR/commands/"*.md; do
    filename=$(basename "$file")
    ln -sf "$file" "$COMMANDS_DIR/$filename"
    echo "Installed: /${filename%.md}"
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
echo "Done. Restart Claude Code to activate the commands."
echo "Future 'git pull' will auto-install new skills."
