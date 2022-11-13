
# ZK:

Refs: https://zookeeper.apache.org/doc/r3.4.8/zookeeperAdmin.html

- Do not purge snapshots manually, deleteing snapshots manually could result in data lose
- CPU load peaks up every hours, check if /etc/crontab any hourly jobs running, radomize the start time accross different zookeeper servers
- If running?
  $ echo 4WORDS | nc ZK_IP 2181
  - if the command shows no output, then it means that zk server are not running
  - Node count <=== if too much node
  - Connections <=== if contains in result
- Throughput increases and latency decreases when transaction logs reside on dedicated log devices.


### 4words cmmand
  - conf, show infromation
  - ruok: Test if server if running in a non-error state. The server will respond with imok if it is running. Otherwise it will not respond at all.
  - crst: Reset connection/session statistics for all connections
  - srst: Reset server statistics.
  - wchs: List brief information on watches for the server
  - wchc: use it carefully! This outputs a list of session(connections) with associated watches(path)
  - wchp: use it carefully! This outputs a list of paths(znodes) with associated sessions.
  - stat: Lists brief details for the server and connected clients.
  - mntr: output a list of variables that could be used for monitoring the health of the cluster

### Things to Avoid
  - inconsistent lists of servers
  - incorrect placement of transaction log (performance issue): Putting the log on a busy device will adversely effect performance.
  - incorrect Java heap size, DON'T SWAP.
  - Be conservative in your estimates; you should use a 3G heap for a 4G machine.

### File system
  - Data Directory
    - myid (Int: Server ID)
    - snapshot.zxid (Transaction ID): holds the fuzzy snapshot of a data tree.
  - Log Directory
    - transaction logs: Before any update take place, Zookeeper ensures that the transaction that represents the update is written to no-volatile storage. A new log file is started each time a snapshot is begun; the log file's suffix is the first zxid written to that log

  Check data & log size

    $ echo dirs | nc localhost 2181

### zkCli.sh
  - ls -R /
  - create /jason_test mydata

### Daemons (JPS)
  - QuorunPeerMain


# Hadoop

### Daemons (JPS)
  - NameNode
  - DataNode
  - ResourceManager
  - SecondaryNameNode *namenode util, not really a slaver*
  - DataNode

# k8s

  - RBAC: Role Base Access Control
  - CR: **Kind: Jason**, Jason is custom resource
  - CRD: custom resource definitions, the full yaml document that use **Kind: Jason**
  - GVK: Group Version Kind
  - GVR: Group version Resource
  - Operator: An operator is an application-specific controller that extends the Kubernetes API to create, and manage instances of complex applications on behalf of a Kubernetes user.
  
  CSI (Container Storage Interface)

### k8s webhooks

  A type of HTTP callback registered to the Kubernetes API server. When a specific event occurs,
  the kubernetes API queries registered webhooks and forward a message.

  Webhooks are divided into mutating webhooks and validating webhooks.
  Mutating webhooks modify input object,whereas validating webhooks only read input objects.

  An Operator is a combination of a CRD, webhook, and controller used to implement user business logic.

### k8s command

  lis all apis
   
     $ kubectl get --raw /

  check api details

     $ kubeclt get --raw /apis/batch/v1 | jp .

# Ceph

  RADOS (Reliabel Autonomic Distrbuted Object Store)

  Ceph FS

  3 components:
  - monitor
  - OSDs (Object Storage Devices)
  - MDS (Ceph MetaData Server)
  
  $ vgscan
  $ vgremove
  $ vgdisplay
  $ wipefs -a /dev/nvme1n1
  $ ceph orch apply osd --all-available-devices
  $ ceph orch apply osd --all-available-devices --unmanaged=true

  device busy
  dmsetup remove –force [lvm]
  sgdisk –z /dev/sdc

Refs:
- https://www.alibabacloud.com/blog/getting-started-with-kubernetes-%7C-operator-and-operator-framework_596320
- Ceph https://access.redhat.com/documentation/zh-cn/red_hat_ceph_storage/5/pdf/troubleshooting_guide/red_hat_ceph_storage-5-troubleshooting_guide-zh-cn.pdf