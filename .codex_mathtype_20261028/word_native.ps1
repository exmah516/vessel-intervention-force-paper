if (-not ('JqrNativeWord' -as [type])) {
Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public static class JqrNativeWord {
  public delegate bool EnumProc(IntPtr h, IntPtr p);
  [DllImport("user32.dll")] static extern bool EnumChildWindows(IntPtr h, EnumProc p, IntPtr l);
  [DllImport("user32.dll",CharSet=CharSet.Unicode)] static extern int GetClassName(IntPtr h,StringBuilder b,int n);
  [DllImport("oleacc.dll")] static extern int AccessibleObjectFromWindow(IntPtr h,uint id,ref Guid iid,[MarshalAs(UnmanagedType.IDispatch)] out object o);
  public static object FromWindow(IntPtr h) {
    object result=null;
    EnumChildWindows(h,(w,p)=> {
      var b=new StringBuilder(128);GetClassName(w,b,128);
      if (b.ToString()=="_WwG") {
        var iid=new Guid("00020400-0000-0000-C000-000000000046");object o;
        if(AccessibleObjectFromWindow(w,0xFFFFFFF0,ref iid,out o)==0) {result=o;return false;}
      }
      return true;
    },IntPtr.Zero);
    return result;
  }
}
'@
}
function Get-JqrWord {
  $taskWordProcesses=Get-Process WINWORD -ErrorAction SilentlyContinue
  foreach($taskWordProcess in $taskWordProcesses) {
    if($taskWordProcess.MainWindowHandle -eq 0 -or $taskWordProcess.MainWindowTitle -match '受保护|Protected View'){continue}
    $taskNativeWindow=[JqrNativeWord]::FromWindow($taskWordProcess.MainWindowHandle)
    if($null -ne $taskNativeWindow) {
      $taskWord=$taskNativeWindow.Application
      if($taskWord.Path -like '*Microsoft Office*'){return $taskWord}
    }
  }
  throw 'Microsoft Word native document window not found'
}
