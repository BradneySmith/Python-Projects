from bs4 import BeautifulSoup
import requests

def tidy(text):
    return text.lstrip().rstrip()

def print_job(data_list):
    print(data_list[0])
    print('Company', data_list[1])
    print('Salary:', data_list[2])
    print('Location:', data_list[3])
    print('Grade:', data_list[4])
    print('Deadline:', data_list[5])
    print('Link:', data_list[6]+'\n')
    

source = requests.get("https://www.gradcracker.com/search/all-disciplines/engineering-graduate-jobs").text
soup = BeautifulSoup(source, 'lxml')

job_profiles = soup.findAll("div", {"class": "job-item"})

all_job_data = []
job_counter = 0

for profile in job_profiles:
    try:
        # Store job attributes in list, starting with title
        data_list = [tidy(profile.h2.a.text)]
        
        # Get company name
        data_list.append(profile.h2.a['title'][profile.h2.a['title'].find('with')+5:])
        
        # Get salary, location, grade and deadline
        data = profile.findAll('li')
        for datum in data:
            if tidy(datum.text)[0:8] == 'Deadline':
                data_list.append(tidy(datum.text)[10:])
            else:
                data_list.append(tidy(datum.text))
        
        # Get URL
        _, url = profile.find_all('a', href=True)
        data_list.append(url['href'])
        
        all_job_data.append(data_list)
    
        job_counter += 1
    
        #print(profile.prettify())
    except:
        pass

# Change key_num to cycle through the attributes of each job listing
# 0 - Title
# 1 - Company
# 2 - Salary
# 3 - Location
# 4 - Grade
# 5 - Deadline
# 6 - Link

key_num = 1
all_job_data.sort(key=lambda x: x[key_num])

# Print the ordered list of jobs
print('Found '+str(job_counter)+' jobs \n')
for job in all_job_data:
    print_job(job)