#!/bin/sh

for bytemodule in ./TC_*8.v; do
	wordmodule=$(echo $bytemodule | sed -e 's/8.v/16.v/g')
	cp -v "$bytemodule" "$wordmodule"
	dwordmodule=$(echo $bytemodule | sed -e 's/8.v/32.v/g')
	cp -v "$bytemodule" "$dwordmodule"
	qwordmodule=$(echo $bytemodule | sed -e 's/8.v/64.v/g')
	cp -v "$bytemodule" "$qwordmodule"
done

sed -i 's/8/16/g' ./TC_*16.v
sed -i 's/7/15/g' ./TC_*16.v
sed -i 's/2/3/g' ./TC_Sh*16.v
sed -i "s/16'b\(.\)/16'b\1\1\1\1_\1\1\1\1_\1/g" ./TC_*16.v

sed -i 's/8/32/g' ./TC_*32.v
sed -i 's/7/31/g' ./TC_*32.v
sed -i 's/2/4/g' ./TC_Sh*32.v
sed -i "s/32'b\(.\)/32'b\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1/g" ./TC_*32.v

sed -i 's/8/64/g' ./TC_*64.v
sed -i 's/7/63/g' ./TC_*64.v
sed -i 's/2/5/g' ./TC_Sh*64.v
sed -i "s/64'b\(.\)/64'b\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1\1\1\1_\1/g" ./TC_*64.v
