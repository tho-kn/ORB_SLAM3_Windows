wget -R "index.*" -m -np -nH --no-check-certificate -e robots=off \
    https://cdn3.vision.in.tum.de/tumvi/exported/euroc/512_16/
wget -R "index.*" -m -np -nH --no-check-certificate -e robots=off \
    https://vision.in.tum.de/tumvi/calibrated/512_16/

# optionally verify md5 sums:
cd tumvi/exported/euroc/512_16
md5sum -c *.md5