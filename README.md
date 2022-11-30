
``` Welcome to JasonCheng lab, This is just my playground ```


## Head First

  For practice, for share, big data / infrastructure as code / Kubernetes / python skill / dockerized / ansible...

  My work env is **MacOS**, and server default is provision in **ubuntu 22.04** system, 

  If you try to run in different enviornment, such as RHEL based os, you should modify ansible to suit your requirements
  
  **BTW**, i'm working on *Pi4 x 5 pcs w/ CentOS7*.

## My Targets

  - **[Hadoop](https://hadoop.apache.org/)** A software for reliable, scalable, distributed computing
  - **[Hbase](https://hbase.apache.org/)** A distrbuted, scalable, big data store database
  - **[Kafka](https://kafka.apache.org/)** A distrbuted event streaming platform
  - **[Spark](https://spark.apache.org/)** A multi-language engine for executing data engineering, data sicense, and machine learning on single-mode machines or cluster
  - **[Zookeeper](https://zookeeper.apache.org/)** For manage animal ... 😂 (used by hadoop, hbase, kafka)
  - **[Kubernetes](https://kubernetes.io/)** A automating deployment, scaling, and management of containerized application
  - **[Ceph](https://ceph.com/en/)** Ceph is an open-source, distrubuted storage system.
  - **[Terraform](https://www.terraform.io/)** Infrastructure as code software
  - **[Ansible](https://www.ansible.com/)** It's the simplest way to automate IT.
  - **[Python](https://www.python.org/)** A program language, one of animal  😂
  - **[Go](https://go.dev/)** A programming language.
  - **[k8s-KEDA](https://keda.sh/)** A kubernetes based Event Driven AutoScaler
  - **[k8s-ingress-nginx](https://github.com/kubernetes/ingress-nginx)** A ingress controller for kubernetes using **[NGINX](https://www.nginx.com/)**
  - **[k8s-csi-ceph](https://github.com/ceph/ceph-csi)** ceph storag class for k8s
  - **[k8s-rook-ceph](https://rook.io/)** provision/manage ceph cluster on k8s by using rook k8s operator
  - prometheus **[blackbox-exporter](https://github.com/prometheus/blackbox_exporter)** Probing of endpoint over HTTP, HTTPS, DNS, TCP, ICMP, gRPC
  - **[Grafana/Loki](https://github.com/grafana/loki)** A horizontally-scalable, highly-available, multi-tenant log aggregation system.

<br />

## File & Directory

  | Name  | Description |
  | ----- | ----- |
  | ansible | Ansible playbook |
  | terraform | For building testing server on AWS (ubuntu 20.04) |
  | test | python code for testing infrastructure |

<br />

## AWS Infrastructure Setup

  If you already have on-premise server, please **skip** this step.

  Change terraform/variables.tf for your personal requirement,

  Default will create 3 t3.small instances(2 Core CPU and 2G Memory) with 24G EBS volumes at ap-northeast-1 region.

   ```
   $ terraform apply
   ```

  ``` Caution ``` 
  
  **t3.small** instance only have 2G memory, if you try to provision all tags, you will face to OOM issue; or maybe you can run **t3.medium** instance (4G memory) for prevent that.

  Once all server created, we will automatic generate below listed files,

   | File | Description |
   | ---- | ---- |
   | ansible/inventory/bd.inv | ansible inventory |
   | terraform/bd.pem | server ssh private key |
   | terraform/bd.pub | server pub key |
   | ansible/ansible.cfg | ansible config file |

<br />

## On-Premise Setup

  If you use previous terraform to build aws infra, please **skip** this step.

  Otherwise, please copy/create/modify below listed files,

  | SRC | DEST | Description |
  | --- | --- | --- |
  | terraform/ansible.cfg.tpl | ansible/ansible.cfg | ansible config file |
  | terraform/ansible.inventory.tpl | ansible/inventory/bd.cfg | ansible inventory file |
  | ansible/group_vars/bd.yml | ansible/group_vars/bd.yml | update what you want |
  | N/A | terraform/bd.pub | rename you public key for servers or update ansible.cfg
  | N/A | terraform/bd.pem | rename you public key for servers or update ansible.cfg


<br />

## Ansible Playbook - Provision

    $ ansible-playbook provision.yml [--tags TAG]

  Note: don't forget add args [**-i inventory/pi.inv**] for all playbooks which depends on what inventory you want to use.

  | TAG | Description | Dependence |
  | --- | --- | --- |
  | N/A | this will setup everything | N/A |
  | base | setup ubuntu server for support other tags, once base is done, <br />you could ssh bd1 for ssh login server01 | N/A |
  | zk | install and setup zk cluster | base |
  | kafka | install and setup kafka cluster | base, zk |
  | k8s | install and setup kubernetes cluster | base |
  | hadoop | install and setup hadoop | base, zk |
  | hbase | install and setup hbase | base, hadoop, zk |
  | ceph | install and setup ceph | base |
  | etchosts | add those servers to you local /etc/hosts | N/A |
  | local-ssh | add new config file into your local ~/.ssh/config.d;<br /> So, you can easiest login server by **ssh bd1** | N/A |
  | stop[start] | stop or stop all | N/A |
  | stop[start]-hbase | stop or stop hbase | base, zk |
  | stop[start]-hadoop | stop or stop hadoop | base, zk |
  | stop[start]-zk | stop or stop zookeeper | base |
  | stop[start]-kafka | stop or stop kafka | base, zk |
  | stop[start]-ceph | stop or stop ceph | base, ceph |


<br />

## Ansible Playbook - config local enviornment

For update your local /etc/hosts, ``` -K  ```  is required
 
    $ ansible-playbook local-config.yml -K
 
Then, enjoy 😍

![SSH](https://user-images.githubusercontent.com/540463/204861081-862d9cbb-ef26-4558-9b15-a74c7f61e37b.png)

![EtcHosts](https://user-images.githubusercontent.com/540463/204861642-8c5edd1d-a6bc-4b84-8c76-f509cf2fd58a.png)

  
<br />

## Ansible Playbook - k8s - Rook & Ceph - Cloud Native Storage Class for Kubernetes

    $ ansible-playbook k8s-rook-ceph.yml

<br />

## Ansible Playbook - Control remote k8s cluster from local

    $ ansible-playbook k8s-local-kube-config.yml

![kubectl from local](https://user-images.githubusercontent.com/540463/204862291-834367a3-a783-4b36-9284-55a9627e23b8.png)

<br />

## Ansible Playbook - Test

   This playbook will test k8s & kafka infra is constructed.

   Using python script as producer and consumer to demo how to use kafka on k8s pod.

    $ ansible-playbook test.yml [--tags TAG]

  | TAG | Description | Dependency |
  | --- | --- | --- |
  | N/A | for testing everything | base, k8s, zk, kafka, hadoop
  | test-kafka | This will create consumer and producer pod, for testing <br />Kubernetes cluster, Kafka and zookeeper are work as expect | base, k8s, zk, kafka |
  | test-spark | This will use netcat as stream server and Spark SQL + <br />Spark Streaming as client on Kubernetes cluster, base on LogisticRegression,  demostrate sentiment analysis by using tweets | base, k8s, hadoop, zk |
  | test-hbase | Try to create a kubernetes job and use python module happybase to create table and insert rows | base, hadoop, zk, hbase |
  | test-k8s-ingress | Write a nodejs simple webserver deploy to ingress nginx controller and verify if ingress works with different paths works. | base, k8s(atleast 3 nodes) |
  | test-k8s-operator-ansible | **Ansible k8s Operator**; require **operator-sdk** & **kustomize** installed | base, k8s && k8s-local-kube-config.yml |
  | test-k8s-operator-go | **Golang k8s Operator**; require **kubebuilder** installed | base, k8s && k8s-local-kube-config.yml |
  | test-k8s-csi-ceph | use ceph as storage class on k8s | base,ceph,k8s && k8s-local-kube-config.yml |

<br /><br />

## Ansible Playbook - k8s dashboard

   This playbook will create **k8s dashboard**.

     $ ansible-playbook k8s-dashboard.yml [--tags TAG]

  | TAG | Description | Provision Denpendency |
  | --- | --- | --- |
  | N/A | provision dashboard and provider login token and url | base, k8s |
  | start | start dashboard | base, k8s |
  | end | stop dashboard | base, k8s |

![Dashboard - login w/ kube config](https://user-images.githubusercontent.com/540463/204858729-d4280fc4-b9d4-429e-a0eb-66ca3af6a35e.png)

![Dashboard - Pi4 cluster](https://user-images.githubusercontent.com/540463/204858669-85950f67-9f90-4d2b-b3cd-79694a62f1a9.png)

<br />

## Ansible Playbook - k8s - Monitoring & AutoScaling HPA and Keda library

  ### Prerequisite

  | Description | Note |
  | --- | --- |
  | At least 3 nodes | N/A |
  | Play provision.yml --tags base,k8s | this will also install ingress nginx |
  | Play k8s-local-kube-config.yml | N/A |
  
  ### Step

  | STEP | Task | Description |
  | --- | --- | --- |
  | 1 | install.yml | helm install and config prometheus, granfa, loki, keda, blackbox, [grafana blackbox exporter dashboard](https://grafana.com/grafana/dashboards/7587-prometheus-blackbox-exporter/) |
  | 2 | apply.yml | use my simple golang to build distroless docker image (**14.4MB**), this application not only listen http request but also provide prometheus /metrics w/ http_requests_total parameters |
  | 3 | apply.yml |deploy my app and [keda](https://keda.sh/) ScaledObject |
  | 4 | verify.yml | make sure scaleobject successful deploy |
  | 5 | test.yml| use [hey](https://github.com/rakyll/hey) command to request /metrics on **http-request-total.default.svc.cluster.local**, **prometheus-stack-kube-prom-prometheus.prometheus-stack** will collection metrics, and [keda](https://keda.sh/) scaledobject will dectect **sum(rate(http_requests_total[10s]))** from prometheus amd do her jobs , then ansible verify if my app ScaleIn and ScaleOut in the right way. |
  | 6 | output.yml | print services uri |

  ### Run

    $ ansible-playbook k8s-monitoring.yml

  Note: [Config](https://github.com/jasoncheng/testbed/issues/12) more URLs to monitoring

  ![BlackBox Exporter](https://user-images.githubusercontent.com/540463/204856792-7b42454d-a5d3-48ae-b4ec-4655125fc92f.png)

  ![Prometheus](https://user-images.githubusercontent.com/540463/204858635-52b5c40e-49f5-4028-8527-e4c41b005ec4.png)

  [![Demo k8s pod auto scaling by using keda scaledobject](http://img.youtube.com/vi/piX1C9a-Ya0/0.jpg)](https://youtu.be/piX1C9a-Ya0 "click watch video")

<br />

## Ansible Playbook - k8s Container Storage Interface(CSI) for Ceph

  This is just demostrate how to use Ceph as storage class on k8s,

  First, create EC2 instances on AWS (note: at least use t3.medium instance, t3.small is not enough for running this demo), so create you YOUR_TERRAFORM_VAR.tf and override **instance_type_first=t3.medium**, **instance_type=t3.medium**, **instance_count=4**.

    $ terraform apply -var-file=vars/YOUR_TERRAFORM_VAR.tf 

  Provision your ubuntu servers, and also install/config ceph and k8s

    $ ansible-playbook provision.yml --tags base,ceph,k8s -K

  Then, able remote control kubernetes cluster through you local kubectl

    $ ansible-playbook k8s-local-kube-config.yml

  Deploy k8s csi for Ceph

    $ ansible-playbook test.yml --tags test-k8s-csi-ceph

  After minintues, login busybox pod, and have fun :)

    $ kubectl exec -it pod-with-raw-block-volume -- ls /mnt/ceph_rbd

  After finished all test, destroy all,

    $ terraform destroy -var-file=vars/YOUR_TERRAFORM_VAR.tf 

  ![Ceph dashboard](https://user-images.githubusercontent.com/540463/201524079-0f35fcbc-aff1-4a70-846e-96050afd8db5.png)

  ![k8s CSI for Ceph](https://user-images.githubusercontent.com/540463/201524082-f4d10d43-ddfb-4787-a75d-55f485043af5.png)

<br />

## Ansbile Playbook - Health check

    $ ansible-playbook health.yml

<br />

## Add new node into k8s cluster
     
  First, increase instance by modify terrafor/variables.tf var.instance_count+1

     ! new a aws instance
     $ cd terraform && terraform apply

     ! provision new instance
     $ ansible-playbook provision.yml --tags base -K

     ! provision new instance and join cluster
     $ ansible-playbook k8s.yml --tags k8sS,join_only

     ! enable kubectl for remote control
     $ ansible-playbook k8s-local-kube-config.yml

<br />

## Ansible AdHoc

   Check running daemon through Java VM Process Status Tool (jps)

     $ ansible -m shell -a jps all 

<br />

## Destroy Infrastructure on AWS

     $ cd terraform && terraform destroy
