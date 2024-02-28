#!/bin/bash

# Set the path to the Python script file
PYTHON_FILE="src/component.py"
# Set the path to the Markdown file containing actions
MD_FILE="component_config/actions.md"

# Check if the file exists before creating it
if [ ! -e "$MD_FILE" ]; then
    touch "$MD_FILE"
    echo "File created: $MD_FILE"
else
    echo "File already exists: $MD_FILE"
fi

# Check if the flag for adding missing actions was provided
ADD_MISSING=false
if [ "$1" == "true" ]; then
    ADD_MISSING=true
fi

# Function to check if an element exists in an array
array_contains() {
    local array="$1[@]"
    local seeking=$2
    local in=1
    for element in "${!array}"; do
        if [[ $element == "$seeking" ]]; then
            in=0
            break
        fi
    done
    return $in
}

# Get all occurrences of lines containing @sync_action('XXX') from the .py file
echo "Parsing Python file to extract sync actions..."
SYNC_ACTIONS=$(grep -o "@sync_action('[^']*')" "$PYTHON_FILE" | sed "s/@sync_action('\([^']*\)')/\1/" | sort | uniq)
echo "SYNC_ACTIONS: $SYNC_ACTIONS"

# Read the content of the actions.md file into a variable and extract the list of actions
echo "Reading actions from Markdown file..."
MD_CONTENT=$(grep -o '\[.*\]' "$MD_FILE" | tr -d '[]"')
echo "MD_CONTENT: $MD_CONTENT"

# Convert the MD_CONTENT to a proper array
IFS=',' read -r -a EXISTING_ACTIONS <<< "$MD_CONTENT"

# If MD_CONTENT is empty, initialize EXISTING_ACTIONS array as empty
if [ -z "$MD_CONTENT" ]; then
    EXISTING_ACTIONS=()
fi

# Iterate over each occurrence of @sync_action('XXX')
for sync_action in $SYNC_ACTIONS; do
    found=false
    # Iterate over each action in the actions.md file
    for md_action in "${EXISTING_ACTIONS[@]}"; do
        # Check if the occurrence is found in the actions.md file
        if [ "$sync_action" == "$md_action" ]; then
            found=true
            break
        fi
    done
    # If the action is not found
    if [ "$found" == false ]; then
        echo "Warning: Action '$sync_action' not found in $MD_FILE"
        # If the flag for adding missing actions is set
        if [ "$ADD_MISSING" == true ]; then
            echo "Adding missing action '$sync_action' to $MD_FILE"
            # Add the missing action to the file
            EXISTING_ACTIONS+=("$sync_action")
        fi
    fi
done

# Convert the array to JSON format
JSON_ACTIONS=$(printf '"%s",' "${EXISTING_ACTIONS[@]}")
JSON_ACTIONS="[${JSON_ACTIONS%,}]"
echo "JSON_ACTIONS: $JSON_ACTIONS"

# Update the content of the actions.md file
echo "Updating Markdown file with actions..."
echo "$JSON_ACTIONS" > "$MD_FILE"
echo "Actions updated successfully."
