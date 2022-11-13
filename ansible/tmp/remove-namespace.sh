#!/bin/bash
if [[ $# -ne 1 ]]; then
  echo "Please input only namespace name"
  exit 1
fi
ns=$1
echo $ns
kubectl get ns ${ns} -o json > tmp.json
cat ./tmp.json | jq 'del(.spec.finalizers[])' > ./modify.json
kubectl replace --raw "/api/v1/namespaces/${ns}/finalize" -f ./modify.json
rm -f tmp.json modify.json
