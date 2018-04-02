#!/bin/bash
. env/bin/activate

pytest jessica -xv --ff

record_test_result.bash $?

