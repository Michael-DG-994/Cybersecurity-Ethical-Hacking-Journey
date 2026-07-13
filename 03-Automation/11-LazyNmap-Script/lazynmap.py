
#i'm lazy so i did this to run the scans that we'll probably do tomorrow for the unit 2 week 5 project
#this one was meant for personal use and by that i mean once tomorrow for whatever test we have that'll probably have us do something similiar

import subprocess #i'll just run kali shell commands from python like TracerTNG
import json #machine readable json format that's useful for scripts or integrating ai reports and whatnot
import datetime #timestamping
import argparse #flags x modularity
import re #regular expression to normalize/parse nmap's output like i did TracerTNG
import os #enviroment path/file stuff

#Output formatting, i keep using this it's very tidy and looks nice
try: 
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    C_TITLE=Fore.CYAN+Style.BRIGHT #headers
    C_OK=Fore.GREEN  #success
    C_WARN=Fore.YELLOW #warning or missing requirements
    C_ERR=Fore.RED #errors
    C_INFO=Fore.BLUE+Style.BRIGHT #info
    C_RESET=Style.RESET_ALL #reset terminal to deafault
    C_BOLD=Style.BRIGHT #bold text
    C_DIM=Style.DIM #less important lines
except ImportError: #if colorama is missing the script still works but all strings will look the same and colorless
    C_TITLE=C_OK=C_WARN=C_ERR=C_INFO=C_RESET=C_BOLD=C_DIM=""

#BANNER i also keep using this it just looks neat idk it's very simple but clean
def banner():
    print(f"""
{C_TITLE}╔══════════════════════════════════════════════════════╗
║     lazynmap  - MIKE DG  -  Kali Linux Edition       ║
║       the laziest way to not get the job done        ║
╚══════════════════════════════════════════════════════╝{C_RESET}
""")

def parse_args(): #i really liked doing this for tracerTNG but it's even more necessary for this since some scans can take eons to finish so it's good i get to just test them separately (also helps modulating for needs)
    parser=argparse.ArgumentParser(
        description="Lazynmap: the laziest way to not get the job done"
    )
    parser.add_argument(
        "-t","--target", #specific target/range
        type=str,
        default="127.0.0.1", #to avoid annoyances i'll just put the default as localhost
        help="Target IP, Hostname, CIDR range (Default: 127.0.0.1)"
    )
    parser.add_argument(
        "-tp","--top",   #using the --top.ports flag
        type=int,
        default=1000, #same as nmap's default
        help="The top however many ports to scan in discovery (Default: top 1000)"
    )
    parser.add_argument(
        "-sa" "--skip-aggressive", #aggressive scan is very thorough so it'll be good as a final scan to run
        type=str,
        help="Skip final aggressive scan"
    )
    parser.add_argument(
        "-od","--output-dir",
        type=str,
        default=".", #save to current directory very neat
        help="Destination directory where reports will be saved", #figured this out with TracerTNG very comfortable to have them all one place and tidy + timestamped
    )
    parser.add_argument(
        "-T","--timing-intensity",
        type=int,
        default=4, #quick, rather than 3
        help="Intensity of the scan (Default: 4(fast)",
    )
    return parser.parse_args()

def run_nmap(cmd:list,label:str)->str: #function to run nmap commands receives the desired list of commands formulated with the necessary arguments and also the label for the scan phase and outputs the stdout as string
    print(f"{C_DIM}\n{"="*69}{C_RESET}")
    print(f"{C_WARN}Starting:{C_RESET} {label}")
    print(f"{C_WARN}Command line:{C_RESET} {C_DIM}{" ".join(cmd)}{C_RESET}")
    print(f"{C_DIM}\n{"="*69}{C_RESET}")

    try:
        result=subprocess.run(
            cmd,
            capture_output=True, #from this we get the stoud rather than cluttering the cli
            text=True, #str not bytes
            check=True, #if there's an error exit
        )
        print(result.stdout)
        if result.stderr: #if we get an error in the output
            print(f"{C_ERR}[ERROR]:{C_RESET} {C_DIM}{result.stderr}{C_RESET}") #output whatever caused it
        return result.stdout #output nmap we need to process
    except subprocess.CalledProcessError as e: #error while trying to run nmap
        print(f"{C_ERR}[ERROR]:{C_RESET} {C_DIM}{label}:{e}{C_RESET} w/{result.stderr}") #basically a debug line masked as an error message so i can see what exactly causes it
        return ""
    except FileNotFoundError: #nmap for some reason isn't on the machine or isn't in path, mostly here for completeness kali comes w ith
        print(f"{C_ERR}[ERROR]:{C_RESET} {C_DIM}nmap missing.{C_RESET}")

def ext_ports(nmap_output:str)->list: #from the first command we run i need to get ONLY the ports i know are responsive as to not lose time with this simpler test
    open_ports=[] #thought about using set() to avoid dupes but idk, i think i prefer a list rn
    pattern=re.compile(r"^(/d+)/\w+\s+open",re.MULTILINE) #i hate regex so much this whole thing's annoying
    #this basically tells to pick the digits at the start of the line, then ignore what's after / (the protocol) and then just get space and the "open", on every line. 
    matched=pattern.findall(nmap_output) #find all the related patterns in the output of nmap
    for port in matched:
        if port not in open_ports: #ignoring dupes
            open_ports.append(port)
    print(f"{C_INFO}\n Open ports:{C_RESET} {C_BOLD}{len(open_ports)}{C_RESET}")
    return open_ports #this i'll just space later with ",".join before giving it to the 2nd and 3rd scan but first i gotta turn them to str for the command

def str_port(port_list:list)->str:
    return ",".join(port_list) # -p 53,80,443,...

def save_report(data:dict,output_dir:str,timestamp:str): #json and txt get crapped out of this from the nmap output, the scan result dict and the timestamp for the file name
    os.makedirs(output_dir,exist_ok=True)#either the directory already exists or i make it used this on TracerTNG for the various outputs too
    json_path=os.path.join(output_dir,f"nmap_report_{timestamp}.json") #report for scripts/ai (in case i do it idk)
    with open(json_path,"w") as f:
        json.dump(data,f,indent=2)
    print(f"{C_OK}[JSON SAVED]:{C_RESET} {C_DIM}{json_path}{C_RESET}")
    txt_path=os.path.join(output_dir,f"nmap_report_{timestamp}.txt")
    with open(txt_path,"w") as f:
        f.write("="*69+"\n")
        f.write(f"SCAN REPORT\n")
        f.write("="*69+"\n\n")
        f.write(f"Target: {data["target"]}\n")
        f.write(f"Timestamp: {data["timestamp"]}\n")
        f.write(f"Open ports: {", ".join(data["open_ports"]) or 'none'}\n\n")
        for phase_name, phase_output in data["phases"].items():
            f.write(f"\n{"-"*69}\n")
            f.write(f"PHASE:{phase_name}\n")
            f.write(f"\n{"-"*69}\n")
            f.write(phase_output or "no output\n")
    print(f"{C_OK}[TXT SAVED]:{C_RESET} {C_DIM}{txt_path}{C_RESET}")

def main():
    banner()
    args=parse_args()
    target=args.target
    top=args.top
    timing_intensity=args.timing_intensity
    output_dir=args.output_dir
    timestamp=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"{C_OK}[TARGET]:{C_RESET} {C_DIM}{target}{C_RESET}")
    print(f"{C_OK}[SCOPE]:{C_RESET} {C_DIM}{top}{C_RESET}")
    print(f"{C_OK}[OUTPUT DIR.]:{C_RESET} {C_DIM}{output_dir}{C_RESET}")
    results={
        "target":target,
        "timestamp":timestamp,
        "timing":timing_intensity,
        "open_ports":[],
        "phases":{}
    }
    
    ph1_cmd=["nmap",f"--top-ports",str(top),f"-T{timing_intensity}",target] #could have made the -TX un parseargument but whatever
    ph1_output=run_nmap(ph1_cmd,f"{C_OK}Port Discovery{C_RESET} {C_DIM}(Scope: top {top} ports){C_RESET}")
    results["phases"]["ph1_port_discovery"]=ph1_output

    open_ports=ext_ports(ph1_output)
    results["open_ports"]=open_ports

    if not open_ports:
        print(f"{C_ERR}[ERROR]:{C_RESET} {C_DIM}NO open ports on this host/range {C_RESET}")
        save_report(results,output_dir,timestamp)
        return
    
    ports_str=str_port(open_ports)

    ph2_report=os.path.join(output_dir,f"service_scan_{timestamp}.txt") #directory/name of ph2 report
    ph2_cmd=[
        "nmap",
        "-sV",
        "-sC",
        f"-T{timing_intensity}"
        "-p",
        ports_str,
        "-oN",
        ph2_report,
        target
    ]
    ph2_output=run_nmap(ph2_cmd,f"service_scan_{timestamp}.txt")
    results["phases"]["ph2_service_detection"]=ph2_output

    if not args.skip_aggressive:
        aggro=os.path.join(output_dir,f"aggro_scan_{timestamp}")
        ph3_cmd=[
            "nmap",
            "-A",
            f"-T{timing_intensity}",
            "-p",
            ports_str,
            "-oA",
            aggro,
            target
        ]
        ph3_output=run_nmap(ph3_cmd,"Aggressive scan")
        results["phases"]["ph3_aggro_scan"]=ph3_output
    else:
        print(f"{C_OK}[SKIPPING AGGRESSIVE SCAN]]{C_RESET}")
        results["phases"]["ph3_aggro_scan"]="skipped"
    
    save_report(results,output_dir,timestamp)
    print(f"{C_OK}{C_BOLD}[REPORTS FINISHED]]{C_RESET}{C_RESET}")

if __name__ == "__main__":
    main()







