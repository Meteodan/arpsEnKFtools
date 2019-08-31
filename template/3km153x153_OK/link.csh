#!/bin/csh

set target_dir="/depot/dawson29/data/users/sharm261/3km051913NAM153x153bgandbc/"
set n_ens_members=40
set n_ens=1

while ($n_ens <= $n_ens_members)
    set ens_pad=`printf "%03d" $n_ens`
    foreach t_ens (20130519.180000 20130519.190000 20130519.200000 20130519.210000 20130519.220000)
        ln -sf $target_dir/3km051913NAM153x153bgandbc.$t_ens ena$ens_pad.$t_ens
    end
    @ n_ens = $n_ens + 1
end
