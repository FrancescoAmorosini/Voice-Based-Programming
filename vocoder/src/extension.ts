import * as vscode from 'vscode';
const { exec } = require("child_process");
const path = require('path');

let cwd = path.resolve(__dirname, '../src');
let isActivated = false;

export function activate(context: vscode.ExtensionContext) {
	console.log('Congratulations, your extension "vocoder" is now active!');

	// The command has been defined in the package.json file
	// Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
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
