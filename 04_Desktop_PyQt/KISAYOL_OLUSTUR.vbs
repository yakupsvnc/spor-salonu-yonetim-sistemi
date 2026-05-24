Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")

Set oShortcut = WshShell.CreateShortcut(strDesktop & "\Spor Salonu Yonetim.lnk")
oShortcut.TargetPath = "pythonw.exe"
oShortcut.Arguments = """" & WshShell.CurrentDirectory & "\main.py"""
oShortcut.WorkingDirectory = WshShell.CurrentDirectory
oShortcut.Description = "Spor Salonu Yonetim Sistemi"
oShortcut.Save

MsgBox "Masaustu kisayolu olusturuldu!", 64, "Tamam"
