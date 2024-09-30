import argparse
import re
import os
import sys, json
import time


def do_amd_check(profile):
    # print('\nBIOS Profile is %s' % profile)
    bios_value, check_ret = amd_common_bios(profile)
    return (bios_value, check_ret)

def amd_common_bios(profile):
    amd_common_BIOS = Scelnx_bios()
    # print(profile)
    tool_package = libbasedir + '/AMD_Bios/scelnx'
    # print (tool_package)
    print( 'Start to get BIOS CFG')
    os.system('%s/scelnx_64_p /o /hb /s %s/bios_cfg_file' % (tool_package, tool_package))
    print('#############################Show current BIOS CFG#################################' )
    bios_value_dict = amd_common_BIOS.current_bios(profile)
    print( '#############################Check Current AMD BIOS CFG################################')
    print(profile )
    check_ret = amd_common_BIOS.bios_check_result(profile)
    return (bios_value_dict, check_ret)

class Scelnx_bios(object):

    def __init__(self):
        self.fir_file = []
        self.sed_file = []
        self.bios_check = []
        self.bios_cfg_file = sys.path[0] + '/scelnx_bios.txt'

    def get_bios(self, bios_list):
        bios_value_lst = ['0', '1']
        for line in bios_list[5:]:
            if '*[' in line:
                bios_value_lst[0] = bios_list[0].split('=')[1].strip().lower()
                bios_value_lst[1] = line.lstrip('Options').strip().lstrip('=').split('//')[0].lower()
                print('%-35s %10s' % (bios_list[0].split('=')[1].strip(), line.lstrip('Options').strip().lstrip('=').split('//')[0]))

        return bios_value_lst
    def current_bios(self, profile):
        cur_path = sys.path[0]
        # print(cur_path)
        infofile = cur_path + '/AMD_Bios/bios_value.json'
        bios_cfg_file = cur_path + '/AMD_Bios/scelnx/bios_cfg_file'
        bios_check_file = profile
        print(infofile)
        self.fir_file = []
        self.sed_file = []
        bios_value_dict = {}
        print('%-35s %10s' % ('BIOS Setup Name', 'Current Value'))
        with open(bios_cfg_file, 'r') as a:
            for line in a:
                self.fir_file.append(line)
            # os.popen("echo %s >> ./log.log"%self.fir_file)
            # print(self.sed_file)
            for line in self.fir_file:
                # print(self.sed_file)
                if line in '\n':
                    with open(bios_check_file, 'r') as f:
                        for line in f:
                            if line.split('=')[0] in self.sed_file[0]:
                                for line in self.sed_file:
                                    pass

                                bios_value_lst = self.get_bios(self.sed_file)
                                bios_value_dict[bios_value_lst[0]] = bios_value_lst[1]

                    self.sed_file = []
                else:
                    self.sed_file.append(line.lstrip('='))

        f = open(infofile, 'w')
        f.writelines(json.dumps(bios_value_dict))
        f.close()
        return bios_value_dict


    def bios_check_result(self, profile):
        cur_path = sys.path[0]
        # print(cur_path)
        bios_cfg_file = cur_path + '/AMD_Bios/scelnx/bios_cfg_file'
        bios_check_file = profile
        self.sed_file = []
        self.fir_file = []
        fail_flag = 0
        print('%-35s %-25s %-15s %5s' % ('BIOS Setup Name', 'Current Value', 'Gold Value',
                                         'Check Result'))
        with open(bios_cfg_file, 'r') as a:
            for line in a:
                self.fir_file.append(line)

            for line in self.fir_file:
                if line in '\n':
                    with open(bios_check_file, 'r') as f:
                        for line in f:
                            if line.split('=')[0] in self.sed_file[0]:
                                for line in self.sed_file:
                                    pass

                                ret = self.bios_setup_check(self.sed_file, bios_check_file)
                                if ret == 'fail':
                                    fail_flag = 1

                    self.sed_file = []
                else:
                    self.sed_file.append(line.lstrip('='))

        if fail_flag == 1:
            return 'fail'
        else:
            return 'pass'

    def bios_setup_check(self, bios_list, bios_check_file):
        fail_flag = 0
        for line in bios_list[5:]:
            self.setup_name = bios_list[0].split('=')[1].strip()
            if '*[' in line:
                self.current_value = line.lstrip('Options').strip().lstrip('=').split('//')[0].strip()
                with open(bios_check_file, 'r') as f:
                    for line in f:
                        if line.split('=')[0] in self.setup_name:
                            self.gold_value = line.split('=')[1].strip()
                            if self.gold_value in self.current_value:
                                self.check_result = 'Pass'
                            else:
                                self.check_result = 'Fail'
                                # print('fail')
                                fail_flag = 1

                print('%-35s %-25s %-15s %5s' % (self.setup_name, self.current_value, self.gold_value, self.check_result))

        if fail_flag == 1:
            return 'fail'
        else:
            return 'pass'
def setoption(libbasedir,args,profile):
    tool_package = libbasedir + '/AMD_Bios/scelnx'
    # request=args.set
    request=args.set
    option = request.split("=")[0]
    flag = request.split("=")[1]
    print("set option:  "+str(option))
    print("set value:  "+str(flag))
    index = 0
    wflag = 0
    cur_path = sys.path[0]
    new_bios_cfg_file = cur_path + "/AMD_Bios/scelnx/new_bios_cfg_file"
    bios_cfg_file = cur_path + '/AMD_Bios/scelnx/bios_cfg_file'
    bios_check_file = profile
    fir_file = []
    sed_file = []
    bios_list=[]
    with open(bios_cfg_file, 'r') as a:
        for line in a:
            fir_file.append(line)
        for line in fir_file:
            if line in '\n':
                with open(bios_check_file, 'r') as f:
                    for line in f:
                        # print(sed_file)
                        if line.split('=')[0] in sed_file[0]:
                            for line in sed_file:
                                pass
                            bios_list=sed_file
                sed_file = []
            else:
                sed_file.append(line.lstrip('='))
    bios_list_new = []
    # print(sed_file)
    for i in bios_list[:6]:
        bios_list_new.append(i)
    for i in bios_list[6:]:
        if flag in i:
            bios_list_new.append(i.replace("[", "*["))
        elif "*[" in i:
            bios_list_new.append(i.replace("*",""))
        else:
            bios_list_new.append(i)
    with open(bios_cfg_file, 'r') as a:
        for line in a:
            if option in line:
                wflag=1
                for j in bios_list_new:
                    with open(new_bios_cfg_file, 'a') as b:
                        b.write(j)
            if wflag == 1:
                if index < len(bios_list_new):
                    index+=1
                    continue
            with open(new_bios_cfg_file, 'a') as b:
                b.write(line)
    os.system('%s/scelnx_64_p /i /s %s/bios_cfg_file' % (tool_package, tool_package))

def replace_in_file(filename, old_text, new_text):
    with open(filename, 'r') as file:
        content = file.read()
        content = re.sub(old_text, new_text, content)
    with open(filename, 'w') as file:
        file.write(content)

def checkVender():
    return os.popen("ipmitool fru |grep -i 'Board Mfg' |awk NR==2 |awk '{print $4}'").read()

def setSMoption(libbasedir,args):
    request = args.set
    setname = request.split("=")[0]
    setvalue = '"'+request.split("=")[1]+'"'
    time.sleep(3)
    os.popen("sudo %s/sum_2.14.0_Linux_x86_64/sum -c GetCurrentBiosCfg --file %s/smbios.file"%(libbasedir,libbasedir))
    time.sleep(10)
    modelname = "/smbios.file"
    newmodelname = "/newsmbios.file"
    path = libbasedir
    filename = path + modelname
    newfilename = path + newmodelname
    with open(filename, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            if "Setting name" in line and setname in line:
                # print(line)
                options = line.split()
                for option in options:
                    if "selectedOption" in option:
                        selectedOption = option.split('=')[1]
                        if setvalue != selectedOption:
                            line = re.sub(selectedOption, setvalue, line)
                # print(line)
            with open(newfilename, 'a') as b:
                b.write(line)
    os.popen("sudo %s/sum_2.14.0_Linux_x86_64/sum -c ChangeBiosCfg --file %s/newsmbios.file"%(libbasedir,libbasedir))
    time.sleep(10)
    print("Please reboot")
    return
def do_SMamd_check(libbasedir,args):
    request = args.check
    setname = request.split("=")[0]
    setvalue = '"'+request.split("=")[1]+'"'
    time.sleep(3)
    print("sudo %s/sum_2.14.0_Linux_x86_64/sum -c GetCurrentBiosCfg --file %s/smbios.file" % (libbasedir, libbasedir))
    os.popen("sudo %s/sum_2.14.0_Linux_x86_64/sum -c GetCurrentBiosCfg --file %s/smbios.file" % (libbasedir, libbasedir))
    time.sleep(10)
    modelname = "/smbios.file"
    path = libbasedir
    filename = path + modelname
    with open(filename, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            if "Setting name" in line and setname in line:
                print(line)
                options = line.split()
                for option in options:
                    if "selectedOption" in option:
                        selectedOption = option.split('=')[1]
                        print(setvalue)
                        print(selectedOption)
                        if setvalue == selectedOption:
                            print("The current value is the same as the target value")
                        else:
                            print("The current value is different from the target value")
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Change the BIOS options."
    )
    parser.add_argument("-s","--set", type=str, help="A=B")
    parser.add_argument("-c", "--check", type=str, help="A=B")
    args = parser.parse_args()
    libbasedir = os.path.abspath(os.getcwd())
    amd_bios_profile = os.path.join(libbasedir, 'ppio_amd_bios.txt')
    vender=str(checkVender()).strip()
    print(args)
    if vender == "Supermicro":
        os.popen("tar -zxvf %s/sum_2.14.0_Linux_x86_64_20240215.tar.gz -C %s"%(libbasedir,libbasedir))
        if args.set:
            setSMoption(libbasedir,args)
        else:
            do_SMamd_check(libbasedir,args)
    else:
        if args.set:
            setoption(libbasedir,args,amd_bios_profile)
        else:
            do_amd_check(amd_bios_profile)


