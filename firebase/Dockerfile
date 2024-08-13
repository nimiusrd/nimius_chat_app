FROM node:lts-alpine

RUN npm install -g firebase-tools
ADD firebase.bash /usr/bin
RUN chmod +x /usr/bin/firebase.sh

ENTRYPOINT [ "/usr/bin/firebase.sh" ]
