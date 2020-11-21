"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
const { exec } = require("child_process");
const path = require('path');
const cwd = path.resolve(__dirname, '../src');
const os_1 = require("os");
let shell = '';
let ext = '';
let pre = '';
//DETECT OS
if (os_1.platform() === 'win32') {
    shell = 'scripts/cmd';
    ext = '.cmd';
}
else {
    shell = 'scripts/bash';
    ext = '.sh';
    pre = './';
}
//DETECT ANACONDA
let detectConda = new Promise(function (resolve, reject) {
    exec("conda --version", (error, stdout, stderr) => {
        if (stderr) {
            shell = shell.concat('/venv');
            console.log(path.resolve(cwd, shell));
        }
        else {
            shell = path.join(shell, 'conda');
        }
        resolve();
    });
});
function activate(context) {
    return __awaiter(this, void 0, void 0, function* () {
        console.log('Activating the extension...');
        yield detectConda;
        //Environment setup
        exec(`${pre}check${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
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
                        exec(`${pre}setup${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
                            if (error) {
                                resolve(`error: ${error.message}`);
                                console.log(`error: ${error.message}`);
                                vscode.window.showErrorMessage('Environment was not loaded successfully');
                                return;
                            }
                            if (stderr) {
                                resolve(`stderr: ${stderr}`);
                                console.log(`stderr: ${stderr}`);
                                vscode.window.showErrorMessage('Environment was not loaded successfully');
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
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "Please, speak your command after the acoustic signal",
                cancellable: false
            }, (progress, token) => {
                return new Promise((resolve) => {
                    exec(`${pre}audiorecorder${ext}`, { cwd: path.resolve(cwd, shell) }, (error, stdout, stderr) => {
                        if (error) {
                            resolve(`error: ${error.message}`);
                            console.log(`error: ${error.message}`);
                            vscode.window.showErrorMessage('Recording failed');
                            return;
                        }
                        if (stderr) {
                            resolve(`stderr: ${stderr}`);
                            console.log(`stderr: ${stderr}`);
                            vscode.window.showErrorMessage('Recording failed');
                            return;
                        }
                        console.log(`stdout: ${stdout}`);
                        resolve(`stdout: ${stdout}`);
                        writeOnEditor(stdout); //to be moved where the response from python will be captured
                    });
                });
            });
        });
        context.subscriptions.push(disposable);
    });
}
exports.activate = activate;
function writeOnEditor(s) {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showWarningMessage('No editor available to write on');
        return;
    }
    const position = editor.selection.active;
    editor.edit((edit) => { edit.insert(position, s); });
}
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map