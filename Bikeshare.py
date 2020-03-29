import time
import random
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = list(CITY_DATA.keys())
#print(cities)

print('Hello! You have chosen to run the program "Bikeshare.py".  The purpose of this program is to allow the user to filter and examine data from bikeshare programs in different cities.  The bikeshare program allowed users to borrow bicycles and ride them from one station to the next. Data was collected for each trip taken and includes:')
print('\n- Trip Start Time, End Time and Duration (time)')
print('- Start Station and End Station (location)')
print('- User\'s Gender')
print('- User\'s Birth Year')
print('- Whether or not the User was a subscriber to the program')
print('\nIf this you are new to this program, it is recommended you preview the raw data to help you understand the data used in this program.')

prvw_yn = input('\nWould you like to preview the raw data? Type "Y" or "N" for yes or no: ').lower()

while prvw_yn not in ['y','n']:
    prvw_yn = input('That is not a valid option. Type "Y" or "N" for yes or no: ').lower()

prvw_city = random.choice(cities)
#print(prvw_city)

if prvw_yn == 'y':
    print('Below is a random preview of the raw data from {}:\n'.format(prvw_city.title()))
    file = CITY_DATA[prvw_city]
    prvw = pd.read_csv(file)
    print(prvw.sample(n=5))


#to help with working with months, I'm making a dictionary of the months:
month_dict = {1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june', 7:'july', 8:'august', 9:'september', 10:'october', 11:'november', 12:'december'}

#to help with working with days, I'm making a dictionary of the days of the week:
day_dict = {6:'sunday', 0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday'}

def get_filtrd_df():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter

    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nLet\'s explore some US bikeshare data!')

    cities_str = ', '.join(cities).title()

    # tell user which cities have data available
    print('Data is available from the cities of {}.'.format(cities_str))

    #get user to input one of the cities
    city = input('\nPlease choose a city by typing the name of the city: ').lower()

    #while loop to reject invalid input.
    while city not in cities:
        city = input('That is not a valid option. Please choose a city by typing the name of the city: ').lower()

    #load initial data frame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime - code borrowed from Udacity's solution to practice problems
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #create 'months' column in dataframe - code borrowed from Udacity's solution to practice problems
    df['month'] = df['Start Time'].dt.month

    # to help specify the valid options for user input, get list of months in dataframe, and include the 'all' option
    month_ints = list(df.month.unique())
    month_ints.sort()

    months_str_list = []

    for month in month_ints:
        months_str_list.append(month_dict[month])

    months_str = ', '.join(months_str_list).title()

    #inform the user which months have data available for the city they chose.
    print('\n{} has data available for the months of {}.'.format(city.title(), months_str))

    while True:
        try:
            month = int(input('\nPlease choose a month by typing the month as an integer. (1 for January, 2 for February, etc.)  Alternatively, type "0" to view data for all available months: '))
            if month in month_ints or month == 0:
                break
            else:
                print('\nNo data available for {}'.format(month_dict[month].title()))
        except:
            print('invalid input')

    while True:
        if month == 0:
            print('\nYou have chosen to view data for all available months.')
            break
        elif month in month_ints:
            print('\nYou have chosen to view data for the month of {}'.format(month_dict[month].title()))
            break

    #filter df by month if month not equal to zero

    if month != 0:
        is_month = df['month'] == month
        df = df[is_month]
    #this filtering code was borrowed from here:  https://cmdlinetips.com/2018/02/how-to-subset-pandas-dataframe-based-on-values-of-a-column/

    while True:
        try:
            dow = int(input('\nPlease choose a day of the week by typing the day as an integer (1-7 with 1 being Sunday and 7 being Saturday).  Alternatively, type "0" to view data for all days of the week: '))
            if 0<= dow <= 7:
                break
            else:
                print('\n{} is not a day of the week.'.format(dow))
        except:
            print('\nInvalid input.')

    #define a dictionary to convert dow to pandas .dt.weekday function with  monday = 0 and sunday = 6
    dow_dict = {0:7, 1:6, 2:0, 3:1, 4:2, 5:3, 6:4, 7:5}

    #redefine dow so that dow works nicely with pandas .dt.weekday function
    dow = dow_dict[dow]

    if dow == 7:
        print('\nYou have chosen to view data for all days of the week')
    else:
        print('\nYou have chosen to view data for {}'.format(day_dict[dow].title()))

    #create 'day_of_week' column in dataframe - code structure borrowed from Udacity's solution to practice problems
    df['day_of_week'] = df['Start Time'].dt.weekday

    if dow == 7:
        pass
    else:
        is_day = df['day_of_week'] == dow
        df = df[is_day]

    #finish formatting dataframe to the dtype's and columns that will be used in the data analysis
    #End time to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Trip duration to timedelta format
    df['Trip Duration'] = pd.to_timedelta(df['Trip Duration'], unit='s')

    #Create hour column
    df['start hour'] = df['Start Time'].dt.hour

    #Create column with start stations and end stations
    df['start&end'] = df['Start Station'] + ' to ' + df['End Station']

    print('- '*40)
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    if len(list(df['month'].unique())) == 1:
        print('Displaying data for the month of', month_dict[most_common_month].title())
    else:
        print('The month with the most Bikeshare trips is', month_dict[most_common_month].title())

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]

    if len(list(df['day_of_week'].unique())) == 1:
        print('Displaying data for', day_dict[most_common_day].title())
    else:
        print('The day of the week with the most Bikeshare trips is', day_dict[most_common_day].title())

    # display the most common start hour
    print('The hour of the day with the most Bikeshare trips is', df['start hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station - code used from: https://stackoverflow.com/questions/20076195/what-is-the-most-efficient-way-of-counting-occurrences-in-pandas
    print('The most commonly used start station is', df['Start Station'].value_counts().keys()[0])

    # display most commonly used end station
    print('The most commonly used end station is', df['End Station'].value_counts().keys()[0])

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip is:\n', df['start&end'].value_counts().keys()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is: ',df['Trip Duration'].sum())

    # display mean travel time
    print('The average travel time is: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    n_usertypes = df['User Type'].nunique()
    utypes = list(df['User Type'].unique())[0:n_usertypes]
    #Remove NaNs from list using: https://stackoverflow.com/a/58696616
    usertypes = [x for x in utypes if pd.notnull(x)]
    print('There are {} different User Types: {}'.format(n_usertypes, usertypes))

    for usertype in usertypes:
        count = df[df['User Type'] == usertype]['User Type'].count()
        print('There were {} {}s'.format(count, usertype))


    # Display counts of gender
    print('\nDisplaying counts of gender (Note some users did not specify):')
    try:
        n_genders = df['Gender'].nunique()
        gendtypes = list(df['Gender'].unique())
        #Remove NaNs from list using: https://stackoverflow.com/a/58696616
        gendertypes = [x for x in gendtypes if pd.notnull(x)]

        for gender in gendertypes:
            count = df[df['Gender'] == gender]['Gender'].count()
            print('There were {} {}s'.format(count, gender))
    except:
        print('\nNo gender data to analyze')

    # Display earliest, most recent, and most common year of birth
    print('\nDisplaying stats based on birth year data:')

    try:
        youngest_yr = df['Birth Year'].max()
        youngest_age = int(datetime.datetime.today().year) - youngest_yr
        print('The youngest user was born in {}    (Age Today: {} years)'.format(youngest_yr, youngest_age))

        oldest_yr = df['Birth Year'].min()
        oldest_age = int(datetime.datetime.today().year) - oldest_yr
        print('The oldest user was born in {}      (Age Today: {} years)'.format(oldest_yr, oldest_age))

        mode_yr = df['Birth Year'].mode()[0]
        mode_age = int(datetime.datetime.today().year) - mode_yr
        print('The most common year of birth is {} (Age Today: {} years)'.format(mode_yr, mode_age))
    except:
        print('\nNo age data to analyze')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('- '*40)


def raw_data(df):
    """Asks the user if they would like to see a random sample of the raw data that was used to calculate the stats.  Columns that were added for calculating stats are not displayed."""
    show_raw = 'blank'
    while True:
        show_raw = input('\nWould you like to view a random sample of the filtered raw data? Enter "yes" or "no".\n')
        if show_raw.lower() == 'yes':
            print(df.drop(['month', 'day_of_week', 'start hour', 'start&end'], axis=1).sample(n=5))
        elif show_raw.lower() == 'no':
            break
        else:
            pass


def main():
    while True:
        df = get_filtrd_df()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        print('-+'*40)
        if restart.lower() != 'yes':
            print('-+'*15+'Terminating Program '+'-+'*15+'\n'+'-+'*40)
            break


if __name__ == "__main__":
	main()
