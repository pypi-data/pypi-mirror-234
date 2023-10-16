#!/usr/bin/env python

import argparse
import subprocess
import os
def Command(text=""):
    print("="*80)
    command = input("*"*4+f"FBC: {text} :> ")
    return command
def run(args):
    print(args)
    subprocess.run(['python', args.file])

def main():
    parameters = {
        "recertification":["recert","recet","rct"]
    }
    parser = argparse.ArgumentParser(description='Run a Python file')
    parser.add_argument('-file', type=str, help='the Python file to be executed')
    parser.add_argument('-file1', type=str, help='the Python file to be executed')
    args = parser.parse_args()
    #print(args)
    
    #print(command)
    footer__ ="=============================================POWERED BY MANLOW CHARUMBIRA==============================================="
    breaker =True
    while breaker:
        command = Command("Enter Command")
        if command.lower() in parameters['recertification']:
            print("-"*50+"\n"+" Enter Recert Type eg Postilion, direct inject etc"+"\n"+"-"*50)
            recert_type = Command("Enter Recertification type").lower()
            if recert_type in ["exit","out","ex","terminate","break","x"]:
                print(footer__)
                breaker = False
            elif recert_type.lower() in ["postilion","postillion","postl"]:
                subprocess.run(["python","main.py"])
        elif command.lower() in ["pam"]:
            
            subprocess.run(["python",os.path.join(os.getcwd(),"priviledged_user_automation","auto.py")])
        elif command.lower() in ["exit","out","ex","terminate","break","x"]:
            print(footer__)
        elif command.lower()=="fbc":
            about="""
==========================*==============FBC INFOSEC PROCESSES AUTOMATION TOOL===================*======================

************************AUTOMATING PROCESSES SUCH AS CHECKLISTS, RECERTIFICATIONS AND MANY MORE*************************

"""
            print(about)
            continue
        else:
            print("=============================UKNOWN COMMAND PLEASE TRY AGAIN=========================================")
            
 

if __name__ == '__main__':
    main()