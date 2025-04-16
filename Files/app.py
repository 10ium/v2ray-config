import pybase64
import base64
import requests
import binascii
import os

# Define a fixed timeout for HTTP requests
TIMEOUT = 20  # seconds

# Define the fixed text for the initial configuration
fixed_text = """#profile-title: base64:8J+GkyBHaXRodWIgfCBCYXJyeS1mYXIg8J+ltw==
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/10ium/V2ray-Config
#profile-web-page-url: https://github.com/10ium/V2ray-Config
"""

# Base64 decoding function
def decode_base64(encoded):
    decoded = ""
    for encoding in ["utf-8", "iso-8859-1"]:
        try:
            decoded = pybase64.b64decode(encoded + b"=" * (-len(encoded) % 4)).decode(encoding)
            break
        except (UnicodeDecodeError, binascii.Error):
            pass
    return decoded

# Function to decode base64-encoded links with a timeout
def decode_links(links):
    decoded_data = []
    for link in links:
        try:
            response = requests.get(link, timeout=TIMEOUT)
            encoded_bytes = response.content
            decoded_text = decode_base64(encoded_bytes)
            decoded_data.append(decoded_text)
        except requests.RequestException:
            pass  # If the request fails or times out, skip it
    return decoded_data

# Function to decode directory links with a timeout
def decode_dir_links(dir_links):
    decoded_dir_links = []
    for link in dir_links:
        try:
            response = requests.get(link, timeout=TIMEOUT)
            decoded_text = response.text
            decoded_dir_links.append(decoded_text)
        except requests.RequestException:
            pass  # If the request fails or times out, skip it
    return decoded_dir_links

# Filter function to select lines based on specified protocols
def filter_for_protocols(data, protocols):
    filtered_data = []
    for line in data:
        if any(protocol in line for protocol in protocols):
            filtered_data.append(line)
    return filtered_data

# Create necessary directories if they don't exist
def ensure_directories_exist():
    output_folder = os.path.abspath(os.path.join(os.getcwd(), ".."))
    base64_folder = os.path.join(output_folder, "Base64")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(base64_folder):
        os.makedirs(base64_folder)

    return output_folder, base64_folder

# Main function to process links and write output files
def main():
    output_folder, base64_folder = ensure_directories_exist()  # Ensure directories are created

    protocols = ["vmess", "vless", "trojan", "ss", "ssr", "hy2", "tuic", "warp://"]
    links = [
        "https://raw.githubusercontent.com/AzadNetCH/Clash/refs/heads/main/AzadNet_iOS.txt",
        "https://raw.githubusercontent.com/Ashkan-m/v2ray/refs/heads/main/Sub.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/clashmeta.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/ndnode.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/nodefree.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/v2rayshare.txt",
        "https://raw.githubusercontent.com/Barabama/FreeNodes/refs/heads/main/nodes/yudou66.txt",
        "https://raw.githubusercontent.com/Ennzo0/V2ray/refs/heads/main/all.txt",
        "https://raw.githubusercontent.com/Huibq/TrojanLinks/refs/heads/master/links/ssr",
        "https://raw.githubusercontent.com/Huibq/TrojanLinks/refs/heads/master/links/vmess",
        "https://raw.githubusercontent.com/Leon406/SubCrawler/refs/heads/main/sub/share/hysteria2",
        "https://raw.githubusercontent.com/Leon406/SubCrawler/refs/heads/main/sub/share/vless",
        "https://raw.githubusercontent.com/Pawdroid/Free-servers/refs/heads/main/sub",
        "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/refs/heads/main/splitted/hy2",
        "https://raw.githubusercontent.com/Surfboardv2ray/TGParse/refs/heads/main/splitted/hysteria2",
        "https://raw.githubusercontent.com/aiboboxx/v2rayfree/refs/heads/main/v2",
        "https://raw.githubusercontent.com/ermaozi01/free_clash_vpn/refs/heads/main/subscribe/v2ray.txt",
        "https://raw.githubusercontent.com/free18/v2ray/refs/heads/main/v.txt",
        "https://raw.githubusercontent.com/ripaojiedian/freenode/refs/heads/main/sub",
        "https://raw.githubusercontent.com/yebekhe/vpn-fail/refs/heads/main/sub-link",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/hysteria",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/juicity",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/reality",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/shadowsocks",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/trojan",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/tuic",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vmess",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_1.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_2.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_3.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_4.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_1.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_2.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_3.txt",
        "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mtn/sub_4.txt",
        "https://raw.githubusercontent.com/ts-sf/fly/refs/heads/main/v2",
        "https://raw.githubusercontent.com/voken100g/AutoSSR/master/online",
        "https://raw.githubusercontent.com/voken100g/AutoSSR/master/recent",
        "https://sDTz6J.absslk.xyz/3e1fc97dfeebc0778a6176c1742d06de",
        "https://joYAQx.mcsslk.xyz/62e8b56aa7f98dcfb44c5a77291ab2ff",
        "https://muma16fx.netlify.app",
        "https://qiaomenzhuanfx.netlify.app",
    ]
    dir_links = [
        "https://raw.githubusercontent.com/10ium/V2Hub3/main/merged",
        "https://raw.githubusercontent.com/10ium/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/Bahrain/config.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/Germany/config.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/Netherlands/config.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/Iran/config.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/Sweden/config.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/Turkey/config.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/United%20Kingdom/config.txt",
        "https://raw.githubusercontent.com/Epodonios/bulk-xray-v2ray-vless-vmess-...-configs/refs/heads/main/sub/United%20States/config.txt",
        "https://raw.githubusercontent.com/Everyday-VPN/Everyday-VPN/refs/heads/main/subscription/main.txt",
        "https://raw.githubusercontent.com/HDYOU/porxy/refs/heads/main/combine.txt",
        "https://raw.githubusercontent.com/MrMohebi/xray-proxy-grabber-telegram/master/collected-proxies/row-url/actives.txt",
        "https://raw.githubusercontent.com/NiREvil/vless/refs/heads/main/sub/SSTime",
        "https://raw.githubusercontent.com/Rayan-Config/Rayan-Config.github.io/refs/heads/main/ALL",
        "https://raw.githubusercontent.com/Rayan-Config/Rayan-Config.github.io/refs/heads/main/WG",
        "https://raw.githubusercontent.com/Rayan-Config/HUB/refs/heads/main/H-I",
        "https://raw.githubusercontent.com/Rayan-Config/HUB/refs/heads/main/H-II",
        "https://raw.githubusercontent.com/Rayan-Config/HUB/refs/heads/main/H-III",
        "https://raw.githubusercontent.com/Rayan-Config/HUB/refs/heads/main/H-IV",
        "https://raw.githubusercontent.com/Rayan-Config/HUB/refs/heads/main/H-V",
        "https://raw.githubusercontent.com/ResistalProxy/V2Ray/refs/heads/master/server.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/custom/udp.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/refs/heads/main/custom/ipv6.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/refs/heads/main/custom/mahsa.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/refs/heads/main/output/bugfix.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/refs/heads/main/output/converted.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/output/US.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/output/IR.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/selector/random",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/output/converted.txt",
        "https://raw.githubusercontent.com/Surfboardv2ray/Proxy-sorter/main/selector/random",
        "https://raw.githubusercontent.com/Surfboardv2ray/v2ray-worker-sub/refs/heads/master/providers/ir",
        "https://raw.githubusercontent.com/ermaozi/get_subscribe/refs/heads/main/subscribe/v2ray.txt",
        "https://raw.githubusercontent.com/freedomnet25500/newyearsub/refs/heads/main/ss",
        "https://raw.githubusercontent.com/hfarahani/pr/refs/heads/main/pr.txt",
        "https://raw.githubusercontent.com/iPsycho1/Subscription/refs/heads/main/iPsycho",
        "https://raw.githubusercontent.com/iPsycho1/Subscription/refs/heads/main/iPsycho_Test-Config",
        "https://raw.githubusercontent.com/liketolivefree/kobabi/refs/heads/main/sub.txt",
        "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
        "https://raw.githubusercontent.com/miladtahanian/V2RayCFGDumper/refs/heads/main/config.txt",
        "https://raw.githubusercontent.com/moeinkey/key/refs/heads/main/ssh",
        "https://raw.githubusercontent.com/ndsphonemy/proxy-sub/refs/heads/main/my.txt",
        "https://raw.githubusercontent.com/ndsphonemy/proxy-sub/refs/heads/main/lt-sub.txt",
        "https://raw.githubusercontent.com/ndsphonemy/proxy-sub/refs/heads/main/hys-tuic.txt",
        "https://raw.githubusercontent.com/ndsphonemy/proxy-sub/refs/heads/main/default.txt",
        "https://raw.githubusercontent.com/peasoft/NoMoreWalls/refs/heads/master/list_raw.txt",
        "https://raw.githubusercontent.com/rb360full/V2Ray-Configs/refs/heads/main/Reza-2",
        "https://raw.githubusercontent.com/rb360full/V2Ray-Configs/refs/heads/main/Reza-Collection",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY_RAW.txt",
        "https://raw.githubusercontent.com/shabane/kamaji/master/hub/tested/ss.txt",
        "https://raw.githubusercontent.com/shabane/kamaji/master/hub/tested/vmess.txt",
        "https://raw.githubusercontent.com/shabane/kamaji/master/hub/tested/vless.txt",
        "https://raw.githubusercontent.com/shabane/kamaji/master/hub/tested/trojan.txt",
        "https://raw.githubusercontent.com/theGreatPeter/v2rayNodes/refs/heads/main/nodes.txt",
        "https://raw.githubusercontent.com/tristan-deng/v2rayNodesSelected/refs/heads/main/MyNodes.txt",
        "https://raw.githubusercontent.com/wudongdefeng/free/refs/heads/main/freevm/list_raw.txt",
        "https://ivuxy.tech/v.txt",
    ]

    decoded_links = decode_links(links)
    decoded_dir_links = decode_dir_links(dir_links)

    combined_data = decoded_links + decoded_dir_links
    merged_configs = filter_for_protocols(combined_data, protocols)

    # Clean existing output files
    output_filename = os.path.join(output_folder, "All_Configs_Sub.txt")
    filename1 = os.path.join(output_folder, "All_Configs_base64_Sub.txt")
    
    if os.path.exists(output_filename):
        os.remove(output_filename)
    if os.path.exists(filename1):
        os.remove(filename1)

    for i in range(20):
        filename = os.path.join(output_folder, f"Sub{i}.txt")
        if os.path.exists(filename):
            os.remove(filename)
        filename1 = os.path.join(base64_folder, f"Sub{i}_base64.txt")
        if os.path.exists(filename1):
            os.remove(filename1)

    # Write merged configs to output file
    with open(output_filename, "w") as f:
        f.write(fixed_text)
        for config in merged_configs:
            f.write(config + "\n")

    # Split merged configs into smaller files (no more than 600 configs per file)
    with open(output_filename, "r") as f:
        lines = f.readlines()

    num_lines = len(lines)
    max_lines_per_file = 600
    num_files = (num_lines + max_lines_per_file - 1) // max_lines_per_file

    for i in range(num_files):
        profile_title = f"🆓 Git:Barry-far | Sub{i+1} 🫂"
        encoded_title = base64.b64encode(profile_title.encode()).decode()
        custom_fixed_text = f"""#profile-title: base64:{encoded_title}
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/10ium/V2ray-Config
#profile-web-page-url: https://github.com/10ium/V2ray-Config
"""

        input_filename = os.path.join(output_folder, f"Sub{i + 1}.txt")
        with open(input_filename, "w") as f:
            f.write(custom_fixed_text)
            start_index = i * max_lines_per_file
            end_index = min((i + 1) * max_lines_per_file, num_lines)
            for line in lines[start_index:end_index]:
                f.write(line)

        with open(input_filename, "r") as input_file:
            config_data = input_file.read()
        
        output_filename = os.path.join(base64_folder, f"Sub{i + 1}_base64.txt")
        with open(output_filename, "w") as output_file:
            encoded_config = base64.b64encode(config_data.encode()).decode()
            output_file.write(encoded_config)

if __name__ == "__main__":
    main()
