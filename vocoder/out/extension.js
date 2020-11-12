"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const { exec } = require("child_process");
const path = require('path');
let cwd = path.resolve(__dirname, '../src');
let shell = '';
let ext = '';
//Detecting OS
exec("ls", (error, stdout, stderr) => {
    if (stderr) {
        shell = 'scripts/cmd';
        ext = '.cmd';
    }
    else {
        shell = 'scripts/bash';
        ext = '.sh';
    }
});
function activate(context) {
    console.log('Activating che extension...');
    //Environment setup
    exec(`check${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        if (stdout.includes('dsd-env')) {
            console.log('environment is ready!');
            vscode.window.showInformationMessage('Everything is ready! Let\'s code!');
        }
        else {
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "We are setting up your environment, it might take a few minutes...",
                cancellable: false
            }, (progress, token) => {
                return new Promise((resolve) => {
                    exec(`setup${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
                        if (error) {
                            console.log(`error: ${error.message}`);
                            return;
                        }
                        if (stderr) {
                            console.log(`stderr: ${stderr}`);
                            return;
                        }
                        resolve(`stdout: ${stdout}`);
                        console.log('environment is ready!');
                        vscode.window.showInformationMessage('Everything is ready! Let\'s code!');
                    });
                });
            });
        }
        console.log(`stdout: ${stdout}`);
    });
    //Disposable functions
    let disposable = vscode.commands.registerCommand('vocoder.captureAudio', () => {
        exec(`audiorecorder${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
            if (error) {
                console.log(`error: ${error.message}`);
                return;
            }
            if (stderr) {
                console.log(`stderr: ${stderr}`);
                return;
            }
            console.log(`stdout: ${stdout}`);
        });
    });
    context.subscriptions.push(disposable);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map