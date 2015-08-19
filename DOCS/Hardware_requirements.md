# [2.2. HARDWARE REQUIREMENTS](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/6/html/Deploying_OpenStack_Learning_Environments/sect-Hardware_Requirements.html)
_**This is pulled from the Red Hat access site, at the above link.**_


## 2.2.1. Compute Node Requirements

Compute nodes are responsible for running virtual machine instances after they are launched. Compute nodes must support hardware virtualization. Compute nodes must also have enough memory and disk space to support the requirements of the virtual machine instances they host.

**Processor**
> 64-bit x86 processor with support for the Intel 64 or AMD64 CPU extensions, and the AMD-V or Intel VT hardware virtualization extensions enabled.

**Memory**
>A minimum of 2 GB of RAM is recommended.
Add additional RAM to this requirement based on the amount of memory that you intend to make available to virtual machine instances.

**Disk Space**
>A minimum of 100 GB of available disk space is recommended.
Add additional disk space to this requirement based on the amount of space that you intend to make available to virtual machine instances. This figure varies based on both the size of each disk image you intend to create and whether you intend to share one or more disk images between multiple instances.
_1 TB of disk space is recommended for a realistic environment capable of hosting multiple instances of varying sizes._

**Network Interface Cards**
>A minimum of 2 x 1 Gbps Network Interface Cards, although it is ideal to have 3 x 1 Gbps Network Interface Cards.
2.2.2. Network Node Requirements

## 2.2.2 Network Nodes Requirements

Network nodes are responsible for hosting the services that provide networking functionality to compute instances. In particular, they host the DHCP agent, layer 3 agent, and metadata proxy services. Like all systems that handle networking in an OpenStack environment, they also host an instance of the layer 2 agent.
The hardware requirements of network nodes vary widely depending on the networking workload of the environment. The requirements listed here are intended as a guide to the minimum requirements of a network node.

**Processor**
>No specific CPU requirements are imposed by the networking services.

**Memory**
>A minimum of 2 GB of RAM is recommended.

**Disk Space**
>A minimum of 10 GB of available disk space is recommended.
No additional disk space is required by the networking services other than that required to install the packages themselves. However, some disk space must be available to store log files and temporary files.
**Network Interface Cards**
>2 x 1 Gbps Network Interface Cards.

### 2.2.3. Block Storage Node Requirements

Block storage nodes are nodes that host the volume service (openstack-cinder-volume) and provide volumes for use by virtual machine instances or other cloud users. The block storage API (openstack-cinder-api) and scheduling services (openstack-cinder-scheduler) can run on the same nodes as the volume service, or on separate nodes. In either case, the primary hardware requirement of the block storage nodes is that there is enough block storage available to serve the needs of the environment.

The amount of block storage required in an environment varies in accordance with the following factors:

The number of volumes that will be created in the environment.

The average size of the volumes that will be created in the environment.

Whether or not the storage back end will be configured to support redundancy.

Whether or not the storage back end will be configured to create sparse volumes by default.

Use the following formula to assist with estimating the initial block storage needs of your environment:

```
VOLUMES * SIZE * REDUNDANCY * UTILIZATION = TOTAL
```

Replace VOLUMES with the number of volumes that are expected to exist in the environment at any one time.

Replace SIZE with the expected average size of the volumes (in gigabytes) that will exist in the environment at any one time.

Replace REDUNDANCY with the expected number of redundant copies of each volume that the back end storage will be configured to store. Use 1, or skip this multiplication operation if no redundancy is required.

Replace UTILIZATION with the expected percentage of each volume that will actually be used. Use 1, indicating 100%, if the use of sparse volumes will not be enabled.

The resultant figure represents an estimate of the block storage needs of your environment in gigabytes. It is recommended that some additional space is allowed for future growth. Addition of further block storage after the environment has been deployed is facilitated by adding more block storage providers and, if necessary, additional instances of the volume service.
