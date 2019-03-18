#!/bin/csh

set target_dir="./"
set n_ens_members=40
set n_ens=1
set date=20160331
set hour=21

while ($n_ens <= $n_ens_members)
    set ens_pad=`printf "%03d" $n_ens`
    foreach t_ens (${date}.${hour}0000 ${date}.${hour}0500 ${date}.${hour}1000 ${date}.${hour}1500 ${date}.${hour}2000 ${date}.${hour}2500 ${date}.${hour}3000 ${date}.${hour}3500 ${date}.${hour}4000 ${date}.${hour}4500 ${date}.${hour}5000 ${date}.${hour}5500)
        ln -s $target_dir/3kmbgfrom3DVAR.$t_ens ena$ens_pad.$t_ens
    end
    @ n_ens = $n_ens + 1
end
