FROM python:3.11-alpine as buildimage

COPY . /tmp/app_install

RUN set -eux; \
# wheel all packages for habapp
	cd /tmp/app_install; \
	pip wheel --wheel-dir=/root/wheels .

FROM python:3.11-alpine

COPY --from=buildimage /root/wheels /root/wheels
COPY container/entrypoint.sh /entrypoint.sh

ENV HABAPP_HOME=/habapp \
	USER_ID=9001 \
	GROUP_ID=${USER_ID}

RUN set -eux; \
# Install required dependencies
	apk update; \
	apk add \
		bash \
		su-exec \
		tini; \
	ln -s -f $(which su-exec) /usr/local/bin/su-exec; \
	mkdir -p ${HABAPP_HOME}; \
	mkdir -p ${HABAPP_HOME}/config; \
# install HABApp
	pip3 install \
    	--no-index \
    	--find-links=/root/wheels \
		habapp; \
# additional modules
        pip3 install \
        --find-links=/root/wheels \
        	influxdb_client; \

# prepare entrypoint script
	chmod +x /entrypoint.sh; \
# clean up
	rm -rf /root/wheels

WORKDIR ${HABAPP_HOME}
VOLUME ["${HABAPP_HOME}/config"]
ENTRYPOINT ["/entrypoint.sh"]

CMD ["su-exec", "habapp", "tini", "--", "python", "-m", "HABApp", "--config", "./config"]
