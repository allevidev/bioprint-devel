; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
SignTool=MSSignTool $f
AppId={{E0A8300A-4192-49C9-8737-AE5573A02E5E}
AppName=Allevi Bioprint
AppVersion=1.5
;AppVerName=Allevi Bioprint 1.5
AppPublisher=Allevi, Inc.
AppPublisherURL=http://www.allevi3d.com/
AppSupportURL=http://www.allevi3d.com/
AppUpdatesURL=http://www.allevi3d.com/
DefaultDirName={pf}\Allevi Bioprint
DisableProgramGroupPage=yes
OutputBaseFilename=Allevi-Bioprint-1.5
Compression=lzma
SolidCompression=yes
SignedUninstaller=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "C:\Users\Administrator\Desktop\bioprint-devel\bioprint\dist\Allevi Bioprint\Allevi Bioprint.exe"; DestDir: "{app}"; Flags: ignoreversion signonce
Source: "C:\Users\Administrator\Desktop\bioprint-devel\bioprint\dist\Allevi Bioprint\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\Allevi Bioprint"; Filename: "{app}\Allevi Bioprint.exe"
Name: "{commondesktop}\Allevi Bioprint"; Filename: "{app}\Allevi Bioprint.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Allevi Bioprint"; Filename: "{app}\Allevi Bioprint.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\Allevi Bioprint.exe"; Description: "{cm:LaunchProgram,Allevi Bioprint}"; Flags: nowait postinstall skipifsilent

