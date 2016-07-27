

default=Prodsum-I250033-20160719.txt
sed -e "s/I250033/I250034/g" -e "s/eL.pL/eL.pR/g" \
    -e "s/6838/6839/g" -e "s/6834/6835/g" ${default} \
    > Prodsum-I250034-20160719.txt

sed -e "s/I250033/I250035/g" -e "s/eL.pL/eR.pR/g" \
    -e "s/6838/6840/g" -e "s/6834/6836/g" ${default} \
    > Prodsum-I250035-20160719.txt

sed -e "s/I250033/I250036/g" -e "s/eL.pL/eR.pL/g" \
    -e "s/6838/6841/g" -e "s/6834/6837/g" ${default} \
    > Prodsum-I250036-20160719.txt

