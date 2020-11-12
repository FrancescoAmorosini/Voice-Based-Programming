import * as vscode from 'vscode';
const { exec } = require("child_process");
const path = require('path');

let cwd = path.resolve(__dirname, '../src');
let isActivated = false;

export function activate(context: vscode.ExtensionContext) {
    console.log('Activating che extension...');
    var platform = navigator.platform;
    console.log(platform);
    exec("check.cmd", {cwd: path.resolve(cwd, 'bash')}, (error: any, stdout: any, stderr: any) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        if (stdout.includes('dsd-env')) {
            isActivated = true;
            console.log('environment is ready!');
            vscode.window.showInformationMessage('Everything is ready! Let\'s code!');
            
        }
        else {
            
            vscode.window.withProgress({
                location: vscode.ProgressLocation.Notification,
                title: "We are setting up your environment, it might take a few minutes...",
                cancellable: false
            }, (progress, token) => {
                return new Promise((resolve:any) => {
                    exec("setup.cmd", {cwd: path.resolve(cwd, 'bash')}, (error: any, stdout: any, stderr: any) => {
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

    //DISPOSABLES
	let disposable = vscode.commands.registerCommand('vocoder.captureAudio', () => {
        exec("audiorecorder.cmd", {cwd: path.resolve(cwd, 'bash')}, (error: any, stdout: any, stderr: any) => {
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

// this method is called when your extension is deactivated
export function deactivate() {}
