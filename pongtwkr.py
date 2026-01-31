#!/usr/bin/env python3
# Main. v0.8-PRE.
# Author: valter-byte
# License: GPL-3.0

import sys
import os
if os.getuid() != 0:
    print("❌ PongTWKR requires root privileges.")
    print("   Run with: sudo pongtwkr <command>")
    sys.exit(1)
try:
    import psutil
except ImportError:
    print("❌ Error: PongTWKR requires psutil.")
    print("   Install: sudo pip install psutil --break-system-packages")
    sys.exit(1)
infos = { 
    "swappiness": "Swappiness is how sensible is the system to switching to SWAP instead of RAM. Safe range: 0-100.",
    "dirtyratio": "Dirty Ratio defines the maximum percentage of dirty memory before writing onto the disk. Safe range: 20-70%",
    "dirtybackground": "Same as dirty ratio, but writing onto the background instead of the disk. IT SHOULD ALWAYS BE LOWER THAN DIRTY RATIO. Safe range: 5-50",
    "cachepressure": "Controls the pressure over the cache (duh), safe values: 0-100",
    "governor": "Governors are presets that the CPU comes with. If you want performance, use sudo pongtwkr governor performance, if you want power saving, use powersave.",
    "cpumin": "Defines the minimum frequency for the CPU",
    "cpumax": "Defines the maximum frequency for the CPU.",
    "info": "Shows a quick set of info and tweaks made.",
    "ping": "Well... just pings google to see your ms.. what did you expect???",
    "thp": """Transparent HugePages (THP) is a kernel feature that allows the system to use larger memory pages, 
improving performance for applications that use large amounts of memory.""",
    "hugepages": """HugePages is a memory management feature that allows the allocation of large memory pages, "
which can improve performance for certain applications by reducing overhead and increasing TLB efficiency.""",
    "cputurbo": """Enables or disables CPU Turbo Boost (Intel) or Precision Boost (AMD),
which allows the CPU to run at higher frequencies under certain conditions for improved performance.""",
    "smt": "Simultaneous Multi-Threading (SMT) allows multiple threads to run on each CPU core, improving parallelism and performance in multi-threaded applications.",
    "offload": "Network offloading features (like GRO, LRO, TSO, GSO) help reduce CPU load by offloading certain network processing tasks to the network interface card (NIC).",
    "tcpmetrics": "TCP metrics saving allows the kernel to save and reuse TCP connection metrics, improving performance for frequently used connections.",
    "wifipower": "Wifi power management allows the system to save power by reducing the power consumption of wifi interfaces when not in use.",
    "mtuprobing": "MTU probing helps optimize network performance by dynamically adjusting the Maximum Transmission Unit (MTU) size based on network conditions.",
    "rmem": "Sets the maximum receive buffer size for network sockets, which can improve network performance for high-throughput applications.",
    "wmem": "Sets the maximum send buffer size for network sockets, which can improve network performance for high-throughput applications.",
    "numa": "NUMA Balancing allows the kernel to automatically manage memory allocation across NUMA nodes, improving performance for applications that use large amounts of memory on NUMA systems.",
    "zswappools": "Sets the maximum pool percentage for ZSWAP, which is a compressed cache for swap pages in RAM, improving performance for systems that use swap memory.",
    "zswapalgo": "Sets the compression algorithm for ZSWAP, which is a compressed cache for swap pages in RAM, improving performance for systems that use swap memory.",
    "zswapenabled": "Enables or disables ZSWAP, which is a compressed cache for swap pages in RAM, improving performance for systems that use swap memory.",
    "zramstreams": "Sets the number of compression streams for ZRAM, which is a compressed block device in RAM used for swap memory, improving performance for systems that use swap memory.",
    "zramsize": "Sets the size of the ZRAM block device, which is a compressed block device in RAM used for swap memory, improving performance for systems that use swap memory.",
    "zramalgo": "Sets the compression algorithm for ZRAM, which is a compressed block device in RAM used for swap memory, improving performance for systems that use swap memory."

}
from modules import logger, profiles, persistence, utils, net, cpu, ram
def show_param_info(param):
    print(infos.get(param, "Ups, theres no info for this..."))
    if param in ("dirtyratio", "dirtybackground", "cachepressure"):
        print("⚠️ Security: values out of range may cause instablity and kernel errors.")
    if param in ("cpumin", "cpumax"):
        print("⚠️ Beware: The CPU automatically tops itself. No matter if you do override, the values will be topped to the physical limits of your CPU")
    if param == "governor":
        print("⚠️ Beware: Some governors may not be available for all systems.")
    if param == "thp":
        print("⚠️ Note: Setting THP to 'always' may lead to performance degradation in some workloads.")
    if param == "hugepages":
        print("⚠️ Note: Setting a high number of HugePages may lead to memory allocation issues for other applications.")
    if param == "smt":
        print("⚠️ SMT Multithreading may not be available on all systems.")
def main():
    """Main entry point"""
    logger.ensure_log_dir()
    logger.save_original_defaults()
    if len(sys.argv) < 2:
        print("⚠️ Usage: sudo pongtwkr <command>")
        print("   Commands: info, save, load, persist")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    override = "override" in sys.argv
    action = sys.argv[2].lower() if len(sys.argv) >= 3 else None # <--- almost killed myself trying to find this bug lol
  
    if action == "info":    
        show_param_info(command)
        sys.exit(0)
    elif command == "save":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr save <name>")
        elif sys.argv[2] in ["persistent_settings", "original_defaults"]:
            print("❌ That name is reserved.")
        else:
            profiles.save_profile(sys.argv[2])
    elif command == "zramstreams":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr zramstreams <value>")
        elif override:
            from modules.ram import set_zramstreams
            val = int(sys.argv[2])
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_zramstreams(val)
        else:
            from modules.utils import limit_value
            from modules.ram import set_zramstreams
            threads = psutil.cpu(logical=True)
            val = limit_value("ZRAM Streams", sys.argv[2], 0, threads)
            set_zramstreams(val)
    elif command == "zramalgo":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr zramalgo <value>")
        else:
            from modules.ram import set_zramalgo
            val = sys.argv[2]
            set_zramalgo(val)
    elif command == "zramsize":
        if override:
            from modules.ram import set_zramsize
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_zramsize(sys.argv[2])
        else:
            from modules.utils import parse_size_2, limit_value
            from modules.ram import set_zramsize
            val = parse_size_2(sys.argv[2])
            if val is not None:
                max_safe = psutil.virtual_memory().total * 2
                val = limit_value("zram_size", val, 0, max_safe) 
                if val is not None:
                    print(f"Proceeding with ZRAM Resize, please, wait, this may take up to 2 minutes... you may experience device freeze, do not interrupt.")
                    set_zramsize(val)

    elif command == "zswappool":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr zswappool <value>")
        elif override:
            from modules.ram import set_zswap_pool
            val = sys.argv[2]
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_zswap_pool(val)
        else:
            from modules.utils import limit_value
            from modules.ram import set_zswap_pool
            val = limit_value("Zswap Pool Percent", sys.argv[2], 1, 40)
            set_zswap_pool(val)
    elif command == "zswapalgo":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr zswapalgo <value>")
        else:
            from modules.ram import set_zswap_algo
            val = sys.argv[2]
            set_zswap_algo(val)
    elif command == "zswap":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr zswap <value>")
        else:
            from modules.ram import set_zswap_enabled
            val = sys.argv[2]
            set_zswap_enabled(val)
    elif command == "offload":
        if len(sys.argv) < 4:
            print("⚠️ Usage: sudo pongtwkr offload <type> <value>")
        else:
            offload_type = sys.argv[2].lower()
            offload_value = sys.argv[3]
            if offload_type == "gro":
                net.set_offload(offload_type, offload_value)
            elif offload_type == "tso":
                net.set_offload(offload_type, offload_value)
            elif offload_type == "gso":
                net.set_offload(offload_type, offload_value)
            else:
                print(f"⚠️ Unknown offload type: {offload_type}")
    elif command == "wmem":
        if override:
            from modules.net import set_wmem
            from modules.utils import parse_size
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_wmem(sys.argv[2])
        else:
            from modules.utils import parse_size, limit_value
            from modules.net import set_wmem
            val = parse_size(sys.argv[2])
            if val is not None:
                val = limit_value("wmem_max", val, 65536, 16777216)
                if val is not None:
                    set_wmem(val)
    elif command == "rmem":
        if override:
            from modules.net import set_rmem
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_rmem(sys.argv[2])
        else:
            from modules.utils import parse_size, limit_value
            from modules.net import set_rmem
            val = parse_size(sys.argv[2])
            if val is not None:
                val = limit_value("rmem_max", val, 65536, 16777216)
                if val is not None:
                    set_rmem(val)
    elif command == "mtuprobing":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr mtuprobing <value>")
        else:
            val = sys.argv[2]
            net.set_mtu_probing(val)
    elif command == "tcpmetrics":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr tcpmetrics <value>")
        else:
            val = sys.argv[2]
            net.set_tcp_metrics(val)
    elif command == "wifipower":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr wifipower <value>")
        else:
            val = sys.argv[2]
            net.set_wifi_power(val)
    elif command == "smt":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr smt <value>")
        else:
            from modules.cpu import set_smt
            val = sys.argv[2]
            set_smt(val)
    elif command == "cputurbo":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr cputurbo <value>")
        else:
            from modules.cpu import set_cputurbo
            val = sys.argv[2]
            set_cputurbo(val)
    elif command == "cpumin":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr cpumin <value>")
        else:
            from modules.cpu import set_cpu_min_freq
            val = sys.argv[2]
            set_cpu_min_freq(val)
    elif command == "cpumax":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr cpumax <value>")
    
        else:
            from modules.cpu import set_cpu_max_freq
            from modules.utils import limit_float
            val = limit_float("CPU Max Frequency (GHz)", sys.argv[2], 0.5, 6.0)
            set_cpu_max_freq(val)
        
    elif command == "load":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr load <name>")
        else:
            profiles.load_profile(sys.argv[2])
        
    elif command == "governor":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr governor <value>")
        else:
            from modules.cpu import set_governor
            val = sys.argv[2]
            set_governor(val)
    elif command == "thp":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr thp <value>")
        else:
            from modules.ram import set_thp
            val = sys.argv[2]
            set_thp(val)
    elif command == "numa":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr numa <value>")
        else:
            from modules.ram import set_numa_balancing
            val = sys.argv[2]
            if val.lower() not in ("true", "false"):
                print("⚠️ Error: numa only accepts 'true' or 'false'.")
            else:
                val = sys.argv[2]
                set_numa_balancing(val)
    elif command == "hugepages":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr hugepages <value>")
        elif override:
            from modules.ram import set_hugepages
            val = int(sys.argv[2])
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_hugepages(val)
        else:
            from modules.utils import limit_value
            from modules.ram import set_hugepages
            val = limit_value("Hugepages", sys.argv[2], 0, 2048)
            set_hugepages(val)
    elif command == "cachepressure":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr cachepressure <value>")
        elif override:
            from modules.ram import set_cache_pressure
            val = int(sys.argv[2])
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_cache_pressure(val)
        else:
            from modules.utils import limit_value
            from modules.ram import set_cache_pressure
            val = limit_value("Cache Pressure", sys.argv[2], 0, 500)
            set_cache_pressure(val)
    elif command == "dirtybackground":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr dirtybackground <value>")
        elif override:
            from modules.ram import set_dirty_background_ratio
            val = int(sys.argv[2])
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_dirty_background_ratio(val)
        else:
            from modules.utils import limit_value
            from modules.ram import set_dirty_background_ratio
            val = limit_value("Dirty Background Ratio", sys.argv[2], 0, 50)
            set_dirty_background_ratio(val)
    elif command == "dirtyratio":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr dirtyratio <value>")
        elif override:
            from modules.ram import set_dirty_ratio
            val = int(sys.argv[2])
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_dirty_ratio(val)
        else:
            from modules.utils import limit_value
            from modules.ram import set_dirty_ratio
            val = limit_value("Dirty Ratio", sys.argv[2], 0, 70)
            set_dirty_ratio(val)
    elif command == "persist":
        persistence.enable_persistence()
    elif command == "swappiness":
        if len(sys.argv) < 3:
            print("⚠️ Usage: sudo pongtwkr swappiness <value>")
        elif override:
            from modules.ram import set_swappiness
            val = int(sys.argv[2])
            if not sys.argv[2].isdigit():
                print("❌ Error: Value must be a number.")
                sys.exit(1)
            set_swappiness(val)
        else:
            from modules.utils import limit_value
            from modules.ram import set_swappiness
            val = limit_value("Swappiness", sys.argv[2], 0, 100)
            set_swappiness(val)
    elif command == "info":
        from modules.utils import show_info
        show_info()
    elif command == "safe":
        from modules.utils import safe_profile
        safe_profile()
    elif command == "reset":
        from modules.utils import reset_defaults
        reset_defaults()
    else:
        print(f"⚠️ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Cancelled")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
