from federal_reserve import merge_fed_data, labor_data
from pybea import automate_nipa, automate_fixedassets


def main():
    labor_data.main()
    merge_fed_data.main()
    automate_nipa.update_all_nipa_tag('A')
    automate_fixedassets.update_all_fa_tag()


if __name__ == '__main__':
    main()
