FROM breakdowns/mega-sdk-python:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt-get -qq update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/* && \
    apt-add-repository non-free && \
    apt-get -qq update && \
    apt-get -qq install -y p7zip-full mediainfo p7zip-rar aria2 curl pv jq ffmpeg locales python3-lxml libmms0 libc-ares2 libc6 libcrypto++6 libgcc1 libmediainfo0v5 libpcre3 libpcrecpp0v5 libssl1.1 libstdc++6 libzen0v5 zlib1g apt-transport-https gnupg2 && \ 
    apt-get purge -y software-properties-common
    curl https://mega.nz/linux/MEGAsync/Debian_9.0/amd64/megacmd_0.9.4-3.1_amd64.deb --output megacmd.deb 
    echo path-include /usr/share/doc/megacmd/* > /etc/dpkg/dpkg.cfg.d/docker 
    apt install ./megacmd.deb -y
COPY requirements.txt .
COPY extract /usr/local/bin
COPY pextract /usr/local/bin
RUN chmod +x /usr/local/bin/extract && chmod +x /usr/local/bin/pextract
RUN pip3 install --no-cache-dir -r requirements.txt
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \ 
locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY . .
COPY .netrc /root/.netrc
RUN chmod 600 /usr/src/app/.netrc
RUN chmod +x aria.sh

CMD ["bash","start.sh"]
