from pandas import read_csv
from urllib.error import HTTPError
from datetime import date,timedelta

print('*** Covidata - A simple Covid-19 tracker ***')
print('Data collected from GitHub repo of JHU CSSE')
print('Tip: Leave date field empty to get latest info!')

while True:
    chk_date = input('\nEnter date (mm-dd-yyyy): ')
    if chk_date=='':
        dynURL = (date.today()-timedelta(days=1)).strftime('%m-%d-%Y')+'.csv'
        dayBeforeURL = (date.today()-timedelta(days=2)).strftime('%m-%d-%Y')+'.csv'
    else:
        dynURL = chk_date+'.csv'
    statURL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    try:
        csv_covid = read_csv(statURL + dynURL)
    except HTTPError:
        try:
            csv_covid = read_csv(statURL + dayBeforeURL)
        except NameError:
            print('Bad date name')
            continue
        
    del csv_covid['FIPS'],csv_covid['Combined_Key']
    us_list = list(csv_covid['Admin2'])
    cr_list = list(csv_covid['Country_Region'])
    ps_list = list(csv_covid['Province_State'])
    lu_list = list(csv_covid['Last_Update'])
    cf_list = list(csv_covid['Confirmed'])
    dt_list = list(csv_covid['Deaths'])
    rc_list = list(csv_covid['Recovered'])
    ac_list = list(csv_covid['Active'])
    cfr_list = list(csv_covid['Case-Fatality_Ratio'])

    c_input = input('Enter country: ')
    if c_input.lower()=='us' or c_input.lower()=='usa' or c_input.lower()=='united states of america':
        c_input = 'US'
    else:
        c_input = c_input.title()
    if c_input not in cr_list:
        print('Bad country name, check spelling')
        continue
    indx = []
    for i in range(len(cr_list)):
        if cr_list[i]==c_input:
            indx.append(i)

    print('\n===================================')
    print('Covid-19 statistics for '+c_input.title())
    print('Last updated at',lu_list[indx[0]])
    print('===================================\n')

    for j in indx:
        if c_input.lower()=='us':
            print('\t'+str(us_list[j])+', '+str(ps_list[j])+'\n')
        else:
            if str(ps_list[j])=='Unknown':
                continue
            elif str(ps_list[j])=='nan':
                print()
                pass
            else:
                print('\t'+ps_list[j]+'\n')
        print('Confirmed cases:\t',cf_list[j])
        print('Deaths:\t\t\t',dt_list[j])
        print('Recovered:\t\t',rc_list[j])
        print('Active cases:\t\t',ac_list[j])
        print('Case-Fatality Ratio:\t',round(cfr_list[j],2))
        print('\n===================================\n')
    if input('Continue? (y/n): ').lower()=='y':
        continue
    else:
        print('Thanks for using the program :)')
        break
