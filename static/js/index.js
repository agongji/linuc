import { Terminal } from '/node_modules/xterm/lib/xterm.js';
import { WebLinksAddon } from 'xterm-addon-web-links';
import { AttachAddon } from 'xterm-addon-attach';



const terminal = new Terminal();
// Load WebLinksAddon on terminal, this is all that's needed to get web links
// working in the terminal.
terminal.open(document.getElementById('terminal'));
terminal.write('Hello from \x1B[1;3;31mxterm.js\x1B[0m $ ')

terminal.loadAddon(new WebLinksAddon());

const attachAddon = new AttachAddon(webSocket);
terminal.loadAddon(attachAddon);