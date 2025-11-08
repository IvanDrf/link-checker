#!/bin/bash
CYAN='\033[36m'
MAGENTA='\033[35m'
GREEN='\033[32m'
RED='\033[31m'
NO_COLOR='\033[0m'

SEPARATOR="=============================="
DIRS=("checker" "auth" "api")


run_golang_tests() {
    go test -v ./... | while IFS= read -r line; do
        if [[ $line == *"PASS"* ]]; then
            echo -e "${GREEN}$line${NO_COLOR}"
        elif [[ $line == *"FAIL"* ]]; then 
            echo -e "${RED}$line${NO_COLOR}"

        elif [[ $line != *"no test files"* ]]; then 
            echo "$line"
        fi
    done;

    cd -> /dev/null
    echo ${SEPARATOR}
}


echo -e "${CYAN}Running all tests ${NO_COLOR}"
echo ${SEPARATOR}

echo -e "${MAGENTA}Python-Bot${NO_COLOR}"
cd  ./bot
pytest
cd  ..

for dir in "${DIRS[@]}";do
    echo -e "${MAGENTA}${dir} ${NO_COLOR}" 
    cd $dir && run_golang_tests
done;
