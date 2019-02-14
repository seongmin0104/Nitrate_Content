import os

path = 'C:/Users/Always9/Desktop/pp'
list_path = os.listdir(path)

total_repeats=4
total_samples=10
fieldname='Field022'

repeats_cnt  = 0
samples_cnt = 1
cnt = -2

for filename in list_path:
    Field_date = fieldname + '_' + filename[4:12]
    cnt += 1

    if filename[4:12] == list_path[cnt][4:12]:
        if repeats_cnt  < 5:
            repeats_cnt += 1
        elif repeats_cnt  == 5:
            repeats_cnt -= 4
            samples_cnt += 1

    else:
        samples_cnt =0
        if repeats_cnt  < 5 and cnt == -1:
            repeats_cnt += 1
            samples_cnt = 1
        elif repeats_cnt  < 5:
            repeats_cnt += 1
        elif repeats_cnt  == 5:
            repeats_cnt -= 4
            samples_cnt += 1

    if samples_cnt >= total_samples and repeats_cnt != (total_repeats+1):
        os.rename(os.path.join(path, filename), os.path.join(path, Field_date + '_below' +str(samples_cnt) + str(0) + str(repeats_cnt) + '.jpg'))
    elif samples_cnt >= total_samples and repeats_cnt == (total_repeats+1):
        os.rename(os.path.join(path, filename), os.path.join(path, Field_date + '_above' + str(samples_cnt) + '.jpg'))
    elif samples_cnt < total_samples and repeats_cnt == (total_repeats+1):
        os.rename(os.path.join(path, filename), os.path.join(path, Field_date + '_above' + str(0) + str(samples_cnt) + '.jpg'))
    elif samples_cnt < total_samples and repeats_cnt != (total_repeats+1):
        os.rename(os.path.join(path, filename), os.path.join(path, Field_date + '_below'+str(0) + str(samples_cnt) + str(0) + str(repeats_cnt) + '.jpg'))

