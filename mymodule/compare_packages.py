import aiohttp
import rpm
from tqdm import tqdm

from mymodule.models import FirstLib, SecondLib


async def fetch_packages(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()
        return data.get('packages')


def compare_packages(session, arch):
    packages_first_lib = session.query(FirstLib).filter(FirstLib.arch == arch)
    packages_second_lib = session.query(SecondLib).filter(SecondLib.arch == arch)
    packages_first_lib_names = set(package.name for package in packages_first_lib.all())
    packages_second_lib_names = set(package.name for package in packages_second_lib.all())
    unique_packages_first_lib = packages_first_lib_names - packages_second_lib_names
    unique_packages_second_lib = packages_second_lib_names - packages_first_lib_names
    common_packages = (
            set(package.name for package in packages_first_lib.all())
            & set(package.name for package in packages_second_lib.all())
    )
    common_packages_second_lib = packages_second_lib.filter(
        SecondLib.name.in_(common_packages)).all()
    common_packages_first_lib = packages_first_lib.filter(
        FirstLib.name.in_(common_packages)).all()
    packages = []
    for package_second_lib in tqdm(common_packages_second_lib):
        package_first_lib = common_packages_first_lib[0]
        common_packages_first_lib = common_packages_first_lib[1:]
        if rpm.labelCompare(package_second_lib.version, package_first_lib.version) > 0:
            packages.append({k: v for k, v in package_second_lib.__dict__.items() if k != '_sa_instance_state'})
    return (
        [
            {k: v for k, v in pack.__dict__.items() if k != '_sa_instance_state'}
            for pack in session.query(FirstLib).filter(FirstLib.name.in_(unique_packages_first_lib)).all()
        ],
        [
            {k: v for k, v in pack.__dict__.items() if k != '_sa_instance_state'}
            for pack in session.query(SecondLib).filter(SecondLib.name.in_(unique_packages_second_lib)).all()
        ],
        packages
    )
