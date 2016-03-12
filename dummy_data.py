
import pandas as pd
from faker import Factory
import random
import datetime
import locale


def main():

    # Set locale to the United States for US-formatted Social Security Numbers
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

    # Create faker factory instance
    faker = Factory.create()

    # The number of rows in the resulting CSV
    num_fake_records = 1000

    # Download the field names from Google Sheets in XLSX format
    google_sheet = pd.read_excel('https://docs.google.com/spreadsheets/d/' + 
                   '1bloqWcGFOmFLJ98iYFAEX5PDZWpqBI722-qZVyekZuU' +
                   '/export?format=xlsx',
                   sheetname=None)
    
    # If a field doesn't have weights, add 1s as weights
    # functionally, this will give each class equal weight
    for field, df in google_sheet.iteritems():
        google_sheet[field] = google_sheet[field].fillna(1)

    # Create the dataframe with dummy data
    dummy_data = pd.DataFrame([fake_record(google_sheet, faker) for _ in range(num_fake_records)])

    # Output and save data
    print dummy_data.head()

    output_file = 'dummy_data.csv'
    dummy_data.to_csv(output_file, index=False)
    print '\nDummy data saved to: ' + output_file


def fake_record(google_sheet, faker):
    """Return one row with fake data
    """

    one_record = {}

    # Pick one from each field in the spreadsheet
    for field, df in google_sheet.iteritems():
        one_record[field] = weighted_choice(df.values.tolist())

    # Add Faker fields
    one_record['home_city'] = faker.city()
    one_record['home_state'] = faker.state()

    # Add dates
    one_record['enlistment_date'] = date_between(faker, 'jan01-1995', 'jan01-2013')
    one_record['separation_date'] = date_between(faker, 'jan01-1996', 'jan01-2014')

    return one_record


def date_between(faker, d1, d2):
    """Return a date that falls between two dates
    """

    f = '%b%d-%Y'
    date_time = faker.date_time_between_dates(datetime.datetime.strptime(d1, f), datetime.datetime.strptime(d2, f))
    return date_time.date()


def weighted_choice(choices):
    """For a list of items in the format (class, weight), return one choice from the list, taking weight into account

    Weight can be percentages or numbers, they don't have to add up to anything
    """

    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

    assert False, "The weighted_choice() function shouldn't get here"


if __name__ == "__main__":
    main()
