import asyncio
import os

import aiohttp
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, declared_attr
from tqdm import tqdm

MAIN_URL = 'https://rdb.altlinux.org/api/export/branch_binary_packages/{}'
ARCHS = ['x86_64', 'armh', 'i586', 'x86_64-i586', 'ppc64le', 'noarch', 'aarch64']


class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)


class Package:
    name = Column(String(200))
    epoch = Column(Integer)
    version = Column(String(200))
    release = Column(String(200))
    arch = Column(String(200))
    disttag = Column(String(200))
    buildtime = Column(Integer)
    source = Column(String(200))

    def __repr__(self):
        return f'{self.__class__.__name__} {self.name} {self.version} {self.arch}'

    class Meta:
        abstract = True


class P10(Base, Package):
    pass


class Sisyphus(Base, Package):
    pass


async def fetch_packages(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()
        return data.get('packages')


def compare_packages(session, arch):
    packages_p10 = session.query(P10).filter(P10.arch == arch)
    packages_sisyphus = session.query(Sisyphus).filter(Sisyphus.arch == arch)
    packages_p10_names = set(package.name for package in packages_p10.all())
    packages_sisyphus_names = set(package.name for package in packages_sisyphus.all())
    unique_packages_p10 = packages_p10_names - packages_sisyphus_names
    unique_packages_sisyphus = packages_sisyphus_names - packages_p10_names
    common_packages = (
            set(package.name for package in packages_p10.all())
            & set(package.name for package in packages_sisyphus.all())
    )
    common_packages_sisyphus = packages_sisyphus.filter(
        Sisyphus.name.in_(common_packages)).all()
    common_packages_p10 = packages_p10.filter(
        P10.name.in_(common_packages)).all()
    packages = []
    for package_sisyphus in tqdm(common_packages_sisyphus):
        package_p10 = common_packages_p10[0]
        common_packages_p10 = common_packages_p10[1:]
        if package_sisyphus.version > package_p10.version:
            packages.append(package_sisyphus)
    return (
        [pack for pack in session.query(P10).filter(P10.name.in_(unique_packages_p10)).all()],
        [pack for pack in session.query(Sisyphus).filter(Sisyphus.name.in_(unique_packages_sisyphus)).all()],
        packages
    )


async def execute(session):
    packages_p10, packages_sisyphus = await asyncio.gather(
        fetch_packages(MAIN_URL.format('p10')),
        fetch_packages(MAIN_URL.format('sisyphus'))
    )
    for package in tqdm(packages_p10):
        session.add(P10(**package))
    for package in tqdm(packages_sisyphus):
        session.add(Sisyphus(**package))
    session.commit()
    results = {}
    for arch in ARCHS:
        (
            unique_packages_p10, unique_packages_sisyphus, packages
        ) = compare_packages(session, arch)
        results[arch] = {
            'unique_packages_p10': unique_packages_p10,
            'unique_packages_sisyphus': unique_packages_sisyphus,
            'packages': packages
        }
    print(results)


def main():
    engine = create_engine('sqlite:///sqlite.db')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        asyncio.run(execute(session))
    engine.dispose()
    os.remove('sqlite.db')

