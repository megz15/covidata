'''
    Program: Covidata
    Version: 1.4
    Author : Meghraj Goswami
    Github : github.com/megz15/covidata
'''

from pandas import read_csv
from urllib.error import HTTPError
from datetime import date,timedelta
from webbrowser import open as wb
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import warnings
warnings.filterwarnings("ignore",category=UserWarning)
plt.style.use('bmh')

print('*** Covidata - A simple Covid-19 tracker ***')
print('Data collected from GitHub repo of JHU CSSE')
#wb('https://github.com/CSSEGISandData/COVID-19')
print('Tip:  Leave date field empty to get latest info!\nNote: Timestamps are in UTC format (GMT+0)')

while True:
    choice=int(input('\nChoose->\n1. Create graph\n2. Show latest data/data at particular date\n3. Get info on Covid-19\n4. Exit\nYour choice: '))
    if choice==1:
        p_s,c_r,datelist,graf_indx = [],[],[],[]
        conf,deth,recv = [],[],[]
        csv_conf = read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        csv_deth = read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
        csv_recv = read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
        del csv_conf['Lat'],csv_conf['Long'],csv_deth['Lat'],csv_deth['Long'],csv_recv['Lat'],csv_recv['Long']
        p_s = csv_conf['Province/State']
        c_r = csv_conf['Country/Region']
        country_name = input('\nEnter country: ')
        if country_name.lower()=='us' or country_name.lower()=='usa' or country_name.lower()=='united states of america':
            country_name = 'US'
        else:
            country_name = country_name.title()
        for i in range(len(c_r)):
            if c_r[i]==country_name:
                graf_indx.append(i)
                
        for i in graf_indx:
            conf.clear(),recv.clear(),deth.clear(),datelist.clear()
            if str(p_s[i])=='nan':
                if len(graf_indx)!=1:
                    continue
                for row in csv_conf:
                    if row=='Province/State' or row=='Country/Region' or row=='Lat' or row=='Long':
                        continue
                    datelist.append(row)
                    conf.append(csv_conf[csv_conf['Country/Region']==country_name][row].item())
                    deth.append(csv_deth[csv_deth['Country/Region']==country_name][row].item())
                    recv.append(csv_recv[csv_recv['Country/Region']==country_name][row].item())
            else:
                for row in csv_conf:
                    if row=='Province/State' or row=='Country/Region' or row=='Lat' or row=='Long':
                        continue
                    datelist.append(row)
                    conf.append(csv_conf[csv_conf['Province/State']==p_s[i]][row].item())
                    deth.append(csv_deth[csv_deth['Province/State']==p_s[i]][row].item())
                    recv.append(csv_recv[csv_recv['Province/State']==p_s[i]][row].item())
            if str(p_s[i])=='nan':
                plt.figure('Covidata for '+country_name)
            else:
                plt.figure('Covidata for '+p_s[i]+' in '+country_name)
            plt.plot(datelist,conf,label='Confirmed',color='#2196F3')
            plt.plot(datelist,deth,label='Deaths',color='#FF5252')
            plt.plot(datelist,recv,label='Recovered',color='#8BC34A')
            plt.axes().xaxis.set_major_locator(tick.MultipleLocator(7))
            plt.axes().xaxis.set_minor_locator(tick.MultipleLocator(1))
            plt.xticks(rotation=45)
            plt.legend()
            plt.text(datelist[-1],conf[-1],conf[-1],ha='right')
            plt.text(datelist[-1],deth[-1],deth[-1],ha='right')
            plt.text(datelist[-1],recv[-1],recv[-1],ha='right')
            plt.subplots_adjust(left=0.04, right=0.99, top=0.93, bottom=0.12)
        print('Graph created!')
        plt.show()
    elif choice==2:
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
                break
    elif choice==3:
        print('\nOpening web browser...\nOpening mohfw.gov.in')
        wb('https://www.mohfw.gov.in')
    elif choice==4:
        print('\nExiting',end='')
        for i in '...':
            sleep(0.5)
            print(i,end='')
        sleep(0.5)
        break
    else:
        print('Bad choice number, try again')
