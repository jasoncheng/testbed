kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
kubectl get pods dnsutils
echo "kubectl exec -i -t dnsutils -- nslookup kubernetes.default"
