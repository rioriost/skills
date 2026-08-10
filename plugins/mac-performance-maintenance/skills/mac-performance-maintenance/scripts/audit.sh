#!/bin/bash

# Read-only macOS performance and storage inventory.
# This script intentionally contains no delete, prune, stop, start, or config commands.

set -u

QUICK=0
TOP_N=15

usage() {
  printf '%s\n' "Usage: audit.sh [--quick] [--top N]"
  printf '%s\n' "  --quick  Skip the broad ~/Library size crawl."
  printf '%s\n' "  --top N  Show N entries in ranked lists (default: 15)."
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --quick)
      QUICK=1
      shift
      ;;
    --top)
      if [ "$#" -lt 2 ] || ! printf '%s' "$2" | grep -Eq '^[1-9][0-9]*$'; then
        printf '%s\n' "error: --top requires a positive integer" >&2
        exit 64
      fi
      TOP_N="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'error: unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 64
      ;;
  esac
done

section() {
  printf '\n## %s\n' "$1"
}

label() {
  printf '\n### %s\n' "$1"
}

note() {
  printf 'NOTE: %s\n' "$1"
}

have() {
  command -v "$1" >/dev/null 2>&1
}

run_readonly() {
  _label="$1"
  shift
  label "$_label"
  _output=$("$@" 2>&1)
  _status=$?
  if [ -n "$_output" ]; then
    printf '%s\n' "$_output"
  else
    printf '%s\n' "(no output)"
  fi
  if [ "$_status" -ne 0 ]; then
    printf '[unavailable: exit %s]\n' "$_status"
  fi
  return 0
}

run_with_timeout() {
  _timeout_seconds="$1"
  shift
  "$@" &
  _command_pid=$!
  (
    sleep "$_timeout_seconds"
    kill -TERM "$_command_pid" 2>/dev/null
  ) &
  _watcher_pid=$!
  wait "$_command_pid"
  _command_status=$?
  kill "$_watcher_pid" 2>/dev/null
  wait "$_watcher_pid" 2>/dev/null
  if [ "$_command_status" -eq 143 ]; then
    return 124
  fi
  return "$_command_status"
}

help_has_subcommand() {
  _help_text="$1"
  _subcommand="$2"
  printf '%s\n' "$_help_text" | grep -Eq "^[[:space:]]*${_subcommand}\\*?([,[:space:]]|$)"
}

humanize_kib() {
  awk '
    function human(kib) {
      if (kib >= 1073741824) return sprintf("%.1f TiB", kib / 1073741824)
      if (kib >= 1048576) return sprintf("%.1f GiB", kib / 1048576)
      if (kib >= 1024) return sprintf("%.1f MiB", kib / 1024)
      return sprintf("%d KiB", kib)
    }
    {
      kib=$1
      $1=""
      sub(/^[[:space:]]+/, "")
      printf "%10s  %s\n", human(kib), $0
    }
  '
}

show_paths() {
  _heading="$1"
  shift
  label "$_heading"
  _found=0
  for _path in "$@"; do
    if [ -e "$_path" ]; then
      _size=$(du -sk "$_path" 2>/dev/null)
      if [ -n "$_size" ]; then
        printf '%s\n' "$_size" | humanize_kib
      else
        printf '%10s  %s\n' "UNKNOWN" "$_path (not fully readable)"
      fi
      _found=1
    fi
  done
  if [ "$_found" -eq 0 ]; then
    printf '%s\n' "(none of the known paths exist)"
  fi
}

printf '%s\n' "# Mac Performance Maintenance Audit"
printf 'Generated: %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
printf '%s\n' "Mode: read-only; no deletion, pruning, service start/stop, or settings changes"

section "Platform"
if [ "$(uname -s 2>/dev/null)" != "Darwin" ]; then
  printf '%s\n' "Unsupported host: this audit targets macOS."
  exit 2
fi

run_readonly "macOS" sw_vers
_architecture=$(uname -m)
_arm64_capable=$(sysctl -n hw.optional.arm64 2>/dev/null || printf '0')
printf 'Architecture: %s\n' "$_architecture"
if [ "$_arm64_capable" != "1" ]; then
  printf '%s\n' "Unsupported hardware: this audit targets Apple Silicon Macs."
  exit 2
fi
printf 'Model identifier: %s\n' "$(sysctl -n hw.model 2>/dev/null || printf 'UNKNOWN')"
printf 'Logical CPUs: %s\n' "$(sysctl -n hw.logicalcpu 2>/dev/null || printf 'UNKNOWN')"
_memory_bytes=$(sysctl -n hw.memsize 2>/dev/null || printf '0')
if printf '%s' "$_memory_bytes" | grep -Eq '^[0-9]+$' && [ "$_memory_bytes" -gt 0 ]; then
  awk -v bytes="$_memory_bytes" 'BEGIN { printf "Physical memory: %.1f GiB\n", bytes / 1073741824 }'
else
  printf '%s\n' "Physical memory: UNKNOWN"
fi
printf 'Uptime/load: %s\n' "$(uptime 2>/dev/null || printf 'UNKNOWN')"

section "Storage"
run_readonly "Mounted volumes" df -h / /System/Volumes/Data
note "APFS purgeable space and snapshots can make directory totals differ from immediately reclaimable space."

section "Memory and CPU"
if have memory_pressure; then
  run_readonly "Current memory pressure" memory_pressure -Q
else
  label "Current memory pressure"
  printf '%s\n' "UNKNOWN (memory_pressure not found)"
fi
run_readonly "Swap" sysctl vm.swapusage
run_readonly "Virtual memory counters" vm_stat
label "Top processes by CPU"
ps -Ao pid,%cpu,%mem,etime,comm -r 2>&1 | head -n "$((TOP_N + 1))"
note "This is a point-in-time sample. Re-sample before attributing sustained load."

section "Login and background items"
if have sfltool; then
  label "Background task management records (summary)"
  run_with_timeout 15 sfltool dumpbtm 2>&1 | awk -v max_records="$TOP_N" '
    function emit() {
      if (record == "") return
      total++
      if (total <= max_records) {
        printf "%s | Name: %s | Type: %s | Disposition: %s | Identifier: %s\n", record, name, type, disposition, identifier
      }
    }
    /^ #[0-9]+:/ {
      emit()
      record=$1
      name="UNKNOWN"; type="UNKNOWN"; disposition="UNKNOWN"; identifier="UNKNOWN"
      next
    }
    /^[[:space:]]+Name:/ { sub(/^[^:]+:[[:space:]]*/, ""); name=$0; next }
    /^[[:space:]]+Type:/ { sub(/^[^:]+:[[:space:]]*/, ""); type=$0; next }
    /^[[:space:]]+Disposition:/ { sub(/^[^:]+:[[:space:]]*/, ""); disposition=$0; next }
    /^[[:space:]]+Identifier:/ { sub(/^[^:]+:[[:space:]]*/, ""); identifier=$0; next }
    END {
      emit()
      if (total == 0) print "(no records parsed)"
      else if (total > max_records) printf "... %d additional records omitted; rerun with --top %d or inspect sfltool dumpbtm locally.\n", total - max_records, total
      printf "Parsed records: %d\n", total
    }
  '
  _sfltool_status=${PIPESTATUS[0]}
  if [ "$_sfltool_status" -eq 124 ]; then
    note "sfltool dumpbtm exceeded 15 seconds; partial records are shown."
  elif [ "$_sfltool_status" -ne 0 ]; then
    note "sfltool dumpbtm was unavailable (exit $_sfltool_status)."
  fi
else
  label "Background task management records (summary)"
  printf '%s\n' "UNKNOWN (sfltool not found)"
fi

for _launch_dir in \
  "$HOME/Library/LaunchAgents" \
  "/Library/LaunchAgents" \
  "/Library/LaunchDaemons"
do
  label "$_launch_dir"
  if [ -d "$_launch_dir" ]; then
    _launch_count=$(find "$_launch_dir" -maxdepth 1 -type f -name '*.plist' 2>/dev/null | wc -l | tr -d ' ')
    printf 'Count: %s\n' "$_launch_count"
    find "$_launch_dir" -maxdepth 1 -type f -name '*.plist' -print 2>/dev/null | sort | head -n "$TOP_N"
    if [ "$_launch_count" -gt "$TOP_N" ]; then
      printf '... %s additional plist files omitted.\n' "$((_launch_count - TOP_N))"
    fi
  else
    printf '%s\n' "(directory not present)"
  fi
done
note "System-provided /System/Library launch items are excluded from this user-maintenance inventory."

section "Time Machine"
if have tmutil; then
  run_readonly "Local snapshots for /" tmutil listlocalsnapshots /
else
  label "Local snapshots for /"
  printf '%s\n' "UNKNOWN (tmutil not found)"
fi
note "The audit does not thin or delete snapshots."

section "Xcode and Apple developer data"
if have xcode-select; then
  run_readonly "Active developer directory" xcode-select -p
fi
note "Directory totals can double-count APFS clones or sparse data and are not guaranteed reclaimable bytes."
show_paths "Focused developer directory sizes" \
  "$HOME/Library/Developer/Xcode/DerivedData" \
  "$HOME/Library/Developer/Xcode/Archives" \
  "$HOME/Library/Developer/Xcode/iOS DeviceSupport" \
  "$HOME/Library/Developer/CoreSimulator" \
  "$HOME/Library/Developer/XCTestDevices" \
  "/Library/Developer/CoreSimulator/Profiles/Runtimes"

label "Installed Simulator runtime bundles"
_runtime_count=0
for _runtime_root in \
  "$HOME/Library/Developer/CoreSimulator/Profiles/Runtimes" \
  "/Library/Developer/CoreSimulator/Profiles/Runtimes"
do
  if [ -d "$_runtime_root" ]; then
    find "$_runtime_root" -maxdepth 1 -type d -name '*.simruntime' -print 2>/dev/null
    _runtime_count=$((_runtime_count + $(find "$_runtime_root" -maxdepth 1 -type d -name '*.simruntime' 2>/dev/null | wc -l | tr -d ' ')))
  fi
done
if [ "$_runtime_count" -eq 0 ]; then
  printf '%s\n' "(no runtime bundles found in known paths)"
fi

label "Mounted or staged Simulator runtime volumes"
if [ -d "/Library/Developer/CoreSimulator/Volumes" ]; then
  _runtime_volume_count=$(find /Library/Developer/CoreSimulator/Volumes -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
  find /Library/Developer/CoreSimulator/Volumes -mindepth 1 -maxdepth 1 -type d -print 2>/dev/null | sort | head -n "$TOP_N"
  if [ "$_runtime_volume_count" -eq 0 ]; then
    printf '%s\n' "(no runtime volumes found)"
  elif [ "$_runtime_volume_count" -gt "$TOP_N" ]; then
    printf '... %s additional runtime volumes omitted.\n' "$((_runtime_volume_count - TOP_N))"
  fi
else
  printf '%s\n' "(runtime volume directory not present)"
fi

section "Homebrew"
if have brew; then
  run_readonly "Homebrew version" brew --version
  printf 'Prefix: %s\n' "$(brew --prefix 2>/dev/null || printf 'UNKNOWN')"
  printf 'Installed formulae: %s\n' "$(brew list --formula 2>/dev/null | wc -l | tr -d ' ')"
  printf 'Installed casks: %s\n' "$(brew list --cask 2>/dev/null | wc -l | tr -d ' ')"
  _brew_cleanup_help=$(brew cleanup --help 2>&1)
  if printf '%s\n' "$_brew_cleanup_help" | grep -Eq -- '(^|[[:space:]])-n,?[[:space:]]+--dry-run|--dry-run'; then
    run_readonly "Homebrew cleanup preview" env HOMEBREW_NO_AUTO_UPDATE=1 brew cleanup --dry-run
  else
    label "Homebrew cleanup preview"
    printf '%s\n' "UNKNOWN (installed brew help does not advertise --dry-run)"
  fi
else
  printf '%s\n' "Homebrew: not installed"
fi

section "Container runtimes"
if have docker; then
  run_readonly "Docker version" docker --version
  _docker_help=$(docker --help 2>&1)
  if help_has_subcommand "$_docker_help" "desktop"; then
    _docker_desktop_help=$(docker desktop --help 2>&1)
    if help_has_subcommand "$_docker_desktop_help" "status"; then
      run_readonly "Docker Desktop status" docker desktop status
    fi
  fi
  if help_has_subcommand "$_docker_help" "context"; then
    _docker_context_help=$(docker context --help 2>&1)
    if help_has_subcommand "$_docker_context_help" "list" || help_has_subcommand "$_docker_context_help" "ls"; then
      run_readonly "Docker contexts" docker context ls
    fi
  fi
  if help_has_subcommand "$_docker_help" "system"; then
    _docker_system_help=$(docker system --help 2>&1)
    if help_has_subcommand "$_docker_system_help" "df"; then
      run_readonly "Docker disk usage" docker system df
    fi
  fi
  if help_has_subcommand "$_docker_help" "container"; then
    run_readonly "Docker containers" docker container ls --all --size
  fi
else
  printf '%s\n' "Docker CLI: not installed"
fi

if have podman; then
  run_readonly "Podman version" podman --version
  _podman_help=$(podman --help 2>&1)
  if help_has_subcommand "$_podman_help" "machine"; then
    _podman_machine_help=$(podman machine --help 2>&1)
    if help_has_subcommand "$_podman_machine_help" "list"; then
      run_readonly "Podman machines" podman machine list
    fi
  fi
  if help_has_subcommand "$_podman_help" "system"; then
    _podman_system_help=$(podman system --help 2>&1)
    if help_has_subcommand "$_podman_system_help" "connection"; then
      _podman_connection_help=$(podman system connection --help 2>&1)
      if help_has_subcommand "$_podman_connection_help" "list"; then
        run_readonly "Podman connections" podman system connection list
      fi
    fi
    if help_has_subcommand "$_podman_system_help" "df"; then
      run_readonly "Podman disk usage" podman system df
    fi
  fi
  if help_has_subcommand "$_podman_help" "container"; then
    run_readonly "Podman containers" podman container ls --all --size
  fi
else
  printf '%s\n' "Podman CLI: not installed"
fi

if have container; then
  run_readonly "Apple Container version" container --version
  _container_help=$(container --help 2>&1)

  if help_has_subcommand "$_container_help" "system"; then
    _container_system_help=$(container system --help 2>&1)
    if help_has_subcommand "$_container_system_help" "status"; then
      run_readonly "Apple Container service status" container system status
    fi
    if help_has_subcommand "$_container_system_help" "df"; then
      run_readonly "Apple Container disk usage" container system df
    fi
  fi

  if help_has_subcommand "$_container_help" "list"; then
    _container_list_help=$(container list --help 2>&1)
    if printf '%s\n' "$_container_list_help" | grep -Eq -- '(^|[[:space:]])-a,?[[:space:]]+--all|--all'; then
      run_readonly "Apple containers" container list --all
    else
      run_readonly "Running Apple containers" container list
    fi
  fi

  if help_has_subcommand "$_container_help" "image"; then
    _container_image_help=$(container image --help 2>&1)
    if help_has_subcommand "$_container_image_help" "list"; then
      run_readonly "Apple Container images" container image list
    fi
  fi

  if help_has_subcommand "$_container_help" "volume"; then
    _container_volume_help=$(container volume --help 2>&1)
    if help_has_subcommand "$_container_volume_help" "list"; then
      run_readonly "Apple Container volumes" container volume list
    fi
  fi

  if help_has_subcommand "$_container_help" "machine"; then
    _container_machine_help=$(container machine --help 2>&1)
    if help_has_subcommand "$_container_machine_help" "list"; then
      run_readonly "Apple container machines" container machine list
    fi
  fi

  if help_has_subcommand "$_container_help" "network"; then
    _container_network_help=$(container network --help 2>&1)
    if help_has_subcommand "$_container_network_help" "list"; then
      run_readonly "Apple Container networks" container network list
    fi
  fi

  if help_has_subcommand "$_container_help" "builder"; then
    _container_builder_help=$(container builder --help 2>&1)
    if help_has_subcommand "$_container_builder_help" "status"; then
      run_readonly "Apple Container builder status" container builder status
    fi
  fi
else
  printf '%s\n' "Apple Container CLI: not installed"
fi

show_paths "Focused container storage paths" \
  "$HOME/Library/Containers/com.docker.docker" \
  "$HOME/Library/Group Containers/group.com.docker" \
  "$HOME/.docker" \
  "$HOME/.local/share/containers" \
  "$HOME/.colima" \
  "$HOME/.lima" \
  "$HOME/Library/Application Support/com.apple.container"

section "Virtual machines"
if have prlctl; then
  run_readonly "Parallels version" prlctl --version
  run_readonly "Parallels VM inventory" prlctl list --all
else
  printf '%s\n' "Parallels CLI: not installed"
fi

if have utmctl; then
  _utm_help=$(utmctl --help 2>&1)
  if help_has_subcommand "$_utm_help" "version"; then
    run_readonly "UTM version" utmctl version
  fi
  if help_has_subcommand "$_utm_help" "list"; then
    run_readonly "UTM VM inventory" utmctl list
  else
    label "UTM VM inventory"
    printf '%s\n' "UNKNOWN (installed utmctl help does not advertise list)"
  fi
else
  printf '%s\n' "UTM CLI: not installed"
fi

if have limactl; then
  run_readonly "Lima VM inventory" limactl list
fi
if have colima; then
  run_readonly "Colima status" colima status
fi
if have VBoxManage; then
  run_readonly "VirtualBox VM inventory" VBoxManage list vms
fi

show_paths "Focused VM storage paths" \
  "$HOME/Parallels" \
  "$HOME/Documents/Parallels" \
  "$HOME/Library/Parallels" \
  "$HOME/Library/Containers/com.utmapp.UTM/Data/Documents" \
  "$HOME/Library/Group Containers/WDNLXAD4W8.com.utmapp.UTM"

section "Large Library directories"
if [ "$QUICK" -eq 1 ]; then
  printf '%s\n' "Skipped in --quick mode."
else
  note "This crawl can take time. Inaccessible directories are omitted rather than treated as zero."
  du -sk "$HOME/Library"/* 2>/dev/null | sort -nr | head -n "$TOP_N" | humanize_kib
fi

section "Battery"
_battery_output=$(pmset -g batt 2>&1)
if printf '%s\n' "$_battery_output" | grep -q 'InternalBattery'; then
  printf '%s\n' "$_battery_output"
  if have system_profiler; then
    system_profiler SPPowerDataType -detailLevel mini 2>&1 | awk '
      /Charge Information:|Health Information:|Cycle Count:|Condition:|Maximum Capacity:|State of Charge|Full Charge Capacity|Design Capacity|Battery Installed:/ { print }
    '
  fi
else
  printf '%s\n' "Not applicable: no internal battery reported (desktop Mac or unavailable data)."
fi

section "Audit limitations"
printf '%s\n' "- No cleanup action was performed."
printf '%s\n' "- Inactive runtimes were not started for inspection."
printf '%s\n' "- Privacy protections may omit directories and background-item details."
printf '%s\n' "- Process load and memory pressure are point-in-time observations."
printf '%s\n' "- Review paths, process names, VM names, and background items before sharing this output."
