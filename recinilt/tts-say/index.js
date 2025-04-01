#!/usr/bin/env node
const cli = require('commander');
const Say = require('say').Say;
const say = new Say();
var textToSay = "hello";
cli
    .arguments('<textToSay>')
    .action((textToSay) => {
        say.speak(textToSay);
    })
cli.parse(process.argv);