import time
import pandas as pd
import numpy as np

"""
    Websites used as reference for some of the ideas I came up with:
    https://stackoverflow.com/questions/11847341/while-not-in-list
    https://stackoverflow.com/questions/60339049/weekday-name-from-a-pandas-dataframe-date-object
    https://stackoverflow.com/questions/48590268/pandas-get-the-most-frequent-values-of-a-column
    https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python
    https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.iloc.html
    https://www.kite.com/python/examples/2645/pandas-get-the-raw-data-from-a-%60dataframe%60-as-a-list-of-rows
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters(city_list):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!  Type "EXIT" at any time in intitial data selection to exit program.')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('\nPlease select a city, between Chicago, New York City, or Washington:  ').lower()
    while city not in city_list:
        if city == "exit":
            exit()
        else:
            city = input('\n{} is an invalid input, please enter one of the three cities:  Chicago, New York City, or Washington:  '.format(city)).lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month_list = ['january','february','march','april','may','june','all']
    month = input('Please select a month, between January and June, or "all" months:  ').lower()
    while month not in month_list:  #Used StackOverflow
        if month == "exit":
            exit()
        else:
            month = input('\n{} is an invalid input, please select a month, between January and June, or "all" months:  '.format(month)).lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    day = input('Please select any day of the week, or "all" days:  ').lower()
    while day not in day_list:
        if day == "exit":
            exit()
        else:
            day = input('\n{} is an invalid input, please select any day of the week, or "all" days:  '.format(day)).lower()

    #Adding option to exit so user can start over
    should_exit = ""
    should_exit = input('\nYou chose {}, {}, and {}, is this correct?  Enter yes or no:  '.format(city.title(), month.title(), day.title())).lower()

    print('-'*40)
    return city, month, day, should_exit


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #create dataframe from the selected city
    df = pd.read_csv(CITY_DATA[city])

    #change Start Time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Get the month and the day of the week from the start time
    #My version of python did not support weekday_name function, but found out I can use day_name() through StackOverflow.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    #filter by month if applicable
    if month != 'all':
        #use the index of the months list to get the corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #filter by month to create the new dataframe
        df = df[df['month'] == month]

    #filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, month, day, city):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month  *IF* "all" selected for month.  Otherwise, ignore this line of code.
    if month == "all":
        popular_month = df['month'].mode()[0]
        print('Most common month in {} to bikeshare:  '.format(city.title()), popular_month)

    # TO DO: display the most common day of week *IF* "all" selected for day.  Otherwise, ignore this line of code.
    if day == "all":
        popular_day = df['day_of_week'].value_counts().idxmax()  #StackOverflow for the idxmax() idea
        print('Most common day in {} to bikeshare:  '.format(city.title()), popular_day)

    # TO DO: display the most common start hour *REGARDLESS* of what month and day chosen
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most frequent ride start hour in {}:  '.format(city.title()), popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()  #StackOverflow for the idxmax() idea
    print('Most frequent ride start station in {}:  '.format(city.title()), popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()  #StackOverflow for the idxmax() idea
    print('Most frequent ride end station in {}:  '.format(city.title()), popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    stn_pair_count = df.groupby(['Start Station','End Station']).size().idxmax()  #Udacity pandas for .groupby idea, StackOverflow for the .size and .idxmax() idea
    print('Most common combo in {} is:  "{}" to "{}"'.format(city.title(), stn_pair_count[0], stn_pair_count[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city):
    """Displays statistics on the total and average trip duration.  Converts to easier to understand time data other than just seconds."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    travel_time = df['Trip Duration'].sum()

    #Breaking down total travel time into more understandable statistics, as opposed to a huge number of seconds.
    int_yrs = int(travel_time / (365*24*60*60))
    year_remainder = travel_time % (365*24*60*60)
    int_days = int(year_remainder / (24*60*60))
    day_remainder = year_remainder % (24*60*60)
    int_hrs = int(day_remainder / (60*60))
    hour_remainder = day_remainder % (60*60)
    int_mins = int(hour_remainder / 60)
    int_secs = int(round(hour_remainder % 60,0))

    print('Total travel time over selected time period in {}:  {} yrs, {} days, {} hrs, {} mins, {} seconds.'.format(city.title(), int_yrs, int_days, int_hrs, int_mins, int_secs))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    #Breaking down mean travel time into more understandable statistics, as opposed to seconds.
    #Also, reusing above variables, no longer need old ones and prefer not to add more variables to memory.
    int_days = int(mean_travel_time / (24*60*60))
    day_remainder = mean_travel_time % (24*60*60)
    int_hrs = int(day_remainder / (60*60))
    hour_remainder = day_remainder % (60*60)
    int_mins = int(hour_remainder / 60)
    int_secs = int(round(hour_remainder % 60,0))

    print('Mean travel time over selected time period in {}:  {} days, {} hrs, {} mins, {} seconds.'.format(city.title(), int_days, int_hrs, int_mins, int_secs))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users.  Provides subscription status, gender counts, and age/birth year statistics."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of subscription status - whether a subscriber, one-time (or at least unsubscribed) customer, or "dependent"
    user_stats = df['User Type'].value_counts()
    print('User statistics over the selected range in {}:  \n{}'.format(city.title(), user_stats))

    # TO DO: Display counts of gender, if not Washington.
    if city == "washington":
        print('\nNo gender information to display for Washington.')
    else:
        gender_stats = df['Gender'].value_counts()
        print('\nGender counts over the selected range in {}:  \n{}'.format(city.title(), gender_stats))

    # TO DO: Display earliest, most recent, and most common year of birth
    #Oldest birth year in range
    if city == "washington":
        print('\nNo birth date information to display for Washington.')
    else:
        old_yob = int(df['Birth Year'].min())
        age = 2017 - old_yob
        print("\n{}'s oldest user born in {} ({} year(s) old in 2017).".format(city.title(), old_yob, age))

        #Youngest birth year in range
        young_yob = int(df['Birth Year'].max())
        age = 2017 - young_yob
        print("{}'s youngest user born in {} ({} year(s) old in 2017).".format(city.title(), young_yob, age))

        #Mode year in range
        mode_yob = int(df['Birth Year'].mode())
        age = 2017 - mode_yob
        print('Most common birth year for a {} user is {}.  In 2017, that would be {} year(s) old!'.format(city.title(), mode_yob, age))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df, acceptable_list):
    """Used to display the raw data for the user.  Will display the first five lines of raw data, until user decides to stop viewing data.  Option to use less-raw data someday."""

    counter = 0
    while True:
        #print(df.iloc[counter:counter+5])  #want to find first 5 rows, and since second number not inclusive have to use +5.  Pandas.pydata documentation for this idea.  Not using it because it's not raw, makes me sad :( commenting out for future projects.
        print(df.values[counter:counter+5])  #want to find first 5 rows, and since second number not inclusive have to use +5.  kite.com blog for this idea, I tested with data in []
        restart = input('\nWould you like to see more data?  Enter yes or no:  \n')

        while restart.lower() not in acceptable_list:
            restart = input('\n{} is an invalid input, would you like to see more data?  Enter yes or no:  '.format(restart))

        if restart.lower() != 'yes' and restart.lower() != "y":
            break
        else:
            counter += 5


def main():
    while True:

        print('-'*40)

        yes_list = ['yes','y']
        city_list = ['chicago','new york city','washington']

        city, month, day, should_exit = get_filters(city_list)
        #should_exit is a string that determines if we should exit the program based on input from the user in get_filters.
        if should_exit.lower() in yes_list:

            df = load_data(city, month, day)
            time_stats(df, month, day, city)
            station_stats(df, city)
            trip_duration_stats(df, city)
            user_stats(df, city)

            acceptable_list = ['yes','y','no','n']

            sample_data = input('\nWould you like to see the raw data?  Enter yes or no:  \n')
            while sample_data.lower() not in acceptable_list:
                sample_data = input('\n{} is an invalid input, would you like to see the raw data?  Enter yes or no:  '.format(sample_data))

            #does user want to see raw data... will call "raw_data" function to display with code below.
            if sample_data.lower() in yes_list:
                raw_data(df, acceptable_list)
            else:
                print('\nSkipping raw data display...')

            restart = input('\nWould you like to restart? Enter yes or no:  \n')
            while restart.lower() not in acceptable_list:
                restart = input('\n{} is an invalid input, would you like to restart? Enter yes or no:  '.format(restart))

            if restart.lower() not in yes_list:  #This works because only no or yes can get passed from loop above.
                break

if __name__ == "__main__":
	main()
