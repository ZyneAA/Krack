@echo off

set JAR_PATH = ./lavalink/Lavalink.jar
code -n --wait
echo java -jar "%JAR_PATH%" & echo. & echo. & echo. & echo exit | code-terminal