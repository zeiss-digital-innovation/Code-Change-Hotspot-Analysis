# Szenarios

### Problembeschreibung
Hans Team steht vor dem Problem, dass das Kompilieren der bereits entwickelten Software bis zu zwei Stunden dauern kann, da bei jeder neuen Kompilierung wird auch der Code kompiliert, der nicht mehr weiterentwickelt wird, sogenannter "Legacy-Code". Hans möchte nun herausfinden welche der Dateien zum "Legacy-Code" gehören. Ist dieser "Legacy-Code" gefunden, kann er verschoben, um damit beim Kompilieren nicht mit übersetzt zu werden. Dies verringert die Zeit für die Kompilierung, was die Entwicklungszeit erheblich senkt. 


### Szenario 1 
Hans nutzt das Tool, um sich eine interaktive Treemap anzeigen zu lassen, die zeigt welche Dateien am häufigsten beziehungsweise garnicht geändert werden. Hans kann sich dabei durch die einzelnen Pfadebenen "klicken". Die Daten basieren auf einer mithilfe des Tools vorher generierten Text-Datei der GitHistorie. 