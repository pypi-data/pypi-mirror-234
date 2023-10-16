######################################
#  DEFAULT es7s configuration file   #
#  DO NOT EDIT                       #
#  Run 'es7s config edit' to set up  #
######################################

[general]
syntax-version = 2.9
theme-color = blue
user-repos-path = ""


###  Data providers [es7s/d]  ###

[provider]
battery = on
cpu = on
disk-usage = on
disk-io = on
datetime = on
docker = on
fan = on
memory = on
network-country = on
network-latency = on
network-usage = on
shocks = on
systemctl = on
temperature = on
timestamp = on
weather = on

[provider.network-latency]
host = 1.1.1.1
port = 53

[provider.network-usage]
; uses first available from the list as primary
net-interface =
    vpn0
    tun0
    lo
# @TODO
# exclude-net-interfaces = ^(veth|br-|docker).+$

[provider.shocks]
check-url = http://1.1.1.1

[provider.shocks.default]
proxy-protocol = socks5
proxy-host = localhost
proxy-port = 1080

[provider.shocks.stonks]
proxy-protocol = socks5
proxy-host = localhost
proxy-port = 9150

[provider.shocks.relay]
proxy-listening = true
proxy-protocol = socks5
proxy-host = localhost
proxy-port = 22

;[provider.shocks.*]
;check-url = <url>
;proxy-listening = true|false
;proxy-protocol = socks5|socks5h
;proxy-host = localhost
;proxy-port = 1080

[provider.timestamp]
url = https://dlup.link/temp/nalog.mtime

[provider.weather]
location = MSK


###  Monitors [tmux]  ###

[monitor]
debug = off
force-cache = off

[monitor.combined]
layout1 =
    es7s.cli.monitor.SystemCtlMonitor

    es7s.cli.monitor.SPACE
    es7s.cli.monitor.DiskUsageMonitor
    es7s.cli.monitor.MemoryMonitor
    es7s.cli.monitor.CpuLoadMonitor

    es7s.cli.monitor.EDGE_LEFT
    es7s.cli.monitor.SPACE
    es7s.cli.monitor.TemperatureMonitor
    es7s.cli.monitor.SPACE
    es7s.cli.monitor.DockerMonitor

    es7s.cli.monitor.SPACE
    es7s.cli.monitor.NetworkLatencyMonitor
    es7s.cli.monitor.SPACE
    es7s.cli.monitor.NetworkCountryMonitor
    es7s.cli.monitor.SPACE_2
    es7s.cli.monitor.ShocksMonitor
    es7s.cli.monitor.SPACE
    es7s.cli.monitor.TimestampMonitor
    es7s.cli.monitor.SPACE
    es7s.cli.monitor.WeatherMonitor

    es7s.cli.monitor.SPACE_2
    es7s.cli.monitor.DatetimeMonitor
    es7s.cli.monitor.SPACE_2
    es7s.cli.monitor.BatteryMonitor

layout2 =
    es7s.cli.monitor.EDGE_LEFT
    es7s.cli.monitor.CpuFreqMonitor
    es7s.cli.monitor.SPACE_2
    es7s.cli.monitor.CpuLoadAvgMonitor
    es7s.cli.monitor.SPACE
    es7s.cli.monitor.FanSpeedMonitor

[monitor.datetime]
display-year = off
display-seconds = off

[monitor.memory]
swap-warn-threshold = 0.70

[monitor.weather]
weather-icon-set-id = 0
weather-icon-max-width = 2
wind-speed-warn-threshold = 10.0


###  Indicators [gtk]  ###

[indicator]
debug = off
icon-demo = off
layout =
    es7s.gtk.IndicatorDocker
    es7s.gtk.IndicatorTimestamp
    es7s.gtk.IndicatorDisk
    es7s.gtk.IndicatorMemory
    es7s.gtk.IndicatorCpuLoad
    es7s.gtk.IndicatorTemperature
    es7s.gtk.IndicatorFanSpeed
    es7s.gtk.IndicatorNetworkUsage
    es7s.gtk.IndicatorShocks
# single =

[indicator.manager]
display = on
label-system-time = off
label-self-uptime = off
label-tick-nums = off
restart-timeout-min = 120

[indicator.docker]
display = on

[indicator.disk]
; label-io = off|read|write|both|sum
display = on
label-used = off
label-free = off
label-io = off
label-busy = off
used-warn-level-ratio = 0.90
busy-warn-level-ratio = 0.00

[indicator.fan]
display = on
label-rpm = off
value-min = 2000
value-max = 5000

[indicator.memory]
; label-physical-bytes = off|dynamic|short
display = on
label-physical-percents = off
label-physical-bytes = off
label-swap-percents = off
label-swap-bytes = off
physical-warn-threshold = 0.90
swap-warn-threshold = 0.70

[indicator.cpu-load]
; label-average = off|one|three
display = on
label-current = off
label-average = off

[indicator.timestamp]
display = on
label-value = off

[indicator.temperature]
; label = off|one|three
display = on
label = off

[indicator.network]
display = on
label-rate = off
label-latency = off
label-country = off
exclude-foreign-codes = 
    ru
    kz

[indicator.shocks]
display = on
label = off
latency-warn-threshold-ms = 1000


###  CLI :: Executables  ###

[cli]
debug-io = off

[exec.autoterm]
default-filter = xbind
input-timeout-sec = 0.5
render-interval-sec = 1.0
proc-read-interval-sec = 1.0
proc-kill-interval-sec = 0.25

[exec.edit-image]
editor-raster = gimp
editor-vector = inkscape
ext-vector =
    svg

[exec.switch-wspace]
; indexes =
;    0
;    1
; filter = off|whitelist|blacklist
; selector = first|cycle
indexes =
filter = off
selector = first


### Tmux ###

[tmux]
colorterm = truecolor
; status = off|on|2|3|4
status = on
status-position = top
pane-status-position = bottom
show-clock-seconds = false
show-date-year = false
show-pane-index = true
hostname = ""

[tmux.theme]
primary = blue
highlight = hi-blue
accent = xterm110
attention = hi-yellow
monitor-bg = #000010

[log]
stderr-colored-bg = on
