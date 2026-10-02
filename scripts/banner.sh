#!/usr/bin/env bash
# Print retro DOS banner with authentic VGA colors
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BANNER_FILE="$SCRIPT_DIR/../docs/assets/banner.txt"

# If stdout is a TTY and supports color, print with DOS blue/cyan/white styling
if [ -t 1 ]; then
    BLUE_BG="\033[44m"
    CYAN="\033[1;36m"
    WHITE="\033[1;37m"
    YELLOW="\033[1;33m"
    RESET="\033[0m"

    echo ""
    while IFS= read -r line; do
        if [[ "$line" =~ ╔.*╗|╚.*╝ ]]; then
            echo -e "${BLUE_BG}${CYAN}${line}${RESET}"
        elif [[ "$line" =~ SOFTWARE\ ENGINEERING ]]; then
            echo -e "${BLUE_BG}${YELLOW}${line}${RESET}"
        elif [[ "$line" =~ Claude\ Code ]]; then
            echo -e "${BLUE_BG}${CYAN}${line}${RESET}"
        elif [[ "$line" =~ ║[[:space:]]*║ ]]; then
            echo -e "${BLUE_BG}${CYAN}${line}${RESET}"
        else
            echo -e "${BLUE_BG}${WHITE}${line}${RESET}"
        fi
    done < "$BANNER_FILE"
    echo ""
else
    # Raw output for pipes / non-TTY
    cat "$BANNER_FILE"
fi
