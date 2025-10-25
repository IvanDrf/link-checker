#!/bin/bash

CYAN='\033[36m'
MAGENTA='\033[35m'
GREEN='\033[32m'
RED='\033[31m'
NO_COLOR='\033[0m'

SEPARATOR="=============================="
DIRS=("checker" "auth" "api")

run_test() {
    local has_failures=false
    
    while IFS= read -r line; do
        if [[ $line == *"PASS"* ]]; then
            echo -e "${GREEN}$line${NO_COLOR}"
        elif [[ $line == *"FAIL"* ]]; then 
            echo -e "${RED}$line${NO_COLOR}"
            has_failures=true
        elif [[ $line != *"no test files"* ]]; then 
            echo "$line"
        fi
    done < <(go test -v ./... 2>&1)
    
    cd - > /dev/null
    echo "${SEPARATOR}"
    
    if [[ $has_failures == true ]]; then
        return 1
    fi
    return 0
}

echo -e "${CYAN}Running all tests ${NO_COLOR}"
echo "${SEPARATOR}"

for dir in "${DIRS[@]}"; do
    echo -e "${MAGENTA}${dir} ${NO_COLOR}" 
    cd "$dir" && run_test
    if [ $? -ne 0 ]; then
        echo -e "${RED}Tests failed in $dir, stopping...${NO_COLOR}"
        exit 1
    fi
done

echo -e "${GREEN}All tests passed!${NO_COLOR}"