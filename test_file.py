import sys
import argparse

def parse_args():
    pass_args = argparse.ArgumentParser()
    pass_args.add_argument("--name", required=True)
    pass_args.add_argument("--reg_no", type=int,required=True)
    pass_args.add_argument("--marks",type=int,required=True)
     
    return pass_args.parse_args()

class MarkSheet:
    def __init__(self,name,reg_no, marks):
        self.name = name
        self.reg_no = reg_no
        self.marks = marks

    def fetch_result(self):
        if (self.marks < 35):
            result = 'fail'
        else:
            result = 'pass'
        return result

def main():
   
    args = parse_args()
    ms = MarkSheet(args.name,args.reg_no,args.marks)
    result = ms.fetch_result()
    print(f"{args.name} with {args.reg_no} result is: {result}")

if __name__ == '__main__':
    main()