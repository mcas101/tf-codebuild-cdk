#!/bin/bash
npx cdk diff "*" 2>&1 | tee cdk.diff
grep "There were no differences" cdk.diff && echo "no diffs found" || echo "diffs found"
