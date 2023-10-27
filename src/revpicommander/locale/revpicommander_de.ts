<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="de_DE">
<context>
    <name>AclManager</name>
    <message>
        <location filename="../aclmanager.py" line="371"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="58"/>
        <source>There are errors in the ACL list!
Check the ALC levels of the red lines in the table. The ACL levels or ip addresses are invalid. If you save this dialog again, we will remove the wrong entries automatically.</source>
        <translation>Es gibt Fehler in der ACL Liste
Prüfe die roten Einträge in der Tabelle. ACL Level oder IP Adressen sind nicht gültig. Beim erneuten Speichern werden ungültige Einträge automatisch gelöscht.</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="81"/>
        <source>Unsaved entry</source>
        <translation>Nicht gespeicherter Eintrag</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="81"/>
        <source>You worked on a new ACL entry. Do you want to save that entry, too?</source>
        <translation>Es ist noch ein bearbeiteter Eintrag vorhanden. Soll dieser auch gespeichert werden?</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="272"/>
        <source>Question</source>
        <translation>Frage</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="98"/>
        <source>Do you really want to quit? 
Unsaved changes will be lost</source>
        <translation>Soll das Fenster wirklich geschlossen werden? 
Nicht gespeicherte Änderunen gehen verloren</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="129"/>
        <source>Select...</source>
        <translation>Auswahl...</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="143"/>
        <source>Level</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="191"/>
        <source>This entry has an invalid ACL level or wrong IP format!</source>
        <translation>Dieser Eintrag hat ein ungütiges ACL Lebel oder ein falsches IP Format!</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="272"/>
        <source>Do you really want to delete the following items?
{0}</source>
        <translation>Sollen die folgenden Einträge wirklich gelöscht werden?
{0}</translation>
    </message>
    <message>
        <location filename="../aclmanager.py" line="371"/>
        <source>Can not save new ACL entry! Check format of ip address and acl level is in value list.</source>
        <translation>Kann neuen ACL Eintrag nicht speichern! Bitte IP Adresse und ACL Level prüfen.</translation>
    </message>
</context>
<context>
    <name>AvahiSearch</name>
    <message>
        <location filename="../avahisearch.py" line="170"/>
        <source>Auto discovered</source>
        <translation>Automatisch erkannt</translation>
    </message>
    <message>
        <location filename="../avahisearch.py" line="290"/>
        <source> over SSH</source>
        <translation> über SSH</translation>
    </message>
</context>
<context>
    <name>ConnectionManager</name>
    <message>
        <location filename="../helper.py" line="549"/>
        <source>SIMULATING</source>
        <translation>SIMULATION</translation>
    </message>
    <message>
        <location filename="../helper.py" line="552"/>
        <source>NOT CONNECTED</source>
        <translation>NICHT VERBUNDEN</translation>
    </message>
    <message>
        <location filename="../helper.py" line="569"/>
        <source>SERVER ERROR</source>
        <translation>SERVER FEHLER</translation>
    </message>
    <message>
        <location filename="../helper.py" line="599"/>
        <source>RUNNING</source>
        <translation>LÄUFT</translation>
    </message>
    <message>
        <location filename="../helper.py" line="601"/>
        <source>PLC FILE NOT FOUND</source>
        <translation>SPS PROGRAMM NICHT GEFUNDEN</translation>
    </message>
    <message>
        <location filename="../helper.py" line="603"/>
        <source>NOT RUNNING (NO STATUS)</source>
        <translation>LÄUFT NICHT (KEIN STATUS)</translation>
    </message>
    <message>
        <location filename="../helper.py" line="605"/>
        <source>PROGRAM KILLED</source>
        <translation>PROGRAMM GETÖTET</translation>
    </message>
    <message>
        <location filename="../helper.py" line="607"/>
        <source>PROGRAM TERMED</source>
        <translation>PROGRAMM BEENDET</translation>
    </message>
    <message>
        <location filename="../helper.py" line="609"/>
        <source>NOT RUNNING</source>
        <translation>LÄUFT NICHT</translation>
    </message>
    <message>
        <location filename="../helper.py" line="611"/>
        <source>FINISHED WITH CODE {0}</source>
        <translation>BEENDET MIT CODE {0}</translation>
    </message>
    <message>
        <location filename="../helper.py" line="411"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
    <message>
        <location filename="../helper.py" line="361"/>
        <source>The combination of username and password was rejected from the SSH server.

Try again.</source>
        <translation>Die Kombination aus Benutzername und Password wurden vom SSH Server abgelehnt

Bitte erneut versuchen.</translation>
    </message>
    <message>
        <location filename="../helper.py" line="373"/>
        <source>Could not establish a SSH connection to server:

{0}</source>
        <translation>Konnte keine Verbindung zum SSH Server herstellen:

{0}</translation>
    </message>
    <message>
        <location filename="../helper.py" line="411"/>
        <source>Can not connect to RevPiPyLoad XML-RPC service! 

This could have the following reasons:
- The Revolution Pi is not online
- The RevPiPyLoad service is not running (activate it on your Revolution Pi)
- The RevPiPyLoad XML-RPC service is bind to localhost, only
- The ACL permission is not set for your IP!!!

Use &apos;Connect via SSH&apos; to use an encrypted connection or run &apos;sudo revpipyload_secure_installation&apos; on Revolution Pi to setup direct remote access!</source>
        <translation>Kann keine Verbindung zum RevPiPyLoad XML-RPC Dienst herstellen!

Das kann eine der folgenden Ursachen haben:
- Der Revolution Pi ist nicht online
- Der RevPiPyLoad Dienst läuft nicht (aktiviere Diesen auf dem Revolution Pi)
- Der RevPiPyLoad XML-RPC Dienst ist nur an localhost gebunden
- Die Berechtigungen sind nicht für diese IP gesetzt!!!

Benutze &quot;Über SSH verbinden&quot; um eine verschlüsselte Verbindung aufzubauen oder führe 'sudo revpipyload_secure_installation' auf dem Revolution Pi aus, um eine direkte Verbindung zu konfigurieren!</translation>
    </message>
    <message>
        <location filename="../helper.py" line="399"/>
        <source>Can not connect to RevPiPyLoad service through SSH tunnel!

This could have the following reasons:
- The RevPiPyLoad service is not running (activate it on your Revolution Pi)
- The RevPiPyLoad XML-RPC service is NOT bind to localhost
- The ACL permission is not set for 127.0.0.1!!!</source>
        <translation>Kann keine Verbindung zum RevPiPyLoad Dienst über SSH herstellen!

Das kann eine der folgenden Ursachen haben:
- Der RevPiPyLoad Dienst läuft nicht (aktiviere Diesen auf dem Revolution Pi)
- Der RevPiPyLoad XML-RPC Dienst ist NICHT an localhost gebunden
- Die Berechtigungen sind nicht für 127.0.0.1 gesetzt!!!</translation>
    </message>
</context>
<context>
    <name>DebugControl</name>
    <message>
        <location filename="../debugcontrol.py" line="137"/>
        <source>Driver reset for piControl detected.</source>
        <translation>Treiberneustart in piCtory erkannt.</translation>
    </message>
    <message>
        <location filename="../debugcontrol.py" line="177"/>
        <source>Error while getting values from Revolution Pi.</source>
        <translation>Fehler bei Werteempfang von RevPi.</translation>
    </message>
    <message>
        <location filename="../debugcontrol.py" line="232"/>
        <source>Auto update values...</source>
        <translation>Werte automatisch aktualisiert...</translation>
    </message>
    <message>
        <location filename="../debugcontrol.py" line="234"/>
        <source>Values updated...</source>
        <translation>Werte aktualisiert...</translation>
    </message>
    <message>
        <location filename="../debugcontrol.py" line="271"/>
        <source>Error set value of device &apos;{0}&apos; Output &apos;{1}&apos;: {2}
</source>
        <translation>Fehler beim Setzen des Ausgangs '{1}' auf Modul '{0}': {2}
</translation>
    </message>
    <message>
        <location filename="../debugcontrol.py" line="280"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
</context>
<context>
    <name>DebugIos</name>
    <message>
        <location filename="../debugios.py" line="231"/>
        <source>signed</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../debugios.py" line="236"/>
        <source>big_endian</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../debugios.py" line="222"/>
        <source>as text</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../debugios.py" line="224"/>
        <source>as number</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../debugios.py" line="380"/>
        <source>Can not use format text</source>
        <translation>Formatierung nicht möglich</translation>
    </message>
    <message>
        <location filename="../debugios.py" line="380"/>
        <source>Can not convert bytes {0} to a text for IO &apos;{1}&apos;. Switch to number format instead!</source>
        <translation>Kann bytes {0} für '{1}' nicht in Text konvertieren. Wechseln Sie auf Nummernformat!</translation>
    </message>
    <message>
        <location filename="../debugios.py" line="242"/>
        <source>switch wordorder</source>
        <translation>Wordorder tauschen</translation>
    </message>
</context>
<context>
    <name>MqttManager</name>
    <message>
        <location filename="../mqttmanager.py" line="82"/>
        <source>Question</source>
        <translation>Frage</translation>
    </message>
    <message>
        <location filename="../mqttmanager.py" line="95"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
    <message>
        <location filename="../mqttmanager.py" line="95"/>
        <source>Can not load the MQTT settings dialog. Missing values!</source>
        <translation>Kann MQTT Einstellungen nicht laden. Es fehlen Werte!</translation>
    </message>
    <message>
        <location filename="../mqttmanager.py" line="82"/>
        <source>Do you really want to quit? 
Unsaved changes will be lost.</source>
        <translation>Soll das Fenster wirklich geschlossen werden?
Ungesicherte Änderungen gehen verloren.</translation>
    </message>
</context>
<context>
    <name>RevPiCommander</name>
    <message>
        <location filename="../revpicommander.py" line="330"/>
        <source>Simulator started...</source>
        <translation>Simulator gestartet...</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="339"/>
        <source>Can not start...</source>
        <translation>Kann nicht gestartet werden...</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="532"/>
        <source>Warning</source>
        <translation>Warnung</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="355"/>
        <source>This version of Logviewer ist not supported in version {0} of RevPiPyLoad on your RevPi! You need at least version 0.4.1.</source>
        <translation>Diese Version vom Logbetrachter wird in RevPiPyLoad Version {0} nicht unterstützt! Es wird mindestens Version 0.4.1 benötigt.</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="405"/>
        <source>XML-RPC access mode in the RevPiPyLoad configuration is too small to access this dialog!</source>
        <translation>XML-RPC Zugriffsberechtigung in der RevPiPyLoad Konfiguraiton ist zu klein für diese Einstellungen!</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="559"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="385"/>
        <source>The Version of RevPiPyLoad on your Revolution Pi ({0}) is to old. This Version of RevPiCommander require at least version 0.6.0 of RevPiPyLoad. Please update your Revolution Pi!</source>
        <translation>Die Version von RevPiPyLoad ({0}) auf dem Revolution Pi ist zu alt. Diese Version vom RevPiCommander braucht mindestens Version 0.6.0. Bitte aktualisiere deinen Revolution Pi!</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="438"/>
        <source>Question</source>
        <translation>Frage</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="438"/>
        <source>Are you sure to reset piControl?
The pictory configuration will be reloaded. During that time the process image will be interrupted and could rise errors on running control programs!</source>
        <translation>Soll piControl wirklich zurückgesetzt werden?
Die piCtory Konfiguration wird neu geladen. Das Prozessabbild wird in dieser Zeit nicht verfügbar sein und es könnten Fehler in Steuerungsprogrammen ausgelöst werden!</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="451"/>
        <source>Success</source>
        <translation>Erfolgreich</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="451"/>
        <source>piControl reset executed successfully</source>
        <translation>piControl wurde erfolgreich zurückgesetzt</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="458"/>
        <source>piControl reset could not be executed successfully</source>
        <translation>piControl konnte nicht zurückgesetzt werden</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="506"/>
        <source>Reset to piCtory defaults...</source>
        <translation>Standardwerte von piCtory laden...</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="532"/>
        <source>The watch mode ist not supported in version {0} of RevPiPyLoad on your RevPi! You need at least version 0.5.3! Maybe the python3-revpimodio2 module is not installed on your RevPi at least version 2.0.0.</source>
        <translation>Der SPS Betrachter ist in Version {0} von RevPiPyLoad auf dem Rev Pi nicht unterstützt! Es muss mindestens Version 0.5.3 installiert sein! Vielleicht fehlt auch das python3-revpimodio2 Modul, welches mindestens Version 2.0.0 haben muss.</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="544"/>
        <source>Can not load this function, because your ACL level is to low!
You need at least level 1 to read or level 3 to write.</source>
        <translation>Für diese Funktion ist das Berechtigungslevel zu gering!
Es muss mindestens Level 1 zum Lesen oder Level 3 zu Schreiben sein.</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="559"/>
        <source>Can not load piCtory configuration. 
Did you create a hardware configuration? Please check this in piCtory!</source>
        <translation>Kann piCtory Konfiguration nicht laden.
Wurde eine Hardwarekonfiguration in piCtory erzeugt? Bitte prüfe dies in piCtory!</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="330"/>
        <source>The simulator is running!

You can work with this simulator if your call RevPiModIO with this additional parameters:
procimg={0}
configrsc={1}

You can copy that from header textbox.</source>
        <translation>Der Simulator läuft!

Du kannst mit der Simulation arbeiten, wenn du RevPiModIO mit diesen zusätzlichen Parametern instantiierst:
procimg={0}
configrsc={1}

Dies kann aus der Textbox oben kopiert werden.</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="339"/>
        <source>Can not start the simulator! Maybe the piCtory file is corrupt or you have no write permissions for &apos;{0}&apos;.</source>
        <translation>Kann Simulator nicht starten! Vielleicht ist die piCtory Datei defekt oder es gibt keine Schreibberechtigung für '{0}'.</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="506"/>
        <source>Do you want to reset your process image to {0} values?
You have to stop other RevPiModIO programs before doing that, because they could reset the outputs.</source>
        <translation>Soll das virtuelle Prozessabbild auf {0} zurückgesetzt werden?
Es sollten alle RevPiModIO Programme vorher beendet werden, da diese ihre IO Werte sofort wieder schreiben würden.</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="506"/>
        <source>zero</source>
        <translation>null</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="506"/>
        <source>piCtory default</source>
        <translation>piCtory Standardwerte</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="260"/>
        <source>Revolution Pi connected!</source>
        <translation>Revolution Pi verbunden!</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="297"/>
        <source>Connecting...</source>
        <translation>Verbinde...</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="260"/>
        <source>Establish a connection to the Revolution Pi...</source>
        <translation>Baue eine Verbindung zum Revolution Pi auf...</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="143"/>
        <source>Information</source>
        <translation>Information</translation>
    </message>
    <message>
        <location filename="../revpicommander.py" line="143"/>
        <source>Can not connect to RevPiPyLoad service through SSH tunnel!

We are trying to activate this service now and reconnect. The settings can be changed at any time via &apos;webstatus&apos;.</source>
        <translation>Vielleicht läuft der RevPiPyLoad Dienst nicht.

Wir versuchen diesen Dienst jetzt zu aktivieren und verbinden uns neu. Die Einstellungen können über 'Webstatus' jederzeit geändert werden.</translation>
    </message>
</context>
<context>
    <name>RevPiFiles</name>
    <message>
        <location filename="../revpifiles.py" line="87"/>
        <source>Please select...</source>
        <translation>Bitte auswählen...</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="602"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="121"/>
        <source>Can not stop plc program on Revolution Pi.</source>
        <translation>Kann SPS Programm auf Rev Pi nicht stoppen.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="144"/>
        <source>The Revolution Pi could not process some parts of the transmission.</source>
        <translation>Der Revolution Pi hat Teile der Übertragung nicht durchgeführt.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="152"/>
        <source>Errors occurred during transmission</source>
        <translation>Fehler bei Übertragung aufgetreten</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="158"/>
        <source>Warning</source>
        <translation>Warnung</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="158"/>
        <source>Could not start the plc program on Revolution Pi.</source>
        <translation>Kann das SPS Programm auf dem Revolution Pi nicht starten.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="276"/>
        <source>Can not open last directory &apos;{0}&apos;.</source>
        <translation>Kann letztes Verzeichnis '{0}' nicht öffnen.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="333"/>
        <source>Stop scanning for files, because we found more than {0} files.</source>
        <translation>Dateisuche wurde angehalten, da mehr als {0} Dateien gefunden wurden.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="375"/>
        <source>Could not load path of working dir</source>
        <translation>Kann Arbeitsverzeichnis nicht laden</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="440"/>
        <source>Can not load file list from Revolution Pi.</source>
        <translation>Kann Dateiliste vom Revolution Pi nicht laden.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="472"/>
        <source>Select folder...</source>
        <translation>Ordner auswählen...</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="483"/>
        <source>Can not access the folder &apos;{0}&apos; to read files.</source>
        <translation>Keine Berechtigung für Zugriff auf Ordner '{0}'.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="584"/>
        <source>Error...</source>
        <translation>Fehler...</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="533"/>
        <source>Error while download file &apos;{0}&apos;.</source>
        <translation>Fehler beim Herunterladen der Datei '{0}'.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="541"/>
        <source>Override files...</source>
        <translation>Dateien überschreiben...</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="541"/>
        <source>One or more files does exist on your computer! Do you want to override the existingfiles?

Select &apos;Yes&apos; to override, &apos;No&apos; to download only missing files.</source>
        <translation>Eine oder mehrere Dateien existieren auf diesem Computer! Sollen bestehende Dateien überschrieben werden?

Wählen Sie 'Ja' zum Überschreiben, 'Nein' um nur fehlende Dateien zu laden.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="573"/>
        <source>Delete files from Revolution Pi...</source>
        <translation>Dateien auf Rev Pi löschen...</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="573"/>
        <source>Do you want to delete {0} files from revolution pi?</source>
        <translation>Sollen {0} Dateien vom Revolution Pi gelöscht werden?</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="584"/>
        <source>Error while delete file &apos;{0}&apos;.</source>
        <translation>Fehler beim Löschen der Datei '{0}'.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="135"/>
        <source>Information</source>
        <translation>Information</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="135"/>
        <source>A PLC program has been uploaded. Please check the PLC program settings to see if the correct program is specified as the start program.</source>
        <translation>Ein SPS Programm wurde hochgeladen. Bitte prüfe die SPS Programmeinstellungen ob das richtige Startprogramm gewählt ist.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="203"/>
        <source>Choose a local directory first.</source>
        <translation>Lokales Verzeichnis wählen.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="129"/>
        <source>File transfer...</source>
        <translation>Dateiübertragung...</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="179"/>
        <source>Upgrade your Revolution Pi! This function needs at least &apos;revpipyload&apos; 0.11.0</source>
        <translation>Aktualisiere deinen Revolution Pi! Diese Funktion benötigt mindestens 'revpipyload' 0.11.0</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="198"/>
        <source>Upgrade your Revolution Pi! This function needs at least &apos;revpipyload&apos; 0.9.5</source>
        <translation>Aktualisiere deinen Revolution Pi! Diese Funktion benötigt mindestens 'revpipyload' 0.9.5</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="193"/>
        <source>Deletes selected files immediately on the Revolution Pi</source>
        <translation>Löscht ausgewählte Dateien sofort auf dem Revolution Pi</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="602"/>
        <source>The settings could not be saved on the Revolution Pi!
Try to save the values one mor time and check the log files of RevPiPyLoad if the error rises again.</source>
        <translation>Die Einstellungen konnten nicht auf dem Revolution Pi gespeichert werden!
Versuche es erneut und prüfe die Logdateien von RevPiPyLoad, wenn der Fehler erneut auftritt.</translation>
    </message>
    <message>
        <location filename="../revpifiles.py" line="171"/>
        <source>Set as start file</source>
        <translation>Als Startdatei festlegen</translation>
    </message>
</context>
<context>
    <name>RevPiInfo</name>
    <message>
        <location filename="../revpiinfo.py" line="45"/>
        <source>Can not load file list</source>
        <translation>Kann Dateiliste nicht laden</translation>
    </message>
    <message>
        <location filename="../revpiinfo.py" line="50"/>
        <source>Not connected</source>
        <translation>Nicht verbunden</translation>
    </message>
</context>
<context>
    <name>RevPiLogfile</name>
    <message>
        <location filename="../revpilogfile.py" line="210"/>
        <source>Can not access log file on the RevPi</source>
        <translation>Kann auf Logbuch vom RevPi nicht zugreifen</translation>
    </message>
</context>
<context>
    <name>RevPiOption</name>
    <message>
        <location filename="../revpioption.py" line="345"/>
        <source>Question</source>
        <translation>Frage</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="188"/>
        <source>The settings will be set on the Revolution Pi now.

ACL changes and service settings are applied immediately.</source>
        <translation>Die Einstellungen werden jetzt auf dem Revolution Pi angewendet.

Berechtigungseinstellungen werden sofort gesetzt.</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="235"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="235"/>
        <source>The settings could not be saved on the Revolution Pi!
Try to save the values one mor time and check the log files of RevPiPyLoad if the error rises again.</source>
        <translation>Die Einstellungen konnten nicht auf dem Revolution Pi gespeichert werden!
Versuche es erneut und prüfe die Logdateien von RevPiPyLoad, wenn der Fehler erneut auftritt.</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="245"/>
        <source>Do you really want to quit? 
Unsaved changes will be lost.</source>
        <translation>Soll das Fenster wirklich geschlossen werden?
Ungesicherte Änderungen gehen verloren.</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="294"/>
        <source>running</source>
        <translation>läuft</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="294"/>
        <source>stopped</source>
        <translation>angehalten</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="285"/>
        <source>The MQTT service is not available on your RevPiPyLoad version.</source>
        <translation>MQTT ist in der RevPiPyLoad Version nicht verfügbar.</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="325"/>
        <source>read only</source>
        <translation>Nur lesen</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="325"/>
        <source>read and write</source>
        <translation>lesen und schreiben</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="345"/>
        <source>Are you sure you want to deactivate the XML-RPC server? You will NOT be able to access the Revolution Pi with this program after saving the options!</source>
        <translation>Willst du den XML-RPC Server wirklich deaktivieren? Du wirst dich NICHT mehr mit diesem Programm zum Revolution Pi verbinden können!</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="357"/>
        <source>Start/Stop PLC program and read logs</source>
        <translation>SPS Programm starten/stoppen und Logs lesen</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="357"/>
        <source>+ read IOs in watch mode</source>
        <translation>+ EAs in SPS Betrachter lesen</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="357"/>
        <source>+ read properties and download PLC program</source>
        <translation>+ Einstellungen lesen und SPS Programm herunterladen</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="357"/>
        <source>+ upload PLC program</source>
        <translation>+ SPS Programm hochladen</translation>
    </message>
    <message>
        <location filename="../revpioption.py" line="357"/>
        <source>+ set properties</source>
        <translation>+ Einstellungen ändern</translation>
    </message>
</context>
<context>
    <name>RevPiPlcList</name>
    <message>
        <location filename="../revpiplclist.py" line="304"/>
        <source>Question</source>
        <translation>Frage</translation>
    </message>
    <message>
        <location filename="../revpiplclist.py" line="135"/>
        <source>Do you really want to quit? 
Unsaved changes will be lost.</source>
        <translation>Soll das Fenster wirklich geschlossen werden?
Ungesicherte Änderungen gehen verloren.</translation>
    </message>
    <message>
        <location filename="../revpiplclist.py" line="304"/>
        <source>If you remote this folder, all containing elements will be removed, too. 

Do you want to delete folder and all elements?</source>
        <translation>Wird dieser Ordner gelöscht, betrifft dies auch alle Elemente im Ordner.

Wollen sie den Ordner und alle Elemente löschen?</translation>
    </message>
    <message>
        <location filename="../revpiplclist.py" line="344"/>
        <source>New folder</source>
        <translation>Neuer Ordner</translation>
    </message>
</context>
<context>
    <name>RevPiProgram</name>
    <message>
        <location filename="../revpiprogram.py" line="674"/>
        <source>Error</source>
        <translation>Fehler</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="106"/>
        <source>You have to select a start program, before uploading the settings.</source>
        <translation>Es muss erst ein Startprogramm gewählt werden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="148"/>
        <source>Question</source>
        <translation>Frage</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="114"/>
        <source>The settings will be set on the Revolution Pi now.

If you made changes on the &apos;PCL Program&apos; section, your plc program will restart now!</source>
        <translation>Die Einstellungen werden jetzt auf dem Revolution Pi angewendet.

Sollte es Änderungen in dem SPS Programmabschnitt geben, wird das SPS Programm neu gestartet!</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="138"/>
        <source>The settings could not be saved on the Revolution Pi!
Try to save the values one mor time and check the log files of RevPiPyLoad if the error rises again.</source>
        <translation>Die Einstellungen konnten nicht auf dem Revolution Pi gespeichert werden!
Versuche es erneut und prüfe die Logdateien von RevPiPyLoad, wenn der Fehler erneut auftritt.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="148"/>
        <source>Do you really want to quit? 
Unsaved changes will be lost.</source>
        <translation>Soll das Fenster wirklich geschlossen werden?
Ungesicherte Änderungen gehen verloren.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="188"/>
        <source>Reset driver...</source>
        <translation>Treiber zurücksetzen...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="188"/>
        <source>Reset piControl driver after successful uploading new piCtory configuration?
The process image will be interrupted for a short time!</source>
        <translation>Soll piControl nach dem erfolgreichen Hochladen der neuen piCtory Konfiguration zurückgesetzt werden?
Das Prozessabbild wird kurzzeitig nicht verfügbar sein!</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="203"/>
        <source>Got an network error while send data to Revolution Pi.
Please try again.</source>
        <translation>Beim Senden der Daten an den Revolution Pi trat ein Netzwerkfehler auf.
Versuche es erneut.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="684"/>
        <source>Success</source>
        <translation>Erfolgreich</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="212"/>
        <source>The transfer of the piCtory configuration and the reset of piControl have been successfully executed.</source>
        <translation>Die piCtory Übertragung und der Reset von piControl wurden erfolgreich durchgeführt.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="220"/>
        <source>The piCtory configuration was successfully transferred.</source>
        <translation>Die piCtory Konfiguration wurde erfolgreich übertragen.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="227"/>
        <source>Can not process the transferred file.</source>
        <translation>Kann die Übertragene Datei nicht verarbeiten.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="233"/>
        <source>Can not find main elements in piCtory file.</source>
        <translation>Konnte piCtory Struktur nicht erkennen.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="239"/>
        <source>Contained devices could not be found on Revolution Pi. The configuration may be from a newer piCtory version!</source>
        <translation>Enthaltene Module können auf dem Revolution Pi nicht gefunden werden. Die Konfiguraiton könnte von einer neueren piCtory Version stammen!</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="246"/>
        <source>Could not load RAP catalog on Revolution Pi.</source>
        <translation>Kann RAP Katalog auf dem Revolution Pi nicht laden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="252"/>
        <source>The piCtory configuration could not be written on the Revolution Pi.</source>
        <translation>Die piCtory Konfiguration konnte nicht auf dem Revolution Pi geschrieben werden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="259"/>
        <source>Warning</source>
        <translation>Warnung</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="259"/>
        <source>The piCtroy configuration has been saved successfully.
An error occurred on piControl reset!</source>
        <translation>Die piCtory Konfiguration wurde erfolgreich hochgeladen.
Es trat jedoch ein Fehler beim Zurücksetzen von piControl auf!</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="323"/>
        <source>Save ZIP archive...</source>
        <translation>ZIP Archiv speichern...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="413"/>
        <source>ZIP archive (*.zip);;All files (*.*)</source>
        <translation>ZIP Archive (*.zip);;Alle Dateien (*.*)</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="341"/>
        <source>Save TGZ archive...</source>
        <translation>TGZ Archiv speichern...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="341"/>
        <source>TGZ archive (*.tgz);;All files (*.*)</source>
        <translation>TAR Archive (*.tgz);;Alle Dateien (*.*)</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="368"/>
        <source>Could not load PLC program from Revolution Pi.</source>
        <translation>Kann SPS Programm nicht vom Revolution Pi laden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="381"/>
        <source>Coud not save the archive or extract the files!
Please retry.</source>
        <translation>Konnte das Archiv nicht speichern oder extrahieren!
Versuche es erneut.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="387"/>
        <source>Transfer successfully completed.</source>
        <translation>Übertragung erfolgreich abgeschlossen.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="413"/>
        <source>Upload content of ZIP archive...</source>
        <translation>ZIP Archiv hochladen...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="438"/>
        <source>The selected file ist not a ZIP archive.</source>
        <translation>Die ausgewählte Datei ist kein ZIP Archiv.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="447"/>
        <source>Upload content of TAR archive...</source>
        <translation>TAR Archiv hochladen...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="447"/>
        <source>TAR archive (*.tgz);;All files (*.*)</source>
        <translation>TAR Archive (*.tgz);;Alle Dateien (*.*)</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="472"/>
        <source>The selected file ist not a TAR archive.</source>
        <translation>Die ausgewählte Datei ist kein TAR Archiv.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="481"/>
        <source>No files to upload...</source>
        <translation>Keine Dateien zum Hochladen...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="481"/>
        <source>Found no files to upload in given location or archive.</source>
        <translation>Konnte keine Dateien in der Quelle zum Hochladen finden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="492"/>
        <source>There was an error deleting the files on the Revolution Pi.
Upload aborted! Please try again.</source>
        <translation>Beim Löschen der Dateien auf dem Revolution Pi ist ein Fehler aufgetreten.
Hochladen abgebrochen! Versuche es erneut.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="538"/>
        <source>The PLC program was transferred successfully.</source>
        <translation>Das SPS Programm wurde erfolgreich übertragen.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="546"/>
        <source>Information</source>
        <translation>Information</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="546"/>
        <source>Could not find the selected PLC start program in uploaded files.
This is not an error, if the file was already on the Revolution Pi. Check PLC start program field</source>
        <translation>Konnte eingestelltes SPS Starprogramm in hochgeladenen Dateien nicht finden.
Dies ist kein Fehler, wenn das SPS Startprogramm bereits auf dem Rev Pi ist. Prüfe SPS Programm Einstellungen</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="559"/>
        <source>There is no piCtory configuration in this archive.</source>
        <translation>Kann keine piCtory Konfiguration im Archiv finden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="566"/>
        <source>The Revolution Pi could not process some parts of the transmission.</source>
        <translation>Der Revolution Pi konnte Teile der Übertragung nicht verarbeiten.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="573"/>
        <source>Errors occurred during transmission.</source>
        <translation>Fehler bei Übertragung aufgetreten.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="592"/>
        <source>Save piCtory file...</source>
        <translation>piCtory Datei speichern...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="632"/>
        <source>piCtory file (*.rsc);;All files (*.*)</source>
        <translation>piCtory Datei (*.rsc);;Alle Dateien (*.*)</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="611"/>
        <source>Could not load piCtory file from Revolution Pi.</source>
        <translation>Kann piCtory Konfiguration nicht vom Revolution Pi laden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="621"/>
        <source>piCtory configuration successfully loaded and saved to:
{0}.</source>
        <translation>piCtory Konfiguration erfolgreich geladen und gespeichert als:
{0}.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="632"/>
        <source>Upload piCtory file...</source>
        <translation>piCtory datei hochladen...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="653"/>
        <source>Save piControl file...</source>
        <translation>piCtory Datei speichern...</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="653"/>
        <source>Process image file (*.img);;All files (*.*)</source>
        <translation>Processabbild (*.img);;Alle Dateien (*.*)</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="674"/>
        <source>Could not load process image from Revolution Pi.</source>
        <translation>Kann Prozessabbild von Revolution Pi nicht laden.</translation>
    </message>
    <message>
        <location filename="../revpiprogram.py" line="684"/>
        <source>Process image successfully loaded and saved to:
{0}.</source>
        <translation>Prozessabbild erfolgreich geladen und gespeichert als:
{0}.</translation>
    </message>
</context>
<context>
    <name>SSHAuth</name>
    <message>
        <location filename="../sshauth.py" line="51"/>
        <source>Could not save password</source>
        <translation>Konnte Kennwort nicht speichern</translation>
    </message>
    <message>
        <location filename="../sshauth.py" line="51"/>
        <source>Could not save password to operating systems password save.

Maybe your operating system does not support saving passwords. This could be due to missing libraries or programs.

This is not an error of RevPi Commander.</source>
        <translation>Konnte das Kennwort nicht im Kennwortspeicher des Betriebssystems speichern.

Vielleicht untersützt das Betriebssystem keine Kennwortspeicherung. Dies könnte an fehlenden Bibliotheken oder Programmen liegen.

Dies ist kein Fehler von RevPi Commander.</translation>
    </message>
</context>
<context>
    <name>Simulator</name>
    <message>
        <location filename="../simulator.py" line="79"/>
        <source>Select downloaded piCtory file...</source>
        <translation>Heruntergeladene piCtory Datei auswählen...</translation>
    </message>
    <message>
        <location filename="../simulator.py" line="79"/>
        <source>piCtory file (*.rsc);;All files (*.*)</source>
        <translation>piCtory Datei (*.rsc);;Alle Dateien (*.*)</translation>
    </message>
</context>
<context>
    <name>diag_aclmanager</name>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="14"/>
        <source>IP access control list</source>
        <translation>IP Berechtigungsliste</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="20"/>
        <source>Existing ACLs</source>
        <translation>Aktuelle ACLs</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="54"/>
        <source>IP Address</source>
        <translation>IP Adresse</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="59"/>
        <source>Access Level</source>
        <translation>Berechtigungslevel</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="75"/>
        <source>&amp;Edit</source>
        <translation>&amp;Bearbeiten</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="88"/>
        <source>&amp;Remove</source>
        <translation>&amp;Löschen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="100"/>
        <source>Add / Edit access entry</source>
        <translation>Eintrag hinzufügen / bearbeiten</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="106"/>
        <source>Clear fields</source>
        <translation>Felder leeren</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="113"/>
        <source>&amp;Save entry</source>
        <translation>Eintrag &amp;Speichern</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="122"/>
        <source>IP address:</source>
        <translation>IP Adresse:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/aclmanager.ui" line="129"/>
        <source>Access level:</source>
        <translation>Berechtigungslevel:</translation>
    </message>
</context>
<context>
    <name>diag_connections</name>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="14"/>
        <source>Revolution Pi connections</source>
        <translation>Revolution Pi Verbindungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="197"/>
        <source>Connection name</source>
        <translation>Verbindungsname</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="202"/>
        <source>Address</source>
        <translation>Adresse</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="30"/>
        <source>Display name:</source>
        <translation>Anzeigename:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="102"/>
        <source>Sub folder:</source>
        <translation>Unterordner:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="40"/>
        <source>Address (DNS/IP):</source>
        <translation>Adresse (DNS/IP):</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="50"/>
        <source>Port (Default {0}):</source>
        <translation>Port (Standard {0}):</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="76"/>
        <source>Connection timeout:</source>
        <translation>Verbindungs-Timeout:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="89"/>
        <source> sec.</source>
        <translation> Sek.</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="24"/>
        <source>Connection</source>
        <translation>Verbindung</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="125"/>
        <source>Over SSH</source>
        <translation>Über SSH</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="131"/>
        <source>Connect over SSH tunnel:</source>
        <translation>Über SSH Tunnel verbinden:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="148"/>
        <source>SSH port:</source>
        <translation>SSH Port:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiplclist.ui" line="165"/>
        <source>SSH user name:</source>
        <translation>SSH Benutzername:</translation>
    </message>
</context>
<context>
    <name>diag_mqtt</name>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="14"/>
        <source>MQTT settings</source>
        <translation>MQTT Einstellungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="20"/>
        <source>Base topic</source>
        <translation>Basistopic</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="44"/>
        <source>Base topic:</source>
        <translation>Basistopic:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="57"/>
        <source>Publish settings</source>
        <translation>Publish Einstellungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="63"/>
        <source>Publish all exported values every n seconds:</source>
        <translation>Exportierte Werte all n Sekunden senden:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="87"/>
        <source>Send exported values immediately on value change</source>
        <translation>Exportierte Werte sofort bei Änderung senden</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="104"/>
        <source>Set outputs</source>
        <translation>Ausgänge setzen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="128"/>
        <source>Allow MQTT to to set outputs on Revolution Pi</source>
        <translation>Erlaube per MQTT Ausgänge auf dem RevPi zu setzen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="144"/>
        <source>Broker address:</source>
        <translation>Broker Adresse:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="154"/>
        <source>Broker port:</source>
        <translation>Broker Port:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="161"/>
        <source>User name:</source>
        <translation>Benutzername:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="168"/>
        <source>Password:</source>
        <translation>Passwort:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="203"/>
        <source>Use TLS</source>
        <translation>TLS benutzen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="138"/>
        <source>Broker settings</source>
        <translation>Broker Einstellungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="32"/>
        <source>The base topic is the first part of any mqtt topic, the Revolution Pi will publish. You can use any character includig &apos;/&apos; to structure the messages on your broker.

For example: revpi0000/data</source>
        <translation>Der Basistopic wird allen MQTT Topics vorangestellt, welche der Revolution Pi veröffentlicht. Es können alle Zeichen inklusive '/' verwendet werden, um die Nachrichten auf dem Broker zu strukturieren.

Zum Beispiel: revpi0000/data</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="80"/>
        <source>Topic:    [basetopic]/io/[ioname]</source>
        <translation>Topic:    [basistopic]/io/[eaname]</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="94"/>
        <source>Topic:    [basetopic]/event/[ioname]</source>
        <translation>Topic:    [basistopic]/io/[eaname]</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="116"/>
        <source>The Revolution Pi will subscribe a topic on which your mqtt client can publish messages with the new io value as payload.

Publish values with topic:    [basetopic]/set/[outputname]</source>
        <translation>Der Revolution Pi abonniert ein Topic, auf dem die MQTT Clients über den Inhalt einer Nachricht einen neuen Ausgangswert setzen können.

Sende Werte mit Topic:    [basistopic]/set/[ausgangsname]</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/mqttmanager.ui" line="175"/>
        <source>Client ID:</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>diag_options</name>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="14"/>
        <source>RevPi Python PLC Options</source>
        <translation>RevPi Python SPS Einstellungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="20"/>
        <source>Start / Stop behavior of PLC program</source>
        <translation>Start- / Stopverhalten des SPS Programms</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="26"/>
        <source>Replace IO file:</source>
        <translation>EA Ersetzungsdatei:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="104"/>
        <source>... sucessfully without error</source>
        <translation>... erfolgreich beendet wird</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="33"/>
        <source>... after exception and errors</source>
        <translation>...durch Fehler abstürzt</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="40"/>
        <source>Start PLC program automatically</source>
        <translation>Starte SPS Programm automatisch</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="128"/>
        <source>Restart PLC program after exit or crash</source>
        <translation>Starte SPS Programm nach Absturz neu</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="73"/>
        <source>Set process image to NULL if program terminates...</source>
        <translation>Setze Prozessabbild auf NULL, wenn das Programm...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="81"/>
        <source>Do not use replace io file</source>
        <translation>Keine Ersetzungsdatei verwenden</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="86"/>
        <source>Use static file from RevPiPyLoad</source>
        <translation>Statische Datei von RevPiPyLoad</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="91"/>
        <source>Use dynamic file from work directory</source>
        <translation>Dynamisch aus Arbeitsverzeichnis</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="96"/>
        <source>Give own path and filename</source>
        <translation>Eigener Pfad und Dateiname</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="111"/>
        <source>Restart delay in seconds:</source>
        <translation>Neustartverzögerung in Sekunden:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="148"/>
        <source>RevPiPyLoad server services</source>
        <translation>RevPiPyLoad Serverdienste</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="222"/>
        <source>Edit ACL</source>
        <translation>ACL bearbeiten</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="161"/>
        <source>MQTT process image publisher</source>
        <translation>MQTT Processabbild Publisher</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="168"/>
        <source>Start RevPi piControl server</source>
        <translation>Starte RevPi piControl Server</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="195"/>
        <source>status</source>
        <translation>Status</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="185"/>
        <source>piControl server is:</source>
        <translation>piControl Serverstatus:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="205"/>
        <source>MQTT publish service is:</source>
        <translation>MQTT Servicestatus:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="215"/>
        <source>Settings</source>
        <translation>Einstellungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="48"/>
        <source>Do nothing</source>
        <translation>Keine Aktion</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="53"/>
        <source>Restart after piCtory changed</source>
        <translation>Neustart nach piCtory Änderungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="58"/>
        <source>Always restart the PLC program</source>
        <translation>SPS Programm immer neu starten</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="66"/>
        <source>Driver reset action:</source>
        <translation>Aktion bei Treiberneustart:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="138"/>
        <source>PLC program behavior after piCtory driver reset clicked</source>
        <translation>Aktion nach piCtory Neustart mit SPS Programm</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpioption.ui" line="229"/>
        <source>Activate XML-RPC for RevPiCommander</source>
        <translation>Aktiviere XML-RPC für RevPiCommander</translation>
    </message>
</context>
<context>
    <name>diag_oss_licenses</name>
    <message>
        <location filename="../../../ui_dev/oss_licenses.ui" line="14"/>
        <source>Open-Source licenses</source>
        <translation>Open-Source Lizenzen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/oss_licenses.ui" line="52"/>
        <source>Software</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../ui_dev/oss_licenses.ui" line="57"/>
        <source>License</source>
        <translation>Lizenz</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/oss_licenses.ui" line="90"/>
        <source>More licenses...</source>
        <translation>Weitere Lizenzen...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/oss_licenses.ui" line="93"/>
        <source>Show more open-source software licenses</source>
        <translation>Weitere Open-Source Software Lizenzen anzeigen</translation>
    </message>
</context>
<context>
    <name>diag_program</name>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="20"/>
        <source>PLC program</source>
        <translation>PLC Programm</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="47"/>
        <source>Python PLC start program:</source>
        <translation>Python PLC Startprogramm:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="40"/>
        <source>Set write permissions for plc program to workdirectory</source>
        <translation>Schreibberechtigung für Arbeitsverzeichnis auf RevPi setzen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="26"/>
        <source>Program arguments:</source>
        <translation>Programargumente:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="73"/>
        <source>Transfair PLC program</source>
        <translation>PLC Programm übertragen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="80"/>
        <source>ZIP archive</source>
        <translation>ZIP Archiv</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="85"/>
        <source>TGZ archive</source>
        <translation>TGZ Archiv</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="151"/>
        <source>Upload</source>
        <translation>Hochladen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="144"/>
        <source>Download</source>
        <translation>Herunterladen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="107"/>
        <source>Transfair format:</source>
        <translation>Übertragungsformat:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="114"/>
        <source>Including piCtory configuration</source>
        <translation>Inklusive piCtory Konfiguraiton</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="121"/>
        <source>Remove all files on Revolution Pi before upload</source>
        <translation>Alle Dateien auf Revolution Pi vor dem Hochladen löschen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="131"/>
        <source>Control files</source>
        <translation>Steuerdateien</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="158"/>
        <source>piCtory configuraiton</source>
        <translation>piCtory Konfiguration</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="165"/>
        <source>Process image from piControl0</source>
        <translation>Prozessabbild von piControl0</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="60"/>
        <source> sec.</source>
        <translation> Sek.</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiprogram.ui" line="33"/>
        <source>Software watchdog (0=disabled):</source>
        <translation>Software watchdog (0=deaktiviert):</translation>
    </message>
</context>
<context>
    <name>diag_revpiinfo</name>
    <message>
        <location filename="../../../ui_dev/revpiinfo.ui" line="43"/>
        <source>RevPiPyLoad version on RevPi:</source>
        <translation>RevPiPyLoad Version auf RevPi:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiinfo.ui" line="14"/>
        <source>Program information</source>
        <translation>Programminformationen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiinfo.ui" line="27"/>
        <source>RevPi Python PLC - Commander</source>
        <translation>RevPi Python SPS - Commander</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiinfo.ui" line="86"/>
        <source>Version:</source>
        <translation></translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpiinfo.ui" line="116"/>
        <source>RevPiModIO, RevPiPyLoad and RevPiPyControl are community driven projects. They are all free and open source software.
All of them comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

(c) Sven Sager, License: GPLv2</source>
        <translation type="unfinished"></translation>
    </message>
</context>
<context>
    <name>diag_search</name>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="14"/>
        <source>Search Revolution Pi devices</source>
        <translation>Revolution Pi Geräte suchen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="22"/>
        <source>Searching for Revolution Pi devices in your network...</source>
        <translation>Netzwerk nach Revolution Pi Geräten durchsuchen...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="35"/>
        <source>Restart search</source>
        <translation>Suche neu starten</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="93"/>
        <source>IP address</source>
        <translation>IP Adresse</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="101"/>
        <source>&amp;Connect to Revolution Pi</source>
        <translation>Mit RevPi &amp;verbinden</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="108"/>
        <source>&amp;Save connection</source>
        <translation>Verbindung &amp;speichern</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="88"/>
        <source>Zero-conf name</source>
        <translation>Zero-conf Name</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="125"/>
        <source>Copy host name</source>
        <translation>Hostnamen kopieren</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="130"/>
        <source>Copy IP address</source>
        <translation>IP Adresse kopieren</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="135"/>
        <source>Open piCtory</source>
        <translation>piCtory öffnen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="140"/>
        <source>Connect via SSH (recommended)</source>
        <translation>Über SSH verbinden (empfohlen)</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="143"/>
        <source>Establish a connection via encrypted SSH tunnel</source>
        <translation>Verbindung über verschlüsselten SSH Tunnel herstellen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="148"/>
        <source>Connect via XML-RPC</source>
        <translation>Über XML-RPC verbinden</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="151"/>
        <source>You have to configure your Revolution Pi to accept this connections</source>
        <translation>Sie müssen den Revolution Pi für diese Art der Verbindung konfigurieren</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="156"/>
        <source>Connect</source>
        <translation>Verbinden</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/avahisearch.ui" line="159"/>
        <source>Connect to Revoluton Pi</source>
        <translation>Mit Revolution Pi verbinden</translation>
    </message>
</context>
<context>
    <name>diag_simulator</name>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="14"/>
        <source>piControl simulator</source>
        <translation>piControl Simulator</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="20"/>
        <source>Simulator settings</source>
        <translation>Simulatoreinstellungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="26"/>
        <source>Last used:</source>
        <translation>Zuletzt verwendet:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="33"/>
        <source>piCtory file:</source>
        <translation>piCtory Datei:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="50"/>
        <source>select...</source>
        <translation>auswählen...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="57"/>
        <source>Process image:</source>
        <translation>Prozessabbild:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="74"/>
        <source>Stop action:</source>
        <translation>Stopaktion:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="81"/>
        <source>Restart action:</source>
        <translation>Neustartaktion:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="102"/>
        <source>Restore piCtory default values</source>
        <translation>piCtory Standardwerte setzen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="112"/>
        <source>Reset everything to ZERO</source>
        <translation>Alles auf NULL setzen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="122"/>
        <source>RevPiModIO integration</source>
        <translation>RevPiModIO Integration</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="154"/>
        <source>Start with piCtory default values</source>
        <translation>Start mit piCtory Standardwerten</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="164"/>
        <source>Start with empty process image</source>
        <translation>Start mit leerem Prozessabbild</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="174"/>
        <source>Start without changing actual process image</source>
        <translation>Start ohne Veränderung des Prozessabbilds</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="95"/>
        <source>Remove process image file</source>
        <translation>Prozessabbilddatei löschen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/simulator.ui" line="128"/>
        <source>You can work with this simulator if you call RevPiModIO with this additional parameters:</source>
        <translation>Mit diesem Simulator kann gearbeitet werden, indem zum Aufruf von RevPiModIO folgende Parameter hinzugefügt werden:</translation>
    </message>
</context>
<context>
    <name>diag_sshauth</name>
    <message>
        <location filename="../../../ui_dev/sshauth.ui" line="17"/>
        <source>SSH authentication</source>
        <translation>SSH Authentifizierung</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/sshauth.ui" line="29"/>
        <source>SSH username:</source>
        <translation>SSH Benutzername:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/sshauth.ui" line="36"/>
        <source>SSH password:</source>
        <translation>SSH Passwort:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/sshauth.ui" line="56"/>
        <source>Username and password will be saved in secured operating systems&apos;s password storage.</source>
        <translation>Benutzername und Kennwort werden im Passwortspeicher vom Betriebssystem gesichert.</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/sshauth.ui" line="59"/>
        <source>Save username and password</source>
        <translation>Benutzername und Kennwort merken</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/sshauth.ui" line="82"/>
        <source>Note: The default user for SSH is &quot;pi&quot; which differs from the web configuration. You can find the password on the sticker on the device.</source>
        <translation>Hinweis: Der Standardbenutzer für SSH ist &quot;pi&quot; dies weicht von der Web-Konfiguration ab. Das Kennwort finden sie auf dem Aufkleber am Gerät.</translation>
    </message>
</context>
<context>
    <name>wid_debugcontrol</name>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="35"/>
        <source>Revolution Pi devices</source>
        <translation>Revolution Pi Module</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="43"/>
        <source>Open to stay on top</source>
        <translation>Immer im Vordergrund</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="50"/>
        <source>IO Control</source>
        <translation>EA Übertragung</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="61"/>
        <source>Read &amp;all IO values</source>
        <translation>&amp;Alle EA Werte lesen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="82"/>
        <source>&amp;Refresh unchanged IOs</source>
        <translation>Unve&amp;ränderte EAs lesen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="98"/>
        <source>Write locally changed output values to process image (F6)</source>
        <translation>Schreibe lokal veränderte Ausgangswerte in das Prozessabbild (F6)</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="101"/>
        <source>&amp;Write changed outputs</source>
        <translation>Ausgänge &amp;schreiben</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="108"/>
        <source>&amp;Auto refresh values</source>
        <translation>&amp;Automatisch aktualisieren</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="115"/>
        <source>and write outputs</source>
        <translation>und Ausgänge schreiben</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="56"/>
        <source>Read all IO values and discard local changes (F4)

Hold this button pressed and it will refresh the IOs every 200 ms.</source>
        <translation>Alle EA Werte lesen und lokale Änderungen überschreiben (F4)

Wird der Button gehalten, aktualisieren sich die EAs alle 200 ms.</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/debugcontrol.ui" line="77"/>
        <source>Refresh all IO values which are locally not changed (F5)

Hold this button pressed and it will refresh the IOs every 200 ms.</source>
        <translation>Alle EA Werte aktualisieren, die lokal nicht geändert sind (F5)

Wird der Button gehalten, aktualisieren sich die EAs alle 200 ms.</translation>
    </message>
</context>
<context>
    <name>win_debugios</name>
    <message>
        <location filename="../../../ui_dev/debugios.ui" line="18"/>
        <source>{0}: Inputs | Outputs</source>
        <translation>{0}: Eingänge | Ausgänge</translation>
    </message>
</context>
<context>
    <name>win_files</name>
    <message>
        <location filename="../../../ui_dev/files.ui" line="14"/>
        <source>File manager</source>
        <translation>Dateimanager</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/files.ui" line="31"/>
        <source>Local computer</source>
        <translation>Lokaler Computer</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/files.ui" line="37"/>
        <source>Path to development root:</source>
        <translation>Entwicklerverzeichnis:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/files.ui" line="44"/>
        <source>Open developer root directory</source>
        <translation>Öffne Entwicklerverzeichnis</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/files.ui" line="200"/>
        <source>Reload file list</source>
        <translation>Dateiliste neu laden</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/files.ui" line="193"/>
        <source>RevPiPyLoad working directory:</source>
        <translation>RevPiPyLoad Arbeitsverzeichnis:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/files.ui" line="331"/>
        <source>Stop - Upload - Start</source>
        <translation>Stoppen - Hochladen -Starten</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/files.ui" line="171"/>
        <source>Revolution Pi</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>win_revpicommander</name>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="56"/>
        <source>PLC &amp;start</source>
        <translation>SPS &amp;start</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="67"/>
        <source>PLC s&amp;top</source>
        <translation>SPS s&amp;top</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="78"/>
        <source>PLC restart</source>
        <translation>SPS Neustart</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="89"/>
        <source>PLC &amp;logs</source>
        <translation>SPS &amp;Logdateien</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="102"/>
        <source>Status:</source>
        <translation>Status:</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="133"/>
        <source>PLC watch &amp;mode</source>
        <translation>SPS &amp;Monitor</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="157"/>
        <source>&amp;File</source>
        <translation>&amp;Datei</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="168"/>
        <source>&amp;Help</source>
        <translation>&amp;Hilfe</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="176"/>
        <source>&amp;PLC</source>
        <translation>S&amp;PS</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="190"/>
        <source>&amp;Connections</source>
        <translation>&amp;Verbindungen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="205"/>
        <source>&amp;Connections...</source>
        <translation>&amp;Verbindungen...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="213"/>
        <source>&amp;Search Revolution Pi...</source>
        <translation>&amp;Suche Revolution Pi...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="221"/>
        <source>&amp;Quit</source>
        <translation>&amp;Beenden</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="226"/>
        <source>Visit &amp;webpage...</source>
        <translation>&amp;Webseite besuchen...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="236"/>
        <source>PLC &amp;logs...</source>
        <translation>SPS &amp;Logdateien...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="244"/>
        <source>PLC &amp;options...</source>
        <translation>SPS &amp;Optionen...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="252"/>
        <source>PLC progra&amp;m...</source>
        <translation>SPS Progra&amp;mm...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="260"/>
        <source>PLC de&amp;veloper...</source>
        <translation>SPS Ent&amp;wickler...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="268"/>
        <source>piCtory configuraiton...</source>
        <translation>piCtory Konfiguration...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="273"/>
        <source>&amp;Disconnect</source>
        <translation>&amp;Trennen</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="281"/>
        <source>Reset driver...</source>
        <translation>Treiber zurücksetzen...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="286"/>
        <source>RevPi si&amp;mulator...</source>
        <translation>RevPi Si&amp;mulator...</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpicommander.ui" line="231"/>
        <source>&amp;Info...</source>
        <translation></translation>
    </message>
</context>
<context>
    <name>win_revpilogfile</name>
    <message>
        <location filename="../../../ui_dev/revpilogfile.ui" line="14"/>
        <source>RevPi Python PLC Logfiles</source>
        <translation>RevPi Python PLC Logdateien</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpilogfile.ui" line="21"/>
        <source>Stay on top of all windows</source>
        <translation>Immer im Vordergrund bleiben</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpilogfile.ui" line="28"/>
        <source>Linewrap</source>
        <translation>Zeilenumbruch</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpilogfile.ui" line="45"/>
        <source>RevPiPyLoad - Logfile</source>
        <translation>RevPiPyLoad - Logdatei</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpilogfile.ui" line="85"/>
        <source>Clear view</source>
        <translation>Ansicht leeren</translation>
    </message>
    <message>
        <location filename="../../../ui_dev/revpilogfile.ui" line="92"/>
        <source>Python PLC program - Logfile</source>
        <translation>Python PLC Programm - Logdatei</translation>
    </message>
</context>
</TS>
