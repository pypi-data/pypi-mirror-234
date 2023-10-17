@echo off
setlocal enabledelayedexpansion

for /f "tokens=*" %%a in ('ipconfig /all') do (
  set line=%%a
  if "!line:Connection-specific DNS Suffix=!" neq "!line!" (
    set suffix=!line:*Suffix.=!
    if not "!suffix:Suffix Search List=!" == "!suffix!" (
      rem skip the Suffix Search List line
    ) else (
      set suffix=!suffix:Connection-specific DNS Suffix  . : =!
      echo !suffix!>suffix.txt
      )
    )
  )
)


