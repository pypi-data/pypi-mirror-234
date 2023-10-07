
import sys,os,argparse
import globals
import json


parser=argparse.ArgumentParser()
parser.add_argument('-c','--config', help="specifies the configuration file to run", required=False,type=str)



def main(config_path=None):
    args=parser.parse_args()
    if args.config is not None:
        config_path=args.config
    elif config_path is not None:
        pass
    else:
        print("usage: [-h] -c CONFIG\n: error: the following arguments are required: -c/--config")
        return
    with open(config_path,"r",encoding="utf-8") as f:
        config=json.load(f)
        globals.init(**config)
        globals.start()


def run(config):
    with open(config,"r",encoding="utf-8") as f:
        config=json.load(f)
        globals.init(**config)
        globals.start()


if __name__=='__main__':
    main()







