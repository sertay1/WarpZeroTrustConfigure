[Setup]
AppName=WARP Configurator
AppVersion=2.3
AppPublisher=WARP Configurator Contributors
DefaultDirName={autopf}\WARP Configurator
DefaultGroupName=WARP Configurator
OutputDir=dist
OutputBaseFilename=WARP_Configurator_Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\icon.ico
PrivilegesRequired=lowest
ArchitecturesInstallIn64BitMode=x64

[Tasks]
Name: "desktopicon"; Description: "Masaüstü kısayolu oluştur"; GroupDescription: "Ek Kısayollar:"

[Files]
Source: "dist\WARP Configurator.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\WARP Configurator"; Filename: "{app}\WARP Configurator.exe"; IconFilename: "{app}\icon.ico"
Name: "{group}\Kaldır WARP Configurator"; Filename: "{uninstallexe}"; IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\WARP Configurator"; Filename: "{app}\WARP Configurator.exe"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\WARP Configurator.exe"; Description: "WARP Configurator uygulamasını başlat"; Flags: nowait postinstall skipifsilent
