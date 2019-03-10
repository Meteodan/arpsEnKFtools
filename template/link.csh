#!/bin/csh

set target_dir="./"
set n_ens_members=40
set n_ens=1

while ($n_ens <= $n_ens_members)
    set ens_pad=`printf "%03d" $n_ens`
    foreach t_ens (19990503.210000 19990504.000000 19990504.030000)
        ln -s $target_dir/3km050399NARR107x107bgandbc.$t_ens ena$ens_pad.$t_ens
    end
    @ n_ens = $n_ens + 1
end
