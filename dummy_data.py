
import pandas as pd
from faker import Factory
import random
import datetime
import locale


# Set locale to the United States for US-formatted Social Security Numbers
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
faker = Factory.create()

num_fake_records = 1000

# Picklists for data fields
enlistment_base = 'Hood,Bragg,Dix,Carson'.split(',')
education = "High School,Some Bachelor's Degree,Bachelor's Degree,Post-Bachelors".split(',')
gender = "M,F".split(',')
ptsd_level = 'No PTSD,Moderate PTSD,Severe PTSD'.split(',')
mtbi_level = 'No mTBI,mTBI Diagnosed'.split(',')

def date_between(d1, d2):
    """Return a date that falls between two dates
    """

    f = '%b%d-%Y'
    date_time = faker.date_time_between_dates(datetime.datetime.strptime(d1, f), datetime.datetime.strptime(d2, f))
    return date_time.date()

def fake_record():
    """Return one row with fake data
    """

    return {
        # 'ssn': faker.ssn()
        'gender': random.choice(gender)
        , 'home_city': faker.city()
        , 'home_state': faker.state()
        , 'education': random.choice(education)
        , 'enlistment_date': date_between('jan01-1995', 'jan01-2013')
        , 'enlistment_base': random.choice(enlistment_base)
        , 'separation_date': date_between('jan01-1996', 'jan01-2014')
        , 'ptsd_level': random.choice(ptsd_level)
        , 'mtbi_level': random.choice(mtbi_level)
        }

# Create the dataframe
dummy_data = pd.DataFrame([fake_record() for _ in range(num_fake_records)])

# Output data
print dummy_data.head()

output_file = 'dummy_data.csv'
dummy_data.to_csv(output_file, index=False)
print '\nDummy data saved to: ' + output_file