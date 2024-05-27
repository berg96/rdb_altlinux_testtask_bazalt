# Test task for a Junior Python programmer from Basealt

## Task description:
I have developed a python module and a cli utility using this module.
The principle of operation:
When the utility is launched, the module receives package lists from Basealt's public API [https://rdb.altlinux.org/api/](https://rdb.altlinux.org/api/) using /export/branch_binary_packages/{branch} method, sisyphus and p10 are used as branches. Next, it compares these lists for each supported architecture and outputs the information to the terminal in JSON format:
* 'unique_packages_p10': all packages that are in p10, but not in sisyphus;
* 'unique_packages_sisyphus': all packages that are in sisyphus but not in p10;
* 'packages': all packages with more version-release in sisyphus than in p10.


### Author Artem Kulikov

tg: [@Berg1005](https://t.me/berg1005)

[GitHub](https://github.com/berg96)


## How to launch a project

Clone repo:
```
git clone git@github.com:berg96/rdb_altlinux_testtask_bazalt.git
```
Run setup:
```
python setup.py install
```
Use 'compare_packages' for run
```
compare_packages
```
