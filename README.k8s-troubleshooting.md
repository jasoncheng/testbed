
# kubelet.go:2448] "Error getting node" err="node not found"

  Verify containerd if version different?

  ```
  $ ansible -m shell -a "containerd --version" -i inventory/pi.inv k8s
  ```

  Leave cluster

  ```
  $ ansible-playbook k8s-node-leave.yml -i inventory/pi.inv
  ```

  Join cluster again

  ```
  $ ansible-playbook k8s-node-join-cp.yml -i inventory/pi.inv
  ```

# couldn't get current server API group list: Get "http://localhost:8080/api?timeout=32s": dial tcp 127.0.0.1:8080: connect: connection refused

  You need ~/.kube/config

  ```
  $ ansible -m file -a "src=~/.kube/config dest=~/.kube/config" -i inventory/pi.inv k8sM
  ``` 