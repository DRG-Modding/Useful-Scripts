echo off
::this is genuinely the dumbest shit I have ever written but I cant figure out any other way

dir %1 /ad /s /b > folderStructure.temp
move %1 %1_reading

for /f %%l in (folderStructure.temp) do (
  md %%l
)

del folderStructure.temp
cd %1
md _ModBPs
cd ..
move %1 %1_empty
move %1_reading %1