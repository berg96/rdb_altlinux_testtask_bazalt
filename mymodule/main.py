import asyncio
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from tqdm import tqdm

from mymodule.compare_packages import fetch_packages, compare_packages
from mymodule.configs import configure_argument_parser
from mymodule.models import FirstLib, SecondLib, Base
from mymodule.outputs import file_output

MAIN_URL = 'https://rdb.altlinux.org/api/export/branch_binary_packages/{}'


async def execute(session, args):
    packages_first_lib, packages_second_lib = await asyncio.gather(
        fetch_packages(MAIN_URL.format(args.branch1)),
        fetch_packages(MAIN_URL.format(args.branch2))
    )
    for package in tqdm(packages_first_lib):
        session.add(FirstLib(**package))
    for package in tqdm(packages_second_lib):
        session.add(SecondLib(**package))
    session.commit()
    (
        unique_packages_first_lib, unique_packages_second_lib, packages
    ) = compare_packages(session, args.arch)
    file_output(
        {
            f'unique_packages_{args.branch1}': unique_packages_first_lib,
            f'unique_packages_{args.branch2}': unique_packages_second_lib,
            'packages': packages
        },
        args
    )


def run():
    args = configure_argument_parser().parse_args()
    engine = create_engine('sqlite:///sqlite.db')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        asyncio.run(execute(session, args))
    engine.dispose()
    os.remove('sqlite.db')
