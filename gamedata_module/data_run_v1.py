from grabscreen import grab_screen
from getInputs import input_check_bro, VK_CODE
import os
import time
import cv2
from _datetime import datetime
import sys
import copy

'''
미래국방 데이터 수집 모듈

- 영상
- 키보드 & 마우스 입력

'''

## 기본설정
# 저장 폴더명 설정
save_folder_name = '2021'
download_path = os.getcwd() + '\\download\\' + save_folder_name
# print(download_path)
if not os.path.isdir(download_path):
    print("@ make download directory")
    os.mkdir(download_path)

# 윈도우 설정
screen_width = 1920
screen_height = 1080
resize_width = 960
resize_height = 540

# 입력 설정
output_code = copy.deepcopy(VK_CODE)

# 키보드 입력 output 형식으로 변환
def keys_to_output(inputs):
    '''

    Convert inputs to a multi-hot array

    '''
    print(inputs)

    output = list(range(0, output_code.values().__len__()))
    output_idx = 0
    for oc in output_code.values():
        if oc in inputs:
            output[output_idx] = 1
        else:
            output[output_idx] = 0
        output_idx = output_idx + 1

    return output

#  데이터수집(영상, 키보드 입력, 마우스 입력)
def main():
    for i in list(range(4))[::-1]:
        print(i + 1)
        time.sleep(1)

    paused = False
    while (True):
        if not paused:
            prev_time = time.time()

            # screen_width X screen_height windowed mode
            screen = grab_screen(region=(0, 0, screen_width-1, screen_height-1))
            # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            # screen = cv2.resize(screen, (resize_width, resize_height))

            # resize to something a bit more acceptable for a CNN
            inputs = input_check_bro()
            output = keys_to_output(inputs)

            save_time = '\\{:%H_%M_%S_%f}'.format(datetime.now())
            save_img_path = download_path + save_time + ".jpg"
            save_input_path = download_path + save_time + ".txt"
            cv2.imwrite(save_img_path, screen)
            f = open(save_input_path, 'w')
            f.write(str(output))
            f.close()

            print(save_time)
            print(output)
            print()

            # print(training_data)

            # 시간확인
            cur_time = time.time()
            sec = cur_time - prev_time
            prev_time = cur_time
            fps = 1 / (sec)
            # print("Time {0}".format(sec))
            print("Time {0} , Estimated fps {1}".format(sec, fps))

        # 일시정지 및 정지
        inputs = input_check_bro()
        if '[' in inputs:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
        elif ']' in inputs:
            sys.exit()

main()






