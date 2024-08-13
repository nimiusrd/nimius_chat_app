FROM node:lts-alpine

RUN npm install -g firebase-tools
COPY --chmod=755 firebase.sh /usr/bin/

ENTRYPOINT [ "/usr/bin/firebase.sh" ]
