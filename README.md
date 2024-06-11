# Test task for a Junior Python programmer from Basealt

## Task description:
I have developed a python module and a cli utility using this module.
The principle of operation:
When the utility is launched, the module receives package lists from Basealt's public API [https://rdb.altlinux.org/api/](https://rdb.altlinux.org/api/) using /export/branch_binary_packages/{branch} method. Next, it compares these lists for each supported architecture and outputs the information to the terminal in JSON format:
* 'unique_packages_first_lib': all packages that are in first_lib but not in second_lib;
* 'unique_packages_second_lib': all packages that are in second_lib but not in first_lib;
* 'packages': all packages with more version-release in second_lib than in first_lib.


### Author Artem Kulikov

tg: [@Berg1005](https://t.me/berg1005)

[GitHub](https://github.com/berg96)


## How to launch a project

Clone repo:
```
git clone git@github.com:berg96/rdb_altlinux_testtask_bazalt.git
```
Run with required arguments (branch1, branch2, arch):
```
python main.py {branch1} {branch2} {arch}
```
