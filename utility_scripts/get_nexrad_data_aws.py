"""Gets NEXRAD level-2 data from AWS using the nexradaws module
"""
from datetime import datetime
import nexradaws

conn = nexradaws.NexradAwsInterface()


# TODO: make these command-line arguments
timestamp_start = '20130519225500'
timestamp_stop = '20130520030000'
radar = 'KTLX'

datetime_start = datetime.strptime(timestamp_start, '%Y%m%d%H%M%S')
datetime_stop = datetime.strptime(timestamp_stop, '%Y%m%d%H%M%S')

scans = conn.get_avail_scans_in_range(datetime_start, datetime_stop, radar)

results = conn.download(scans, './')

for scan in results.iter_success():
    print("{} volume scan time {}".format(scan.radar_id, scan.scan_time))

print("{} downloads failed.".format(results.failed_count))
