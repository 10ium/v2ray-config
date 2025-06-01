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
    for item in data: # Changed from 'line' to 'item' to avoid confusion with lines in a file
        for line in item.splitlines(): # Process each line if item is a multi-line string
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

    # Define the new folder for count-based split files
    count_split_folder_name = "Count_Splitted_Configs"
    count_split_path = os.path.join(output_folder, count_split_folder_name)

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
    # Ensure merged_configs contains only strings, not lists of strings
    merged_configs_lines = []
    for item in combined_data:
        merged_configs_lines.extend(item.splitlines())
    
    merged_configs = filter_for_protocols(merged_configs_lines, protocols)


    # Clean existing output files
    all_configs_sub_path = os.path.join(output_folder, "All_Configs_Sub.txt")
    # Assuming All_Configs_base64_Sub.txt is intentionally in the root, as per original script structure
    all_configs_base64_output_path = os.path.join(output_folder, "All_Configs_base64_Sub.txt")
    
    if os.path.exists(all_configs_sub_path):
        os.remove(all_configs_sub_path)
    if os.path.exists(all_configs_base64_output_path): # Path used for main base64 file
        os.remove(all_configs_base64_output_path)

    # Clean SubX.txt files from the new count_split_path folder
    # The original loop cleaned Sub0.txt to Sub19.txt. We replicate this for the new location.
    # Files are generated as Sub1.txt, Sub2.txt, etc.
    if os.path.exists(count_split_path):
        for i in range(20): # Cleans Sub0.txt .. Sub19.txt if they exist in count_split_path
            filename_to_clean = os.path.join(count_split_path, f"Sub{i}.txt")
            if os.path.exists(filename_to_clean):
                os.remove(filename_to_clean)
    
    # Clean SubX_base64.txt files from base64_folder (this part is unchanged as per request)
    if os.path.exists(base64_folder):
        for i in range(20): # Cleans Sub0_base64.txt .. Sub19_base64.txt if they exist
            base64_file_to_clean = os.path.join(base64_folder, f"Sub{i}_base64.txt")
            if os.path.exists(base64_file_to_clean):
                os.remove(base64_file_to_clean)

    # Write merged configs to output file (All_Configs_Sub.txt in root)
    with open(all_configs_sub_path, "w") as f:
        f.write(fixed_text)
        unique_configs = sorted(list(set(merged_configs))) # Remove duplicates and sort
        for config in unique_configs:
            f.write(config + "\n")

    # Split merged configs into smaller files (no more than 600 configs per file)
    with open(all_configs_sub_path, "r") as f:
        lines = f.readlines() # lines already includes fixed_text as first few lines

    # Exclude fixed_text lines from being counted towards max_lines_per_file if they are part of 'lines'
    # and not part of the actual configs.
    # However, the original script includes fixed_text in the count for splitting.
    # The current `lines` variable will include the `fixed_text` if it was written to All_Configs_Sub.txt
    # and then read back. The split files also get a custom_fixed_text.

    num_config_lines = len(lines) # This includes the initial fixed_text lines from All_Configs_Sub.txt
    max_lines_per_file = 600
    num_files = (num_config_lines + max_lines_per_file - 1) // max_lines_per_file

    # Ensure the new directory for count-split files exists
    os.makedirs(count_split_path, exist_ok=True)

    for i in range(num_files): # i from 0 to num_files-1
        profile_title = f"🆓 Git:Barry-far | Sub{i+1} 🫂"
        encoded_title = base64.b64encode(profile_title.encode()).decode()
        custom_fixed_text_for_split_files = f"""#profile-title: base64:{encoded_title}
#profile-update-interval: 1
#subscription-userinfo: upload=29; download=12; total=10737418240000000; expire=2546249531
#support-url: https://github.com/10ium/V2ray-Config
#profile-web-page-url: https://github.com/10ium/V2ray-Config
"""
        # Path for the split file (e.g., Sub1.txt) now goes into count_split_path
        split_file_path = os.path.join(count_split_path, f"Sub{i + 1}.txt")
        with open(split_file_path, "w") as f:
            f.write(custom_fixed_text_for_split_files) # Write header for this specific split file
            start_index = i * max_lines_per_file
            end_index = min((i + 1) * max_lines_per_file, num_config_lines)
            
            # Logic to handle writing lines:
            # If start_index is 0, we are in the first file (Sub1.txt).
            # The 'lines' variable contains everything from All_Configs_Sub.txt including its header.
            # The custom_fixed_text_for_split_files is already written.
            # We should write the config lines from 'lines' starting after its header,
            # or adjust 'max_lines_per_file' to account for the new header in each split file.

            # Simpler approach: write the segment of lines directly.
            # Each split file gets its own header, then a chunk of lines from the main aggregated file.
            for line_content in lines[start_index:end_index]:
                f.write(line_content)

        # Base64 encoding part for the split file
        # Reads from split_file_path (which is now in count_split_path/SubX.txt)
        # Writes to base64_folder/SubX_base64.txt (this behavior is unchanged as per request)
        with open(split_file_path, "r") as input_file:
            config_data_for_base64 = input_file.read()
        
        base64_output_for_split_file = os.path.join(base64_folder, f"Sub{i + 1}_base64.txt")
        with open(base64_output_for_split_file, "w") as output_file:
            encoded_config = base64.b64encode(config_data_for_base64.encode()).decode()
            output_file.write(encoded_config)

if __name__ == "__main__":
    main()
