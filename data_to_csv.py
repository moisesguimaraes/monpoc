#!/usr/bin/env python
import sys

from oslo_config import cfg

import monpoc


_opts = [
    cfg.StrOpt(
        'cathegory',
        required=True,
        positional=True,
        choices=["Monsters", "Units", "Buildings", "Abilities"],
        help='What cathegory to be exported.'),
]


def main():
    conf = cfg.ConfigOpts()
    conf.register_cli_opts(_opts)

    try:
        conf(sys.argv[1:])

        if conf.cathegory == "Monsters":
            pass
        elif conf.cathegory == "Units":
            pass

        elif conf.cathegory == "Buildings":
            print(monpoc.Building.csv_headers())

            for building in monpoc.BUILDINGS.values():
                print(building.to_csv())

        elif conf.cathegory == "Abilities":
            print(monpoc.Ability.csv_headers())

            for ability in monpoc.ABILITIES.values():
                print(ability.to_csv())

    except cfg.RequiredOptError:
        conf.print_help()
        if not sys.argv[1:]:
            raise SystemExit
        raise


if __name__ == '__main__':
    sys.exit(main())
