; -- insta-bot-installer.iss --
[Setup]
AppName=Insta Bot
AppVersion=1.0
DefaultDirName={autopf}\InstaBot
DefaultGroupName=Insta Bot
OutputDir=dist_installer
OutputBaseFilename=InstaBotInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\assets\*"; DestDir: "{app}\assets"; Flags: recursesubdirs createallsubdirs
Source: "dist\.env"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Insta Bot"; Filename: "{app}\main.exe"
Name: "{group}\Uninstall Insta Bot"; Filename: "{uninstallexe}"
