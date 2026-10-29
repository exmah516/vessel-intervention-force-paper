param([ValidateSet('Save','Render')][string]$Action = 'Render')
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'word_native.ps1')
$taskRoot=Split-Path $PSScriptRoot -Parent
$taskDocPath=Join-Path $taskRoot '面向往复夹持递送的血管介入机器人力反馈扰动建模与残差抑制_MathType_自然多行版.docx'
$taskWord=Get-JqrWord
$taskAlerts=$taskWord.DisplayAlerts
$taskBackgroundSave=$taskWord.Options.BackgroundSave
$taskWord.DisplayAlerts=0
$taskWord.Options.BackgroundSave=$false
$taskDoc=$null
try {
  $taskDoc=$taskWord.Documents.Open($taskDocPath,$false,($Action -eq 'Render'))
  $taskUpdated=$taskDoc.Fields.Update()
  $taskDoc.Repaginate()
  $taskRecords=@()
  foreach($taskField in $taskDoc.Fields) {
    $taskCode=$taskField.Code.Text.Trim()
    if($taskCode -notmatch '^(SEQ JQREquation|REF JQR_eq_)'){continue}
    $taskRecord=[ordered]@{Code=$taskCode;Result=$taskField.Result.Text;Page=$taskField.Result.Information(3);Line=$taskField.Result.Information(10)}
    if($taskCode -match '^SEQ JQREquation') {
      $taskParagraph=$taskField.Result.Paragraphs.Item(1)
      if($taskParagraph.Range.InlineShapes.Count -ne 1){throw "Equation has unexpected shape count: $taskCode"}
      $taskFormula=$taskParagraph.Range.InlineShapes.Item(1)
      $taskRecord.FormulaPage=$taskFormula.Range.Information(3)
      $taskRecord.FormulaLine=$taskFormula.Range.Information(10)
      $taskRecord.Width=$taskFormula.Width
      $taskRecord.Height=$taskFormula.Height
      $taskRecord.FormulaY=$taskFormula.Range.Information(6)
      $taskRecord.NumberY=$taskField.Result.Information(6)
      $taskRecord.NumberX=$taskField.Result.Information(5)
      if($taskRecord.Page -ne $taskRecord.FormulaPage -or $taskRecord.Line -ne $taskRecord.FormulaLine){throw "Number separated from equation: $($taskField.Result.Text)"}
    }
    $taskRecords += [pscustomobject]$taskRecord
  }
  if($taskUpdated -ne 0){throw "Word fields update failed: $taskUpdated"}
  if($Action -eq 'Save') {$taskDoc.Save()}
  if($Action -eq 'Render') {
    $taskPdf=Join-Path $PSScriptRoot 'render_native_multiline.pdf'
    $taskDoc.ExportAsFixedFormat($taskPdf,17)
  }
  $taskReport=[ordered]@{Path=$taskWord.Path;Version=$taskWord.Version;Pages=$taskDoc.ComputeStatistics(2);UpdateResult=$taskUpdated;Action=$Action;Fields=$taskRecords}
  $taskReport | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $PSScriptRoot ('native_multiline_word_'+$Action.ToLower()+'.json')) -Encoding utf8
  [pscustomobject]@{Path=$taskWord.Path;Pages=$taskReport.Pages;Fields=$taskRecords.Count;UpdateResult=$taskUpdated;Action=$Action} | ConvertTo-Json
}
finally {
  if($null -ne $taskDoc){$taskDoc.Close(0)}
  $taskWord.DisplayAlerts=$taskAlerts
  $taskWord.Options.BackgroundSave=$taskBackgroundSave
}
