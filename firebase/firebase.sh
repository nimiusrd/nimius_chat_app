#!/bin/bash
if [ $FIREBASE_TOKEN ]; then
    firebase "$@" --token $FIREBASE_TOKEN
else
    firebase "$@"
fi
