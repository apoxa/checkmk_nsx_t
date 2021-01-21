# CheckMK extension for NSX-T 3.x

<a href="https://github.com/apoxa/checkmk_nsx_t/actions"><img alt="checkmk_nsx_t status" src="https://github.com/apoxa/checkmk_nsx_t/workflows/build/badge.svg"></a>

Monitores the status of a NSX-T 3.x environment by use of the [NSX-T](https://www.vmware.com/de/products/nsx.html) API. The status of the following items is checked:

* Resources of NSX-Manager appliance
    * CPU
    * Memory
* Backups
* Load Balancers
    * Virtual Servers
    * Pools
