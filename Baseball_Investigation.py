from bs4 import BeautifulSoup, SoupStrainer
import urllib.request, pickle, time, csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.patches as mpatches


all_data = []


def strain_data():
    #http = httplib2.Http()
    response = urllib.request.urlopen('https://www.brooksbaseball.net/tabs.php?player=477132&p_hand=-1&ppos=-1&cn=200&compType=none&risp=0&1b=0&2b=0&3b=0&rType=perc&balls=-1&strikes=-1&b_hand=-1&time=month&minmax=ci&var=gl&s_type=2&gFilt=&startDate=&endDate=')

    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href') and str(link).find("pfxVB") >= 0:
            strain_data_2(link['href'])
            time.sleep(2)
            
def strain_data_2(link):
    response = urllib.request.urlopen(link)

    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href') and str(link).find("size=500") >= 0:
            scrape_data("https://www.brooksbaseball.net/pfxVB/" + link['href'])
            time.sleep(2)
            
def scrape_data(link):
    

    page = urllib.request.urlopen(link)
    time.sleep(2)
    soup = BeautifulSoup(page, 'html.parser')

    #Trim data, append
    for c in soup.find_all("td"):
        data = str(c).replace('<td>','').replace('</td>','')
        all_data.append(data)

    #Save data
    with open('ahh.pkl','wb') as f:
        pickle.dump(all_data,f)

 
def panda_time():
    
    # Getting back the objects:
    
    data = pd.read_csv('titled_eggs.csv')
    
    ff_data = data[data.mlbam_pitch_name=='FF']

    filtered_df = ff_data[['start_speed','type','pdes']]

    filtered_df.sort_values(by=['start_speed'], inplace=True)

    filtered_df.to_csv("filtered_df.csv",index=False)

    return filtered_df



def work_with_data_contact(filtered_df):

    contact_list = []
    average_speed_list = []
    
    bucket_size = 200
    for i in range(int(len(filtered_df)/bucket_size)):
        data_point_data = filtered_df[i*bucket_size:(i+1)*bucket_size]

        ball = sum(pd.Series(data_point_data['pdes']).str.contains(r'Ball'))
        c_strike = sum(pd.Series(data_point_data['pdes']).str.contains(r'Called Strike'))
        s_strike = sum(pd.Series(data_point_data['pdes']).str.contains(r'Swinging Strike'))

        contact = len(data_point_data)-ball-c_strike-s_strike
        swings = contact + s_strike
        contact_list.append(contact/swings)

        average_speed_list.append(sum(data_point_data['start_speed'])/len(data_point_data))
    
    #Turn data into something digestable
    plt.plot(average_speed_list,contact_list)
    plt.title("Contact % vs Pitch Speed for Clayton Kershaw's Fastballs, 2008 - 2018")
    plt.xlabel("Speed (mph)")
    plt.ylabel("Contact %")

    z = np.polyfit(average_speed_list, contact_list, 1)
    p = np.poly1d(z)
    red_patch = mpatches.Patch(color='orange', label='y=%.6fx+(%.6f)'%(z[0],z[1]))
    plt.plot(average_speed_list,p(average_speed_list),'--')
    plt.legend(handles=[red_patch])
    plt.savefig('contact_percent.png')
    plt.close()

def work_with_data_swing(filtered_df):

    swing_list = []
    average_speed_list = []
    
    bucket_size = 200
    for i in range(int(len(filtered_df)/bucket_size)):
        data_point_data = filtered_df[i*bucket_size:(i+1)*bucket_size]

        ball = sum(pd.Series(data_point_data['pdes']).str.contains(r'Ball'))
        c_strike = sum(pd.Series(data_point_data['pdes']).str.contains(r'Called Strike'))
        s_strike = sum(pd.Series(data_point_data['pdes']).str.contains(r'Swinging Strike'))

        contact = bucket_size-ball-c_strike-s_strike
        swings = contact + s_strike
        swing_list.append((contact+s_strike)/bucket_size)

        average_speed_list.append(sum(data_point_data['start_speed'])/bucket_size)
    
    #Turn data into something digestable
    plt.plot(average_speed_list,swing_list)
    plt.title("Swing % vs Pitch Speed for Clayton Kershaw's Fastballs, 2008 - 2018")
    plt.xlabel("Speed (mph)")
    plt.ylabel("Swing %")

    z = np.polyfit(average_speed_list, swing_list, 1)
    p = np.poly1d(z)
    red_patch = mpatches.Patch(color='orange', label='y=%.6fx+(%.6f)'%(z[0],z[1]))
    plt.plot(average_speed_list,p(average_speed_list),'--')
    plt.legend(handles=[red_patch])
    plt.savefig('swing_percentage.png')
    plt.close()

def work_with_data_swstr(filtered_df):

    swing_list = []
    average_speed_list = []
    
    bucket_size = 200
    for i in range(int(len(filtered_df)/bucket_size)):
        data_point_data = filtered_df[i*bucket_size:(i+1)*bucket_size]

        ball = sum(pd.Series(data_point_data['pdes']).str.contains(r'Ball'))
        c_strike = sum(pd.Series(data_point_data['pdes']).str.contains(r'Called Strike'))
        s_strike = sum(pd.Series(data_point_data['pdes']).str.contains(r'Swinging Strike'))

        contact = bucket_size-ball-c_strike-s_strike
        swings = contact + s_strike
        swing_list.append((s_strike)/bucket_size)

        average_speed_list.append(sum(data_point_data['start_speed'])/bucket_size)
    
    #Turn data into something digestable
    plt.plot(average_speed_list,swing_list)
    plt.title("SwingStr % vs Pitch Speed for Clayton Kershaw's Fastballs, 2008 - 2018")
    plt.xlabel("Speed (mph)")
    plt.ylabel("Swing %")

    z = np.polyfit(average_speed_list, swing_list, 1)
    p = np.poly1d(z)
    red_patch = mpatches.Patch(color='orange', label='y=%.6fx+(%.6f)'%(z[0],z[1]))
    plt.plot(average_speed_list,p(average_speed_list),'--')
    plt.legend(handles=[red_patch])
    plt.savefig('swstr_percentage.png')
    plt.close()



####################

#strain_data()
#relevant_data = work_with_data()

filtered_df = panda_time()
work_with_data_contact(filtered_df)
work_with_data_swing(filtered_df)
work_with_data_swstr(filtered_df)
