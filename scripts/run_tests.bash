#!/bin/bash
CYAN='\033[36m'
MAGENTA='\033[35m'
NO_COLOR='\033[0m'

SEPARATOR="=============================="
DIRS=("checker" "auth" "api")

run_test() {
    go test -v ./... 2>&1 | grep -v "no test files" 
    cd -> /dev/null
    echo ${SEPARATOR}
}


echo -e "${CYAN}Running all tests ${NO_COLOR}"
echo ${SEPARATOR}

for dir in "${DIRS[@]}";do
    echo -e "${MAGENTA}${dir} ${NO_COLOR}" 
    cd $dir && run_test
done;
