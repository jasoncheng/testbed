# Ceph - no active mgr

rook-ceph-mgr-*YOUR_MGR_DEPLOY_NAME*
```
$ kubectl rollback restart deploy -n rook-ceph rook-ceph-mgr-a
$ kubectl rollback restart deploy -n rook-ceph rook-ceph-mgr-b
```

# Rook - how to login as root in toolbox

1. Edit deployment 

   ```
   $ kubectl edit deploy -n rook-ceph rook-ceph-tools
   ```

2. In spec.template.spec.containers.args[0] add or update securityContext, and save 

   ```
   securityContext: <--- here
     privileged: true <--- here
     runAsUser: 0 <--- here
   terminationMessagePath: /dev/termination-log
   terminationMessagePolicy: File
   ...
   ```

3. Wait for new pod launch, then you should have root permission.
   
   ```
   $ kubectl exec -it -n rook-ceph rook-ceph-tools-5976f97f97-zvhsx -- ls -al /var/lib/ceph
   ```

# Ceph - Dashboard not running

1. Find Pod id(s)
   
   ```
   $ kubectl get po -n rook-ceph
   ```

2. Use Pod id digging what's wrong w/,

   ```
   $ kubectl logs -f -n rook-ceph rook-ceph-mgr-a-78475b55c-s8wh4 -c mgr
   ```

3.  Still have no idea ? 
   
    Recovery service first by **rollback restart** mgr deploy one by one, and digging pod's container logs again, until you find the issue locate.

    ```
    $ kubectl rollback restart deploy -n rook-ceph rook-ceph-mgr-a
    ```

