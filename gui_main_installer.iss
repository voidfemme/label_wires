; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{D4969DAE-D65F-46DA-96BA-51208A73F18B}
AppName=My Program
AppVersion=0.1.0
;AppVerName=My Program 0.1.0
AppPublisher=voidfemme
AppPublisherURL=https://github.com/voidfemme/label_wires
AppSupportURL=https://github.com/voidfemme/label_wires
AppUpdatesURL=https://github.com/voidfemme/label_wires
DefaultDirName={autopf}\Wire Labeling Tool
ChangesAssociations=yes
DisableProgramGroupPage=yes
InfoAfterFile=C:\Users\Rose\Programs\label_wires\README.md
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=WireLabelInstaller_v1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Setup]
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\Rose\Programs\label_wires\dist\gui_main.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\Classes\.csv\OpenWithProgids"; ValueType: string; ValueName: "WireLabelCSVFiles.csv"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\WireLabelCSVFiles.csv"; ValueType: string; ValueName: ""; ValueData: "WireLabel CSV Files"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\WireLabelCSVFiles.csv\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Wire Labeler.exe,0"
Root: HKA; Subkey: "Software\Classes\WireLabelCSVFiles.csv\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Wire Labeler.exe"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\Wire Labeler.exe\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{autoprograms}\My Program"; Filename: "{app}\Wire Labeler.exe"
Name: "{autodesktop}\My Program"; Filename: "{app}\Wire Labeler.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Wire Labeler.exe"; Description: "{cm:LaunchProgram,My Program}"; Flags: nowait postinstall skipifsilent
