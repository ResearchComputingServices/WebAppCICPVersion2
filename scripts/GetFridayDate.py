from datetime import timedelta

# Fetching the Friday date based on user input date
def fetch_fridaydate(todays_date):
# Using current time
        week_day = todays_date.weekday()

        #Monday
        if week_day == 0:
                # Prev Friday
                past_week_friday = todays_date + \
                                timedelta(days = -3)
                return(past_week_friday.date())               
        #Tuesday                        
        elif week_day == 1:
                # Prev Friday
                past_week_friday = todays_date + \
                                timedelta(days = -4)
                return(past_week_friday.date())
        #Wednesday                        
        elif week_day == 2:
                
                # Report is not yet generated and user selects a wednesday
                past_week_friday = todays_date + \
                                timedelta(days = -5)

                # Report is generated on Friday and user selects a wednesday
                this_week_friday = todays_date + \
                                timedelta(days = 2)
                
                return(past_week_friday.date())

        # Thursday                        
        elif week_day == 3:
                
                # Report is not yet generated and user selects a thursday
                past_week_friday = todays_date + \
                                timedelta(days = -6)

                # Report is generated on Friday and user selects a thursday
                this_week_friday = todays_date + \
                                timedelta(days = 1)

                return(past_week_friday.date())
        # Friday                        
        elif week_day == 4:
                # Today - Friday
                this_week_friday = todays_date + \
                                timedelta(days = 0)
                return(this_week_friday.date())
        # Saturday
        elif week_day == 5:
                # Present Week Friday
                this_week_friday = todays_date + \
                                timedelta(days = -1)
                return(this_week_friday.date())
        # Sunday                        
        elif week_day == 6:
                # Present Week Friday
                this_week_friday = todays_date + \
                                timedelta(days = -2)
                return(this_week_friday.date())