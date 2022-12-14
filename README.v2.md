Previous on [main branch](https://github.com/jasoncheng/testbed/tree/main) we play Ceph, Zookeeper, Kafka, Hadoop, HBase, Kubernetes ...on Ubuntu and RHEL based OS.

From now on, we start a brand new [v2 branch](https://github.com/jasoncheng/testbed/tree/v2), let's build almost everything on kubernetes, 
hope this ansible automatic scripts can help someone else to learn more about devops.<br><br>

# Environment

### Computer
  
&nbsp;&nbsp; [Pi4B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) x 6

### OS

&nbsp;&nbsp; [Ubuntu 20.04](https://ubuntu.com/) ([why?](https://docs.ceph.com/en/quincy/start/os-recommendations/)); *Use [Pi-Imager](https://www.raspberrypi.com/software/) to install ubuntu to all your sdcard first.*


&nbsp;&nbsp; *I also test on CentOS 7 and CentOS Stream 9, even though i installed everything but still look like many kubernetes's issues on Raspberry Pi require to be resolve, in current stage, all i want is focus on k8s, this is another reason.*

### SDCard for OS

&nbsp;&nbsp; [SanDisk microSD C10](https://www.amazon.com/SanDisk-128GB-Extreme-microSD-Adapter/dp/B07FCMKK5X) x 6

### HardDisk for storage

&nbsp;&nbsp;1TB Toshiba (Over seven years ago?? maybe)

&nbsp;&nbsp;~~500GB Unknow brand (Over ten years ago)~~ !! Broken 🥲

&nbsp;&nbsp;~~150GB Unknow brand (Over ten years ago)~~ !! Broken 🥲

&nbsp;&nbsp;1TB ADATA (20221214 New One)

<sup>
   I cannot afford more hard disk for now, so collect disk from others; I would recommend buy new one instead of waste your time on troubleshooting... But debugging more issues, let us can handle more situation earily, isn't it.......</sup> 😂

   ![505852](https://user-images.githubusercontent.com/540463/207633001-f442db96-934b-43bc-902a-aac3af679bab.jpg)

<br><br>

### Nodes Information

| IP | Hostname | k8s Role | HA Proxy |
| -------- | -------- | ----- | --- |
| 10.33.27.184 | pi0 | node |✔️
| 10.33.27.186 | pi1 | control-plane |
| 10.33.27.138 | pi2 | node |
| 10.33.27.193 | pi3 | control-plane |
| 10.33.27.129 | pi4 | node |
| 10.33.27.174 | pi5 | node |✔️

&nbsp;&nbsp;Keep in mind, best pratice and better performance is **2*N + 1** nodes, but...but...we just wanna use all of our Pi 😍.
<br><br>

### Goal 

&nbsp;&nbsp; *once all step finished, you can test all the tools on your PC browser*

| Domain | Description | Account Passwoard |
| -------- | -------- | -------- |
| https://k8s | kubernetes dashboard | Login w/ you PC ~/.kube/config |
| https://ceph | Ceph dashboard | ID: admin <br>PS: output from step 7. console log |
| http://alert | AlertManager dashboard | N/A |
| http://prome | Prometheus dashboard | N/A |
| http://grafana | Grafana dashboard | ID: admin <br> PS: admin
| https://k8s-api:16443 | No UI, just for k8s HA | N/A |

| SSH Hostname | Description |
| -------- | -------- |
| pi0~pi5 | $ ssh pi0<br> $ ssh pi1|


<br>

# Getting Start

### 0. What kind of infra you choise ?

- AWS Cloud: Please [go here](https://github.com/jasoncheng/testbed#aws-infrastructure-setup) to finish terraform apply, once finished, you can skip Step 1.
- On-Premise: Go next.

### 1. Update Ansible Inventory

&nbsp;&nbsp;Modify [inventory/pi.inv](https://github.com/jasoncheng/testbed/blob/v2/ansible/inventory/pi.inv), *according to you envirnoment.*

### 2. Update Ansible variables

[groups/vars/pi.yml](https://github.com/jasoncheng/testbed/blob/v2/ansible/group_vars/pi.yml#L34)

&nbsp;&nbsp;&nbsp;<sup>Pick a available IP, later..we will use this IP address to play as **VIP**.</sup>

&nbsp;&nbsp;&nbsp;<sup>BTW, most other variables was used for legacy branch main, leave it alone.</sup>

     K8S_HA_VIP: '10.33.27.78'

[groups/vars/all.yml](https://github.com/jasoncheng/testbed/blob/v2/ansible/group_vars/all.yml#L23)

&nbsp;&nbsp;&nbsp;<sup>Go [docker.io](https://docker.io/), register account and get information for fill up the params.</sup>
  
     DOCKER_USER: 'USE_YOUR_OWN'
     DOCKER_PASS: 'USE_YOUR_OWN'

### 3. Provision all nodes

     $ ansible-playbook provision.yml --tags base

### 4. Prepare High Availability Proxy

&nbsp;&nbsp;Create a VIP on eth0; This will install and configure [HaProxy](http://www.haproxy.org/) and [KeepAlived](https://github.com/acassen/keepalived) by VIP (according inventory/pi HA group)

     $ ansible-playbook ha.yml
     
     ## Verify if VIP success binding on eth0 ##

     $ ansible -m shell -a "ip a" HA

### 5. Install Kubernetes

     $ ansible-playbook provision.yml --tags k8s


### 6. Install Ingress-Nginx on kubernetes

     $ ansible-playbook k8s-ingress-nginx.yml


### 7. Install Kubernetes dashboard (Optional)


     $ ansible-playbook k8s-dashboard.yml


### 8. Create Storage Cluster on Kubernetes

&nbsp;&nbsp;&nbsp;&nbsp;Create StorageClass on Kubernetes by [Rook Ceph operator](https://rook.io/).

     $ ansible-playbook k8s-rook-ceph.yml

     ## This output will also include login credential, if you want to retrieve password again ##

     $ kubectl -n rook-ceph get secret rook-ceph-dashboard-password -o jsonpath="{['data']['password']}" | base64 --decode && echo


### 9. Install Monitor tools on Kubernetes

&nbsp;&nbsp;&nbsp;&nbsp;Let's start crazy install all the monitor tools ..😝. haha,
This will install,

- [Prometheus](https://prometheus.io/)
- [Loki](https://github.com/grafana/loki)
- [Grafana](https://grafana.com/)
- [AlertManager](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [NodeExporter](https://github.com/prometheus/node_exporter)
- [Blackbox Exporter](https://github.com/prometheus/blackbox_exporter)
- [Keda Operator](https://keda.sh/)

&nbsp;&nbsp;&nbsp;&nbsp;By [Prometheus Community Operator](https://github.com/prometheus-community/helm-charts) with [Helm](https://helm.sh/), as mentioned before, everything on Kubernetes.

     $ ansible-playbook k8s-monitoring.yml

### 10. Config you local envirnoment


     ## point virtual domains for your PC only ##

     $ ansible-playbook local-config.yml-K

     ## remote control k8s from your PC ##

     # ansible-playbook k8s-local-kube-config.yml


### 11. Test all by kubernetes Keda Operator (Auto Scaling Operator)


&nbsp;&nbsp;&nbsp;&nbsp;This step can make sure below listed is setup correctly, something like all you can eat? 🧐

- Kubernetes: Cluster must be okay for sure
- Prometheus: Scrape config is okay, and also provide Keda's ScaledObject to query metrics
- System OS: Okay for build docker image, and push to registry
- HttpRequest Go Server: My simple go server for provide /metrics for prometheus to scrape.
- Keda operator: ScaledObject(Auto Scaling) is work as expected.
- Kubernetes Nginx ingress: If nginx correct proxy my fake host to HttpRequest service port

&nbsp;&nbsp;&nbsp;&nbsp;[Click me](https://github.com/jasoncheng/testbed/tree/main#ansible-playbook---k8s---monitoring--autoscaling-hpa-and-keda-library) for checking more details (Video).

      $ ansible-playbook test.yml --tags test-keda