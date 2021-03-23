import pandas as pd
import pickle
import os

nipa_path = os.path.join(os.path.dirname(__file__), '..', 'nipa', 'nipadataA.csv')
print(nipa_path)



# It turns out that these three separate functions might not be necessary
# since they all appear to populate the same lists.
def get_a_tables():
    annual_data = pd.read_csv(nipa_path)
    annual_tables = annual_data['%SeriesCode'].values

    return annual_tables


def get_q_tables():
    quarterly_data = pd.read_csv(nipa_path)
    quarterly_tables = quarterly_data['%SeriesCode'].values

    return quarterly_tables


def get_m_tables():
    monthly_data = pd.read_csv(nipa_path)
    monthly_tables = monthly_data['%SeriesCode'].values

    return monthly_tables


def main():
    annual_tables = get_a_tables()
    quarterly_tables = get_q_tables()
    monthly_tables = get_m_tables()

    # annual_tables = sorted(list(set(annual_tables)))
    # quarterly_tables = sorted(list(set(quarterly_tables)))
    # monthly_tables = sorted(list(set(monthly_tables)))

    # with open('annual_tables.pkl', 'wb') as f:
    #     pickle.dump(annual_tables, f)

    with open('annual_tables.pkl', 'rb') as f:
        annual_tables = pickle.load(f)
        print((annual_tables))
        print(len(annual_tables))


if __name__ == '__main__':
    main()
