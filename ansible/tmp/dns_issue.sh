kubectl create -f https://k8s.io/examples/admin/dns/busybox.yaml
kubectl get pods busybox
kubectl exec -ti busybox -- nslookup kubernetes.default
#iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
#kubectl delete pod -n kube-system -l k8s-app=kube-dns
