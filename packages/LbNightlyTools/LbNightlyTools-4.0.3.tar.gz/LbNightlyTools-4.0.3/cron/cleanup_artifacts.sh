#!/bin/bash
###############################################################################
# (c) Copyright 2013 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

# Remove old data from the artifacts archive directory.
#
# Typical use in acrontab:
#
#   0 22 * * * lxplus.cern.ch curl -sSL https://gitlab.cern.ch/lhcb-core/LbNightlyTools/-/raw/master/cron/cleanup_artifacts.sh | bash
#


# prepare environment

logfile=/eos/user/l/lhcbsoft/logs/cleanup_artifacts.log
artifacts_dir=/eos/project/l/lhcbwebsites/www/lhcb-nightlies-artifacts

# clean up the artifacts directory (if present)
if [ -e ${artifacts_dir} ] ; then
    echo "$(date): removing old artifacts from ${artifacts_dir}" >> $logfile 2>&1
    find ${artifacts_dir} -mindepth 2 -maxdepth 3 \
        -daystart -mtime +15 -and -path '*/lhcb-*' \
        -print -exec rm -rf \{} \; >> $logfile 2>&1
    find ${artifacts_dir}/nightly/lhcb-master-mr -mindepth 2 -maxdepth 2 \
        -daystart -mtime +3 -and -name 'packs' \
        -print -exec rm -rf \{} \; >> $logfile 2>&1
    find ${artifacts_dir} \
        -daystart -mtime +1 -type f -and -name 'ccache_dir.*.zip' \
        -print -delete >> $logfile 2>&1
fi
echo "$(date): done" >> $logfile 2>&1
